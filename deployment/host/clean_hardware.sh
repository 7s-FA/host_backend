#!/usr/bin/env bash
set -eo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if [[ "${1:-}" == -h || "${1:-}" == --help ]]; then
    echo 'hostclean: 정지한 장치의 남은 작업·오류 잠금 정리. 전체 성공 후 hostrun.'
    echo '관제 실행 중에는 먼저 현장 정지·공정 종료를 확인하고 hoststop 하세요.'
    echo '실패 주문·응답 미확인 기록은 삭제하지 않습니다. 초기 자세·주차 이동은 hostrun에서 실행합니다.'
    exit 0
fi
if (( $# )); then echo '사용법: hostclean [--help]' >&2; exit 2; fi
source "$root/scripts/host_env.bash"
[[ "$ROS_DOMAIN_ID" == 40 && "${HOST_MOCK:-0}" != 1 ]] || { echo '실물 Domain 40 전용입니다.' >&2; exit 1; }
mkdir -p "$HOST_RUNTIME_DIR"
exec 9> "$HOST_RUNTIME_DIR/host.lock"
if ! flock -n 9; then
    echo '관제 실행/준비 중에는 정리할 수 없습니다. 현장 정지·공정 종료 확인 후 hoststop 하세요.' >&2
    exit 1
fi
cd "$root"
# Keep host.lock inherited until cleanup exits: hostrun cannot race these goals.
exec /usr/bin/python3 "$root/scripts/prepare_cells.py" --cleanup-only
