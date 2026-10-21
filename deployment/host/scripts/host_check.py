#!/usr/bin/env python3
"""Local preflight only: no ROS node, discovery, subscription, or robot command."""
import argparse
import hashlib
import importlib
import os
from pathlib import Path
import socket
import sys
import xml.etree.ElementTree as ET


def signature():
    package = Path(os.environ['HOST_BACKEND_DIR']) / 'src/host_pkg'
    digest = hashlib.sha256(str(package.resolve()).encode())
    for path in [package / 'CMakeLists.txt', package / 'package.xml',
                 *sorted((package / 'action').glob('*.action'))]:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signature', action='store_true')
    parser.add_argument('--skip-ports', action='store_true')
    args = parser.parse_args()
    if args.signature:
        print(signature())
        return 0

    failures = []

    def check(label, function):
        try:
            detail = function()
            print(f'[OK] {label}' + (f': {detail}' if detail else ''))
        except Exception as exc:
            failures.append(label)
            print(f'[FAIL] {label}: {exc}', file=sys.stderr)

    def configuration():
        domain = int(os.environ['ROS_DOMAIN_ID'])
        if not 0 <= domain <= 232:
            raise ValueError('HOST_ROS_DOMAIN_ID는 0~232 범위여야 합니다.')
        discovery = os.environ['ROS_AUTOMATIC_DISCOVERY_RANGE']
        if discovery not in ('SUBNET', 'LOCALHOST', 'OFF', 'SYSTEM_DEFAULT'):
            raise ValueError(f'지원하지 않는 HOST_DISCOVERY_RANGE: {discovery}')
        profile = os.environ.get('FASTRTPS_DEFAULT_PROFILES_FILE')
        if profile:
            tree = ET.parse(profile)
            for entry in tree.findall('.//{*}interfaceWhiteList/{*}address'):
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
                    try:
                        probe.bind((entry.text, 0))
                    except OSError as exc:
                        raise RuntimeError(f'관제 LAN 주소 {entry.text}를 사용할 수 없습니다. config/host_dds.xml과 PC IP를 확인하세요.') from exc
        return f'domain={domain}, discovery={discovery}, RMW={os.environ["RMW_IMPLEMENTATION"]}'

    def packages():
        from ament_index_python.packages import get_package_prefix
        for name in ('rosbridge_server', 'rosapi', os.environ['RMW_IMPLEMENTATION']):
            get_package_prefix(name)
        importlib.import_module('rosbridge_library.capabilities.send_action_goal')
        importlib.import_module('rosapi_msgs.srv')
        return 'rosbridge Action / rosapi / DDS'

    def interfaces():
        from ament_index_python.packages import get_package_prefix
        from host_pkg.action import Arm, Burger
        from rclpy.type_support import check_for_type_support
        expected = Path(os.environ['HOST_RUNTIME_DIR']) / 'install/host_pkg'
        actual = Path(get_package_prefix('host_pkg'))
        if actual.resolve() != expected.resolve():
            raise RuntimeError(f'다른 host_pkg가 선택되었습니다: {actual}; --build로 준비하세요.')
        for interface in (Arm, Burger):
            check_for_type_support(interface)
        return str(actual)

    def backend():
        source = Path(os.environ['HOST_BACKEND_DIR']) / 'src/host_pkg/src'
        sys.path.insert(0, str(source))
        importlib.import_module('main')
        return 'main.py 및 모든 관제 노드 import 완료 (노드 실행 없음)'

    def web_files():
        root = Path(os.environ['HOST_WEB_DIR'])
        for relative in ('index.html', 'host/server.py', 'host/host_control.launch.py', 'host/action_discovery.py'):
            if not (root / relative).is_file():
                raise FileNotFoundError(root / relative)
        return str(root)

    def ports():
        for port in (8082, 9090):
            with socket.socket() as probe:
                probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    probe.bind(('127.0.0.1', port))
                except OSError as exc:
                    raise RuntimeError(f'127.0.0.1:{port} 사용 불가: {exc}') from exc
        return '127.0.0.1:8082 / 9090 사용 가능'

    check('ROS 환경', configuration)
    check('ROS 패키지', packages)
    check('프로젝트 Action 타입', interfaces)
    check('백엔드', backend)
    check('웹 파일', web_files)
    if not args.skip_ports:
        check('수신 포트', ports)
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
