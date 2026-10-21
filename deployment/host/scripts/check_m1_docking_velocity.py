#!/usr/bin/env python3
"""Offline regression of the deployed M1 controller; no ROS imports or robot I/O.

Usage: python3 scripts/check_m1_docking_velocity.py SNAPSHOT_DIRECTORY
Directory: docking_control.remote.py, docking_node.remote.py, docking.after.yaml.
The snapshot is read from M1: the host checkout has an older controller/profile.
"""
import ast
import importlib.util
import math
from pathlib import Path
import sys
from types import SimpleNamespace
import yaml


def check(root):
    spec = importlib.util.spec_from_file_location('m1_deployed_control', root/'docking_control.remote.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    cfg = yaml.safe_load((root/'docking.after.yaml').read_text())
    before = yaml.safe_load((root/'docking.before.yaml').read_text())
    expected = yaml.safe_load((root/'docking.before.yaml').read_text())
    expected['control']['move_final_enabled'] = False
    assert cfg == expected, 'Only pulse-mode selection may change'

    # Load only pure node methods, never the ROS node or its publishers.
    tree = ast.parse((root/'docking_node.remote.py').read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'DockingNode')
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in ('handle_move', 'motor_error')]
    namespace = {}
    exec(compile(ast.Module(body=methods, type_ignores=[]), '<pure-node-methods>', 'exec'), namespace)

    def settings(mode, config=cfg):
        values = dict(config['control'])
        if mode != 'normal':
            values.update(config[mode+'_control'])
        return module.Settings(**values)

    def inputs(c, t, x=0., v=0., z=None):
        z = c.cfg.staging_distance_m if z is None else z
        a = math.radians(c.cfg.camera_yaw_deg)
        c.set_odom(x, 0., 0., v, 0., t)
        c.set_observation({'pose_valid': True, 'tvec_m': [z*math.tan(a), 0., z],
                           'normal_yaw_rad': a}, t)

    def aligned(s):
        c = module.DockingControl(s)
        inputs(c, 0.)
        assert c.start(0.)[0]
        for i in range(1, 101):
            t = i*.01
            inputs(c, t)
            c.tick(t)
            if c.state == 'FINAL_APPROACH':
                return c, t
        raise AssertionError('alignment never completed')

    old, t = aligned(settings('normal', before))
    assert old.move_request is not None
    old.move_request['id'] = 1
    old.set_move_status(1, 'ERROR', 'position_setup')
    assert old.tick(t) == (0., 0.)
    assert old.state == 'FAULT' and old.reason == 'move_error:position_setup'
    print('PASS: previous pulse path reproduces recorded position_setup failure')

    for mode in ('normal', 'parking', 'assembly'):
        s = settings(mode)
        assert s.move_final_enabled is False
        c, t = aligned(s)
        assert c.move_request is None
        # A poison publisher makes any move or torque command fail the test.
        class NoCommands:
            def publish(self, _):
                raise AssertionError('Unexpected STM32 move/torque command')
        node = SimpleNamespace(control=c, execute=True, move_cmd_pub=NoCommands(),
                               motor_time=t, motor_torque=True)
        x, v = 0., 0.
        for _ in range(2000):
            t += .01
            x += v*.01
            inputs(c, t, x=x, v=v, z=max(.001, s.staging_distance_m-x))
            v, w = c.tick(t)
            namespace['handle_move'](node)
            assert 0 <= v <= s.final_speed_mps and w == 0.
            assert c.move_request is None
            if c.state == 'DOCKED':
                break
            assert c.state in ('FINAL_APPROACH', 'STOPPING'), (mode, c.state, c.reason)
        assert c.state == 'DOCKED' and v == 0.
        expected_distance = s.staging_distance_m-s.encoder_stop_distance_m-s.encoder_stop_lead_m
        assert abs(x-expected_distance) < .002, (mode, x, expected_distance)
        print(f'PASS: {mode} alignment -> velocity/encoder approach -> verified stop; {x:.4f} m; no torque commands')

    c, t = aligned(settings('normal'))
    node = SimpleNamespace(control=c, execute=True, move_cmd_pub=NoCommands(),
                           motor_time=t, motor_torque=False)
    error = namespace['motor_error'](node, t)
    assert error == 'motor_torque_off'
    c.halt(error)
    namespace['handle_move'](node)
    assert c.tick(t) == (0., 0.) and c.state == 'FAULT'
    node.motor_torque = True
    assert namespace['motor_error'](node, t+1) == 'motor_state_timeout'

    c, t = aligned(settings('normal'))
    assert c.tick(t+.4) == (0., 0.) and c.state == 'ODOM_WAIT'
    assert c.tick(t+5) == (0., 0.) and c.state == 'FAULT'
    c, t = aligned(settings('normal'))
    inputs(c, t+.01, x=.2)
    assert c.tick(t+.01) == (0., 0.) and c.reason == 'odometry_jump'
    c, t = aligned(settings('normal'))
    for i in range(1, 401):
        inputs(c, t+i*.01)
        c.tick(t+i*.01)
    assert c.state == 'FAULT' and c.reason == 'final_approach_stalled'
    print('PASS: torque off/stale, odom timeout/jump, and stalled motion still stop; no automatic torque recovery')


if __name__ == '__main__':
    check(Path(sys.argv[1]))
