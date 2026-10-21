# 관제 PC 통합 실행 환경 · host_total

ROS 2 Jazzy / Fast DDS 기반입니다. 이 폴더를 형제 저장소들의 상위 작업 폴더로 복사해 사용합니다. 게시 파일의 `192.0.2.*`와 `robot`, `warehouse`, `operator`는 **접속되지 않는 예시 주소·계정**입니다.

## 설치

```bash
mkdir -p ~/final_project
cd ~/final_project
git clone -b host_total https://github.com/7s-FA/host_web.git
git clone -b host_total https://github.com/7s-FA/host_backend.git
cp -a host_backend/deployment/host/. .
```

실제 환경에 맞춰 `config/amr.env`, `config/host_dds.xml`, `scripts/prepare_cells.py`의 SSH 대상, `scripts/cell_remote.py`의 로봇 PC 프로젝트 경로를 수정합니다. 방화벽·ROS domain·Action 타입·SSH 키 연결을 현장에 맞춰 준비합니다. 비밀번호나 개인키는 저장하지 않습니다.

```bash
bash start_host.sh --check
bash start_host.sh --mock
```

모의 모드는 Domain 149 / LOCALHOST를 사용하며 실물 준비 명령을 보내지 않습니다. 웹은 `http://localhost:8082/control.html`입니다. `host_web`와 `host_backend` 모두 host_total이어야 합니다.

## 별칭

`aliases.bash`의 프로젝트 위치를 확인한 뒤 아래 줄을 ~/.bashrc에 한 번 추가합니다.

```bash
source "$HOME/final_project/aliases.bash"
```

| 명령 | 동작 |
|---|---|
| hostcheck | 환경·포트·타입 점검 |
| hostmock | 모의 장치와 웹 실행 |
| hostamr | M1·M2 Action 서버 시작, 이미 실행 중이면 유지 |
| hostready | 지정 주차 위치·방향에 놓인 두 로봇의 준비 |
| hostrun | 센서·토크·정지 잠금·팔 시작 자세·리니어 확장 초기 위치 준비 후 웹 실행 |
| hostmanual | 초기 준비를 생략한 개별 점검; 선택 장치만 준비돼도 수동 이동 가능 |
| hoststop | 관제 프로세스 종료; 로봇 비상정지의 대체 수단 아님 |
| hostclean | 정지·종료된 작업과 잠금 정리; 이동·원점 복귀 없음 |
| hostreset | 실패 주문 복구 절차 |

hostrun의 초기화는 실제 팔·리니어 동작을 포함합니다. 리니어 초기 위치는 확장 프리셋(`BUILD_SLIDE`)입니다. 전체 초기화 버튼은 M1·M2 주차 이동도 포함합니다. 이미 실행 중이면 준비를 반복하지 않고 화면만 엽니다.

hostclean은 전원·통신·기구적 문제를 고치는 명령이 아닙니다. 진행 중이거나 결과가 미확인인 작업은 먼저 웹에서 정지·결과를 확인해야 하며, 실제 정지가 확인되지 않으면 정리를 중단합니다. `--parked`는 지정 주차 위치·방향 확인 후에만 사용합니다.

전체 공정은 자재창고·조립대 서버의 HOME/CLEAR_ERROR/완료 피드백 등 지원을 전제로 합니다. 이 브랜치는 해당 두 저장소의 원격 코드를 변경하지 않습니다.
