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
alias hostreset='python3 "$HOST_WORKSPACE/scripts/host_reset.py"'
# 실제 SSH 주소/계정으로 변경하세요. 정지·공정 종료 후에만 사용합니다.
alias hostrestart='ssh warehouse@192.0.2.166 "systemctl --user restart warehouse-arm1.service" && ssh -t robot@192.0.2.113 "sudo systemctl restart workcell-actions.service"'
howtoready() {
  printf '%s\n' '준비: hostcheck → hostamr → hostrun' '지정 주차 위치·방향 확인 후: hostready' '초기 위치 이동: 웹 전체 초기화' '개별 점검: hostmanual / 모의: hostmock' '관제 종료: hoststop / 팔 서버 재시작: 정지 확인 후 hostrestart'
}
