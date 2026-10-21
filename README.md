# host_total · 호스트 공정 제어 통합 (2026-10-21)

현장 `pjb` 기반 작업 내용을 공유하는 브랜치입니다. 기존 `main`이나 `pjb`를 덮어쓰지 않았습니다. `main`과 다른 커밋 이력이 있으므로 단순 최신 main 복사본으로 보지 마세요.

## 추가·수정

- 실제 Action 최종 Result로 공정·수량을 진행하는 제어기, HTTP 웹 어댑터, 모의 장치.
- `parallel_process.py`: 자재 적재와 M2 대기 이동 등 독립 작업을 병렬 진행. 조립 완료 피드백으로 이동과 팔레트 적재를 분리하며 실패/미확인 작업은 추적.
- 실패 단계 재시도 성공 시 기존 자동 진행 선택 유지. 수동 이동과 주문 실행의 동시 접수 방지.
- `full_reset.py`, `initial_state.py`: 정지 잠금 정리 → 팔 시작 자세 → 리니어 초기 위치 → 이동로봇 주차. 결과 기록과 중복 전송/불명확 결과 보호.
- `parked_preparation.py`: 사람이 두 로봇을 지정 주차 위치·방향에 놓았을 때 위치·Nav2 재준비. 단순 이동 명령과 구분.
- 수동 점검 모드에서는 선택 장치만 연결돼도 개별 테스트 가능. 전체 주문과 전체 초기화는 차단하고 사용권·동작 중·불확실 결과 보호는 유지.
- 통합 실행기 `hostrun`, `hostmanual`, `hostclean`, `hoststop`와 설정·별칭 예시를 `deployment/host/`에 추가. 과거 추적되던 Python 캐시와 build/install/log 산출물을 제거. 새 PC에서는 Action 타입을 다시 빌드.

## 설치·실행

[통합 실행 환경 README](deployment/host/README.md)를 따르세요. `host_web`도 **host_total**을 함께 받습니다. 내부 IP·SSH 사용자·홈 경로는 예시로 바꿨으므로 실제 환경으로 설정해야 합니다.

```bash
python3 -m pytest tests -q
```

테스트는 모의 제어 검증입니다. 실물 준비 완료나 충돌 없는 동작을 보증하지 않습니다. 리니어 초기 위치는 `BUILD_SLIDE`(전진/확장 프리셋)이며, 시간 완료를 실측 위치 도착으로 간주하지 않습니다.

---

# host_backend

관제 공정 제어기와 ROS Action 클라이언트입니다. `host_pkg` 빌드는 Action
인터페이스를 생성하며, 실행 진입점은 `src/host_pkg/src/main.py`입니다.

통합 작업 공간의 관제 PC에서는 다음 명령을 사용합니다.

```bash
bash /home/operator/final_project/start_host.sh --mock
```

웹·rosbridge·rosapi·백엔드가 함께 실행됩니다. 설정·빌드·종료 방법과 현재 공정
기능의 범위는 [최상위 안내](../README.md)를 확인하세요. 공통 실행기는 이 폴더의
기존 `build*`·`install*` 대신 `../.runtime/host/`의 새 빌드를 사용합니다.

`control.py`는 최종 성공 Result로 단계·카운트를 진행하는 공정 제어기이고,
`action_transport.py`는 실제 Burger/Arm 클라이언트, `http_adapter.py`는
`control.html` 연결입니다. `mock_devices.py`는 Domain 149 / LOCALHOST에서만
실행됩니다. 실물은 `--mock` 없이 실행하며, 기본 `/web_to_ros` 시뮬레이션
재생 값은 새 주문을 시작하지 않습니다.

## 게시 전 확인

호스트/웹 모의·HTTP 테스트 합계 146개 통과. 실행기는 실제 로봇으로 실행하지 않음.
