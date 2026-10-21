# 프로젝트 폴더를 바꾸었다면 아래 값도 변경하세요.
export HOST_WORKSPACE="${HOST_WORKSPACE:-$HOME/final_project}"
alias hostrun='bash "$HOST_WORKSPACE/start_host.sh"'
alias hostmanual='bash "$HOST_WORKSPACE/start_host.sh" --manual'
alias hostmock='bash "$HOST_WORKSPACE/start_host.sh" --mock'
alias hostcheck='bash "$HOST_WORKSPACE/start_host.sh" --check'
alias hostbuild='bash "$HOST_WORKSPACE/start_host.sh" --build'
alias hostmonitor='bash "$HOST_WORKSPACE/start_host.sh" --monitor-only'
alias hostamr='bash "$HOST_WORKSPACE/start_amr.sh"'
alias hostready='bash "$HOST_WORKSPACE/start_amr.sh" --ready --parked'
alias hoststop='python3 "$HOST_WORKSPACE/scripts/host_stop.py"'
alias hostclean='bash "$HOST_WORKSPACE/clean_hardware.sh"'
alias hostreset='python3 "$HOST_WORKSPACE/scripts/host_reset.py"'
howtoready() {
  printf '%s\n' '준비: hostcheck → hostamr → hostrun' '지정 주차 위치·방향에서만: hostready' '개별 점검: hostmanual / 모의: hostmock' '종료·정리: 현장 정지 확인 → hoststop → hostclean'
}
