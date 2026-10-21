#!/usr/bin/env bash
# start_host.sh 또는 진단용 터미널에서 source하는 프로젝트 전용 환경.
# ROS setup 파일은 nounset 없이 로드합니다.
export HOST_PROJECT_ROOT
HOST_PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
export HOST_BACKEND_DIR="$HOST_PROJECT_ROOT/host_backend"
export HOST_WEB_DIR="$HOST_PROJECT_ROOT/host_web"
export HOST_RUNTIME_DIR="$HOST_PROJECT_ROOT/.runtime/host"
export HOST_OVERLAY="$HOST_RUNTIME_DIR/install/local_setup.bash"
source "$HOST_PROJECT_ROOT/config/host.env" || return 1

if [[ ! -r /opt/ros/jazzy/setup.bash ]]; then
    echo 'ROS 2 Jazzy가 필요합니다: /opt/ros/jazzy/setup.bash' >&2
    return 1
fi

# 이전 워크스페이스·Python 가상환경·DDS 검색 설정을 이번 프로세스에서 분리.
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
unset PYTHONPATH PYTHONHOME LD_LIBRARY_PATH
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS ROS_DISCOVERY_SERVER ROS_NAMESPACE
unset FASTRTPS_DEFAULT_PROFILES_FILE FASTDDS_DEFAULT_PROFILES_FILE CYCLONEDDS_URI
source /opt/ros/jazzy/setup.bash || return 1
export ROS_DOMAIN_ID="$HOST_ROS_DOMAIN_ID"
export ROS_AUTOMATIC_DISCOVERY_RANGE="$HOST_DISCOVERY_RANGE"
export RMW_IMPLEMENTATION="$HOST_RMW_IMPLEMENTATION"
# Real equipment: use the control LAN for discovery and data, including local
# nodes. Keep Tailscale and shared-memory transport out of this DDS session.
# Mock remains isolated on domain 149 / LOCALHOST with the default transport.
if [[ "$ROS_DOMAIN_ID" == 40 && "$ROS_AUTOMATIC_DISCOVERY_RANGE" == SUBNET && "$RMW_IMPLEMENTATION" == rmw_fastrtps_cpp ]]; then
    export FASTRTPS_DEFAULT_PROFILES_FILE="$HOST_PROJECT_ROOT/config/host_dds.xml"
fi
export ROS_LOG_DIR="$HOST_RUNTIME_DIR/log"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# --build는 기존 overlay가 없는 상태에서도 실행할 수 있어야 합니다.
if [[ -r "$HOST_OVERLAY" ]]; then
    source "$HOST_OVERLAY" || return 1
fi
