#!/usr/bin/env bash
set -eo pipefail

usage() {
    cat <<'HELP'
사용법: hostamr [--status | --ready [--parked]] [--robot M1|M2]
  옵션 없음       M1·M2 Action 서버 시작. 이미 실행 중이면 유지합니다.
  --status        서비스 상태만 조회합니다.
  --ready         센서·위치·모터 토크·정지 상태를 준비하고 정지 잠금을 해제합니다.
  --parked        --ready와 함께, 두 로봇이 지정 주차 위치·방향에 있을 때만 사용합니다.
  --robot M1|M2   지정한 로봇만 실행합니다. 기본은 M1 다음 M2입니다.
  -h, --help      사용법

SSH 비밀번호를 물으면 해당 로봇의 비밀번호를 입력하세요.
--ready는 이동 목적지 Goal을 보내지 않습니다. 주문은 웹 관제에서 시작합니다.
연결이 끊기거나 준비가 실패하면 자동 재시도하지 않습니다.
HELP
}

mode=start
robot=all
parked=false
while (( $# )); do
    case "$1" in
        --status|--ready)
            if [[ "$mode" != start ]]; then echo '--status와 --ready는 각각 실행하세요.' >&2; exit 2; fi
            mode="${1#--}" ;;
        --parked) parked=true ;;
        --robot)
            shift
            if [[ "${1:-}" != M1 && "${1:-}" != M2 ]]; then echo '--robot M1 또는 --robot M2를 지정하세요.' >&2; exit 2; fi
            robot="$1" ;;
        -h|--help) usage; exit 0 ;;
        *) echo "알 수 없는 옵션: $1" >&2; usage >&2; exit 2 ;;
    esac
    shift
done
if [[ "$parked" == true && "$mode" != ready ]]; then
    echo '--parked는 --ready와 함께 사용하세요.' >&2; exit 2
fi

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$root/config/amr.env"
command -v ssh >/dev/null || { echo 'openssh-client가 필요합니다.' >&2; exit 1; }
robots=(M1 M2)
if [[ "$robot" != all ]]; then robots=("$robot"); fi

for robot in "${robots[@]}"; do
    destination_var="AMR_${robot}_SSH"
    destination="${!destination_var}"
    if [[ ! "$destination" =~ ^[a-zA-Z0-9._-]+@[a-zA-Z0-9][a-zA-Z0-9.-]*$ ]]; then
        echo "config/amr.env의 $destination_var 주소 형식을 확인하세요." >&2; exit 2
    fi
    printf '\n[%s] %s · %s\n' "$robot" "$destination" "$mode"
    batch_options=()
    if [[ "${HOST_AMR_BATCH:-0}" == 1 ]]; then batch_options=(-o BatchMode=yes); fi
    if ! ssh -T "${batch_options[@]}" -o ConnectTimeout=8 -o ServerAliveInterval=5 -o ServerAliveCountMax=3 \
        -o StrictHostKeyChecking=accept-new -o NumberOfPasswordPrompts=1 \
        "$destination" "bash -s -- $robot $mode $parked" < "$root/scripts/amr_remote.bash"; then
        echo "$robot 처리 실패 또는 SSH 연결 끊김. 원격 결과를 확인한 뒤 다시 실행하세요. 이후 로봇은 실행하지 않았습니다." >&2
        exit 1
    fi
done
echo '완료. 서비스 active는 센서·위치·모터 준비 완료를 뜻하지 않습니다.'
