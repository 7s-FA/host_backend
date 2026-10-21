#!/usr/bin/env python3
"""Offline replay of recorded assembly failures. No ROS, sockets or robot I/O.

Usage: python3 scripts/check_m1_docking_alignment.py SNAPSHOT_DIRECTORY
"""
import importlib.util
import math
from pathlib import Path
import sys
import yaml


def check(root):
    spec = importlib.util.spec_from_file_location('alignment_snapshot', root/'docking_control.remote.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    cfg = yaml.safe_load((root/'docking.after.yaml').read_text())
    settings = module.Settings(**{**cfg['control'], **cfg['assembly_control']})
    assert settings.lateral_tolerance_m == .002 and settings.yaw_tolerance_deg == .7
    a = math.radians(settings.camera_yaw_deg)
    samples = [(.14727828750514063, .006733245371165911, 2.8309105578072016),
               (.14769836229612945, .006344470044329531, 2.601942715379807),
               (.14727193450312331, .007495566755007411, 3.0569390869523625)]

    def inputs(c, t, bx, by, theta, angle=0., w=0.):
        z = math.cos(a)*bx + math.sin(a)*by
        xr = math.sin(a)*bx - math.cos(a)*by
        c.set_odom(0., 0., angle, 0., w, t)
        c.set_observation({'pose_valid': True, 'tvec_m': [xr, 0., z],
                           'normal_yaw_rad': a-theta}, t)

    for index, (z, by0, degrees) in enumerate(samples, 1):
        bx0 = (z-math.sin(a)*by0)/math.cos(a)
        theta0 = math.radians(degrees)
        c = module.DockingControl(settings)
        angle = w = 0.
        for i in range(1500):
            t = i*.02
            bx = bx0*math.cos(angle)+by0*math.sin(angle)
            by = -bx0*math.sin(angle)+by0*math.cos(angle)
            theta = theta0-angle
            inputs(c, t, bx, by, theta, angle, w)
            if i == 0:
                assert c.start(t)[0]
            v, w = c.tick(t)
            assert v == 0., 'Heading correction must not advance toward the board'
            assert abs(w) <= settings.near_angular_rps
            assert c.move_request is None, 'Pulse motion must remain disabled'
            if c.state == 'FINAL_APPROACH':
                assert abs(by) <= settings.lateral_tolerance_m
                assert abs(theta) <= math.radians(settings.yaw_tolerance_deg)
                assert t >= settings.aligned_hold_s
                print(f'PASS: recorded attempt {index} aligns by rotation only in ideal simulation ({t:.2f}s)')
                break
            assert c.state != 'FAULT', c.reason
            # Existing controller test convention: STM32 velocity resolution.
            w = int(w*100)/100
            angle += w*.02
        else:
            raise AssertionError('Alignment did not settle')

    for bx, by, theta, reason in [(.147, .03, .05, 'insufficient_visual_alignment_space'),
                                  (.10, .005, .05, 'too_close_before_alignment')]:
        c = module.DockingControl(settings)
        inputs(c, 0., .25, 0., 0.)
        assert c.start(0.)[0]
        inputs(c, .02, bx, by, theta)
        assert c.tick(.02) == (0., 0.)
        assert c.state == 'FAULT' and c.reason == reason, (c.state, c.reason)
        print('PASS: unchanged stop guard:', reason)


if __name__ == '__main__':
    check(Path(sys.argv[1]))
