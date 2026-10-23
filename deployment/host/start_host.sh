#!/usr/bin/env bash
set -eo pipefail

usage() {
    cat <<'HELP'
사용법: bash start_host.sh [옵션] (스크립트의 절대경로로도 실행 가능)
  (옵션 없음)       웹(8082) + rosbridge(9090) + rosapi + 실물 관제 백엔드 (장치 초기 준비 없음)
  --mock            모의 ROS 장치와 전체 공정 실행 (Domain 149 / LOCALHOST 고정)
  --monitor-only    웹 + rosbridge/rosapi만 실행 (백엔드 제외)
  --no-browser      브라우저 자동 열기 없이 실행
  --no-arm-prepare  이전 명령 호환용 (기본 실행도 장치 초기 준비 생략)
  --manual          수동 점검: 초기 준비 생략, 연결된 로봇 개별 이동, 전체 공정 시작 금지
  --check           환경·Action 타입·포트 점검 후 종료, ROS 노드 실행 없음
  --build           현재 경로에서 Action 타입 재빌드 및 점검 후 종료
  -h, --help        사용법

첫 실행 또는 Action 소스/경로 변경 시 자동으로 로컬 빌드합니다.
화면: 서버 준비 후 기본 브라우저에서 http://localhost:8082/control.html 자동 열기
장치 초기 준비: 웹의 전체 초기화 버튼에서 현장 확인 후 실행
종료: Ctrl+C (프로세스 종료이며 로봇 정지 명령은 아님)
HELP
}

mode=run
with_backend=true
mock=false
manual=false
open_browser="${HOST_OPEN_BROWSER:-1}"
for argument in "$@"; do
    case "$argument" in
        --check|--build)
            if [[ "$mode" != run ]]; then
                echo '--check와 --build는 각각 실행하세요.' >&2
                exit 2
            fi
            mode="${argument#--}" ;;
        --monitor-only) with_backend=false ;;
        --mock) mock=true ;;
        --no-browser) open_browser=0 ;;
        --no-arm-prepare) : ;; # 기존 별칭과 실행 명령 호환
        --manual) manual=true ;;
        -h|--help) usage; exit 0 ;;
        *) echo "알 수 없는 옵션: $argument" >&2; usage >&2; exit 2 ;;
    esac
done
if [[ "$mock" == true && "$with_backend" == false ]]; then
    echo '--mock와 --monitor-only는 함께 사용할 수 없습니다.' >&2
    exit 2
fi
if [[ "$manual" == true && "$with_backend" == false ]]; then
    echo '--manual과 --monitor-only는 함께 사용할 수 없습니다.' >&2; exit 2
fi
export HOST_MANUAL_INSPECTION=0
if [[ "$manual" == true ]]; then export HOST_MANUAL_INSPECTION=1; fi
export HOST_MOCK=0
if [[ "$mock" == true ]]; then
    export HOST_MOCK=1 HOST_ROS_DOMAIN_ID=149 HOST_DISCOVERY_RANGE=LOCALHOST
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$script_dir/scripts/host_env.bash"
cd -- "$HOST_PROJECT_ROOT"
page_mode=hardware
if [[ "$mock" == true ]]; then page_mode=mock; fi
if [[ "$with_backend" == false ]]; then page_mode=monitor; fi
page_opener="$HOST_PROJECT_ROOT/scripts/open_host_page.py"
page_options=()
if [[ "$manual" == true ]]; then page_options+=(--manual); fi
checker="$HOST_PROJECT_ROOT/scripts/host_check.py"
signature="$(/usr/bin/python3 "$checker" --signature)"
stamp="$HOST_RUNTIME_DIR/interfaces.sha256"
previous_signature=''
if [[ -f "$stamp" ]]; then read -r previous_signature < "$stamp" || true; fi

if [[ "$mode" == check ]]; then
    if [[ ! -r "$HOST_OVERLAY" || "$signature" != "$previous_signature" ]]; then
        echo '현재 경로의 Action 빌드가 필요합니다: bash start_host.sh --build' >&2
        exit 1
    fi
    exec /usr/bin/python3 "$checker"
