#!/usr/bin/env bash
# start_amr.sh가 SSH 표준입력으로 전송합니다. 원격 파일을 설치하지 않습니다.
set -eo pipefail
robot="${1:-}"
mode="${2:-}"
parked="${3:-false}"
[[ "$robot" == M1 || "$robot" == M2 ]] || exit 2
[[ "$mode" == start || "$mode" == status || "$mode" == ready ]] || exit 2
[[ "$parked" == true || "$parked" == false ]] || exit 2
[[ "$parked" != true || "$mode" == ready ]] || exit 2
unit="${robot,,}-action.service"

if [[ "$(systemctl --user show "$unit" -p LoadState --value)" != loaded ]]; then
    echo "$unit 미설치: 로봇의 AMR 서비스 설치를 확인하세요." >&2; exit 1
fi

if [[ "$mode" == ready ]]; then
    cli="$HOME/AMR/scripts/robot.py"
    [[ -f "$cli" ]] || { echo "실행 파일 없음: $cli" >&2; exit 1; }
    echo '준비: 모터 토크 활성화·정지 잠금 해제. 이동 목적지 전송 없음.'
    args=(--robot "$robot" host-ready)
    if [[ "$parked" == true ]]; then args+=(--parked); fi
    python3 "$cli" "${args[@]}"
    python3 "$cli" --robot "$robot" status
elif [[ "$mode" == start ]]; then
    state="$(systemctl --user show "$unit" -p ActiveState --value)"
    case "$state" in
        active) echo "$unit 이미 실행 중: 현재 서버 유지" ;;
        inactive) systemctl --user start "$unit" ;;
        *) echo "$unit 상태=$state. journalctl --user -u $unit 로 확인하세요." >&2; exit 1 ;;
    esac
fi

systemctl --user show "$unit" -p ActiveState -p SubState -p MainPID
if [[ "$mode" != status ]]; then
    [[ "$(systemctl --user show "$unit" -p ActiveState --value)" == active ]] || exit 1
fi
