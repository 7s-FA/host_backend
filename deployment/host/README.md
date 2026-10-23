# 관제 PC 실행 환경 · host_total (2026-10-22)

host_web와 host_backend를 형제 폴더로 받고 이 폴더의 내용을 상위 final_project에 복사합니다. ROS 2 Jazzy가 필요합니다.

```bash
mkdir -p ~/final_project
cd ~/final_project
git clone -b host_total https://github.com/7s-FA/host_web.git
git clone -b host_total https://github.com/7s-FA/host_backend.git
cp -a host_backend/deployment/host/. .
bash start_host.sh --check
```

config/와 scripts/의 192.0.2.* 주소, robot/warehouse/operator 계정·홈 경로를 실제 설치에 맞추세요. SSH 키는 별도로 등록합니다. 웹은 http://localhost:8082/control.html입니다.

`aliases.bash`를 확인하고 ~/.bashrc에 `source "$HOME/final_project/aliases.bash"`를 추가합니다.

| 명령 | 동작 |
|---|---|
| hostrun | 관제와 웹 실행. 자동 초기 위치 준비 없음 |
| hostmanual | 장치별 수동 점검 화면 |
| hostmock | 실물과 분리된 Domain 149·LOCALHOST 모의 실행 |
| hostamr | M1/M2 Action 서버 시작 |
| hostready | 지정 주차 위치·방향에서 M1/M2 준비; 모터 토크 준비 포함 |
| hoststop | 관제 프로세스 종료. 실물 비상정지 대체 아님 |
| hostrestart | 정지·공정 종료 후 자재창고·조립대 제어 서버 재시작 |
| hostreset | 실패 주문 복구 절차 |
| howtoready | 준비 명령 안내 |

장치 초기 위치 이동은 웹의 전체 초기화에서 현장 확인 후 실행합니다. 예전 hostclean 별칭은 제거됐고, 서버 재시작은 hostrestart로 구분합니다. clean_hardware.sh는 이전 정리 도구 보존본이며 기본 시작 과정에 포함되지 않습니다. 재시작은 전원·케이블·기구 문제를 해결하는 명령이 아닙니다.

작업 중 주문 추가는 기존 연속 공정에 연결되며 A/B 각각 최대 2개입니다. 공정 실패·일시정지·불확실한 결과는 자동으로 해제하지 않습니다.