fi

mkdir -p "$HOST_RUNTIME_DIR/log"
exec 9> "$HOST_RUNTIME_DIR/host.lock"
if ! flock -n 9; then
    if [[ "$mode" == run && "$open_browser" == 1 ]]; then
        echo '이미 관제가 실행 중입니다. 같은 모드의 관제 화면을 확인합니다.'
        if /usr/bin/python3 "$page_opener" --mode "$page_mode" "${page_options[@]}" --timeout 3 9>&-; then
            exit 0
        fi
    fi
    echo '이미 관제 실행 또는 빌드가 진행 중입니다. 모드 변경은 작업 종료 후 hoststop → hostmanual 또는 hostrun 순서로 실행하세요.' >&2
    exit 1
fi

if [[ "$mode" == build || ! -r "$HOST_OVERLAY" || "$signature" != "$previous_signature" ]]; then
    if [[ ! -x /usr/bin/colcon ]]; then
        echo '빌드 도구가 필요합니다: sudo apt install python3-colcon-common-extensions' >&2
        exit 1
    fi
    echo "Action 타입 빌드: $HOST_RUNTIME_DIR"
    : > "$stamp"
    # 빌드에는 ROS 기본 환경만 사용하며 이전 host_pkg overlay를 포함하지 않습니다.
    unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH LD_LIBRARY_PATH
    source /opt/ros/jazzy/setup.bash
    /usr/bin/colcon --log-base "$HOST_RUNTIME_DIR/build-log" build \
        --base-paths "$HOST_BACKEND_DIR/src/host_pkg" \
        --build-base "$HOST_RUNTIME_DIR/build" \
        --install-base "$HOST_RUNTIME_DIR/install" \
        --packages-select host_pkg --cmake-clean-cache \
        --cmake-args -DBUILD_TESTING=OFF
    source "$HOST_OVERLAY"
    /usr/bin/python3 "$checker" --skip-ports
    printf '%s\n' "$signature" > "$stamp"
fi

if [[ "$mode" == build ]]; then
    echo '빌드 완료. bash start_host.sh로 실행할 수 있습니다.'
    exit 0
fi

/usr/bin/python3 "$checker"
if [[ "$open_browser" == 1 ]]; then
    /usr/bin/python3 "$page_opener" --mode "$page_mode" "${page_options[@]}" --parent-pid "$$" 9>&- &
fi
if [[ "$with_backend" == true ]]; then
    export ROBOT3_BRIDGE_TOKEN
    ROBOT3_BRIDGE_TOKEN="$(/usr/bin/python3 -c 'import secrets; print(secrets.token_hex(32))')"
else
    unset ROBOT3_BRIDGE_TOKEN
fi
echo "관제 실행: domain=$ROS_DOMAIN_ID / backend=$with_backend"
if [[ "$mock" == false && "$with_backend" == true && "$manual" == false ]]; then
    echo '장치 초기 준비 생략 · 필요할 때 웹의 전체 초기화 버튼으로 실행하세요.'
fi
if [[ "$manual" == true ]]; then echo '수동 점검 모드 · 초기 준비 생략 · 선택한 로봇만 연결 확인 · 전체 공정 시작 비활성'; fi
echo '공정 관제: http://localhost:8082/control.html'
if [[ "$mock" == true ]]; then echo '모의 실행: 실물 로봇 연결 없음'; fi
echo "로그: $ROS_LOG_DIR"
echo 'Ctrl+C: 함께 종료. 새 이동·작업은 주문 시작 후 전송하며, 미완료 주문 복구 시 정지를 요청합니다.'
exec /opt/ros/jazzy/bin/ros2 launch "$HOST_WEB_DIR/host/host_control.launch.py" \
    "with_backend:=$with_backend" \
    "mock_devices:=$mock" \
    "backend_script:=$HOST_BACKEND_DIR/src/host_pkg/src/main.py"
