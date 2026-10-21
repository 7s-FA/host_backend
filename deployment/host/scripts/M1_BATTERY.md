# M1 배터리 연동 작업 기록

## 2026-10-20 적용 전 확인

- M1: `robot@192.0.2.104`, ROS namespace `/burger1`, domain 40.
- 실행 중인 `/stm32/imu/status`는 `fw=imu-ahrs-v6.7`을 보고한다.
- `/burger1/battery_state`의 publisher count는 0이다. 웹 구독자는 존재한다.
- 현재 ROS 토픽 목록에 `/stm32/battery_voltage`는 없다.
- M1의 `~/battery_check/README.md`는 배터리가 11.1V LiPo이며 펌웨어 전압 발행이 미구현이라고 기록한다. Pi의 5V 입력이나 시계용 BATT_V는 로봇 배터리 잔량으로 사용하지 않는다.
- M1에 남은 `~/STMProject/burger` 소스에는 v6.7의 move_status 기능이 없다. 해당 소스를 그대로 빌드하여 덮어쓰지 않는다.
- 사용자가 최신 저장소 `https://github.com/7s-FA/M3_stm32.git`를 제공했다. `M3_stm32/`에 커밋 `9cdd070ed4e6b11ee77acd847d8e34605617dc41`을 받아 v6.7과 기존 배터리 부저 코드를 확인했다.
- 일시적인 SSH 연결 끊김 후 연결을 복구했다. 사용자가 다시 정지 상태를 확인했고 ROS motion_owner도 idle이었다. Host에는 과거 실패 주문이 남아 있지만 pending_commands=0, manual_move=null이었다.

## 적용한 코드

`m1_battery_bridge.py`는 `/stm32/battery_voltage`의 Float32 전압(V)을 `/burger1/battery_state`로 중계한다. 펌웨어가 발행하는 실측 전압을 수신하며 중계 노드 자체에는 모터 제어 기능이 없다.

- 새 유효 측정값을 수신할 때만 발행한다. 이전 값의 반복 발행이나 임의의 초기값은 없다.
- 0, 음수, NaN, 무한대는 발행하지 않는다. 수신이 끊기면 웹의 기존 5초 지연 표시가 적용된다.
- 측정하지 않은 전류·용량·퍼센트는 NaN으로 둔다. 웹의 퍼센트는 기존 전압 기반 추정치이며 실측 잔량이 아니다.
- 전체 플래시 백업 후 펌웨어 기록·검증 완료. 본체와 M1 Action 서비스를 복구했으며 배터리 중계 자동 실행을 등록했다. 이동 명령과 모터 토크 켜기 요청은 보내지 않았다.

## 검증

실물 domain 40과 분리된 domain 149 / LOCALHOST에서 `test_m1_battery_bridge.py` 통과. 시작 시 미발행, 전압 전달, 잘못된 입력 거부, 수신 중단 시 재발행 없음, 재수신을 확인했다. 기존 웹 `robot-battery-client.test.cjs`도 통과했다.

최신 펌웨어의 기존 100ms 배터리 측정 결과를 캐시해 1Hz best-effort Float32 `/stm32/battery_voltage`로 발행하도록 수정했다. 모터 UART 읽기를 추가하거나 주행 제어를 변경하지 않았다. 실패/0값/500ms 초과된 캐시는 발행하지 않는다. 전압 발행 오류만으로 모터 재연결·정지를 일으키지 않는다. 부저 알고리즘은 유지했다. 진단 태그는 `imu-ahrs-v6.7-battery`다.

- `M3_stm32/tests/run_reconnection.sh` 통과: 주행·피드백·상대 이동·watchdog·IMU·UART·배터리 및 23개 ROS 생성 실패/정리 회귀 검사.
- GCC ARM 13.2.1로 펌웨어 빌드 완료: `M3_stm32/build/battery/burger.elf`, FLASH 169700 B / RAM 88792 B.
- 빌드 도구는 `/tmp/m1-arm-toolchain/root`에만 압축 해제했고 시스템 패키지는 변경하지 않았다.
- 자동 실행 파일: `start_m1_battery_bridge.bash`, `m1-battery.service`. M1에 설치 및 enable했고 active 상태를 확인했다.

## 실물 적용 및 수신 검증 완료

- 10:08 KST: 원본 512KiB 플래시 백업 후 OpenOCD `Verified OK` 확인.
- 펌웨어: `imu-ahrs-v6.7-battery`, IMU calibration READY, attitude=1.
- M1 → 호스트 ROS → 실제 열린 관제 페이지에서 **11.70V / 추정 67%** 표시 확인. 퍼센트는 기존 10.5~12.3V 환산 기준의 추정치다.
- 배터리 중계만 잠시 정지했을 때 웹이 `수신 지연 · 마지막 추정 67% · 11.70 V`로 전환하고, 서비스 재시작 후 정상 표시로 복구됨을 확인했다.
- `burger1-base.service`, `m1-battery.service`, `m1-action.service` 모두 active, 배터리 서비스 enabled.
- 모터 토크는 펌웨어 재시작 후 off(바퀴 상태 0)로 확인했다. 임의로 다시 켜거나 이동시키지 않았다. 과거 실패 주문 및 실제 배치는 변경하지 않았다.

### 복구 자료

- M1 원본: `/home/robot/M3_stm32_battery_20261020/backup.PJywO4JP/flash.bin`
- 관제 PC 원본: `.runtime/diagnostics/m1-battery-20261020/original-flash.bin`
- M1 적용 ELF: `/home/robot/M3_stm32_battery_20261020/burger-battery.elf`
- ELF SHA256: `f8760e5f0898b1a91e3eb0e7bf092ab1c67b3ee03a7d43bea553ddf9e40c0051`
- 해당 소스 보관: `/home/robot/M3_stm32_battery_20261020/m1-battery-source-20261020.tar.gz`
- 중계: `/home/robot/AMR/battery_telemetry/`, unit: `~/.config/systemd/user/m1-battery.service`
- 원본 복원은 정지·진행 작업 없음 확인 후 수행한다. 배터리 중계 서비스 정지는 모터 정지가 아니다.

### 정지 상태의 수신 주기 비교 (각 20초)

| 구간 | IMU | raw JointState | odom | 관찰 |
|---|---:|---:|---:|---|
| 적용 전 | 21.8Hz | 8.1Hz | 8.1Hz | IMU 최대110ms, JointState 288ms, odom 289ms |
| 적용 직후 | 20.9Hz | 8.0Hz | 8.0Hz | IMU 최대1116ms, JointState 420ms, odom 320ms; IMU read_errors=1 |
| 안정화 후 재측정 | 22.2Hz | 7.8Hz | 7.8Hz | IMU 최대306ms, JointState 353ms, odom 295ms; read_errors=1 유지 |

평균 수신률은 비슷하나 공백이 전혀 없다는 검증은 아니다. 적용 전후 모터 토크 상태와 시작 직후 부하가 같지 않아 배터리 발행만의 영향을 분리할 수 없다. 주행 성능·최악 지연은 실물 주행에서 별도로 확인해야 한다.

## 별도 문의: 웨이포인트 근처 멈춤

- 실제 Nav2 로그: 09:09:45.910 목표 성공 → 09:09:47.532 다음 목표 시작, 약 1.62초 간격.
- 웨이포인트 실행 코드는 새 목표 전에 최신 odom으로 최소 0.5초 정지를 확인하며, 좌표 도착·정지·방향 정렬을 별도로 수행한다.
- 09:09:57에는 별도의 `Failed to make progress`와 목표 중단이 있었고, 09:10:06/11에 방향 정렬 후 09:10:14 재이동, 09:10:21 목표 성공 기록이 있다.
- 따라서 짧은 구간 전환 정지와 진행 실패 후 재시도 지연을 구분해야 한다. 배터리 수정 적용 전의 현상이다.
- 이번 작업에서는 Nav2 경로·정지 확인·회전 조건을 변경하지 않았다.

## 10월 20일 재부팅 후 배터리 수신 중단 수정

10:21 재부팅 때 중계가 Wi-Fi 주소 할당보다 먼저 시작했다. 중계 로그에 `All whitelist interfaces were filtered out`가 있었고 서비스는 active로 남았으나 관제에 배터리가 전달되지 않았다. Wi-Fi 연결 후 배터리 중계만 재시작하자 웹에서 **11.20V / 추정 39%** 수신이 복구됐다.

재발 방지를 위해 `start_m1_battery_bridge.bash`가 DDS를 생성하기 전에 `wait_m1_battery_network.py`를 실행한다. 기존 DDS XML의 UDPv4 허용 주소가 실제 UP 인터페이스에 할당됐는지 확인하고, 준비 전에는 최대 90초 기다린다. 시간 초과 시 실패 종료해 기존 systemd `Restart=on-failure` 정책으로 재시도한다. 허용 주소/방화벽을 바꾸거나 다른 인터페이스로 우회하지 않는다. 준비 후에는 대기 검사를 종료하므로 주행 중 반복 검사 부하는 없다.

- 오프라인 부팅 순서 검사 6개 통과: 즉시 준비, 2초 지연 연결, 다른 주소만 존재, 인터페이스 DOWN, 설정 파일 없음, 빈 허용 목록.
- 실행기와 새 대기 스크립트를 M1 `/home/robot/AMR/battery_telemetry/`에 배포했다. 새로 설치할 때 두 파일을 함께 복사해야 한다.
- 이전 실행기: `/home/robot/AMR/battery_telemetry/backup-network-20261020/start_m1_battery_bridge.bash`.
- 수정 후 `M1 battery DDS interface ready: 192.0.2.104` 로그 및 중계 시작 확인. 모터·Nav2·펌웨어는 변경하지 않았고 실물 재부팅 시험은 하지 않았다.

## 2026-10-20 16:00 IMU 통신 복구 및 hostrun 토크 준비

- 사용자 정지·주변 비움·공정 종료 확인 후 적용. 주행 목표/팔 HOME은 보내지 않았다.
- 사용자가 새로 올린 펌웨어와 같은 Drive/IMU/ROS 분리 구조의 upstream main `716f271b825ea14ecc9e0238e66b634fdf71ac43`에서 수정했다. 로컬 브랜치 `codex/m1-imu-startup`.
- 이전 상태: IMU HAL_BUSY(2) 뒤 samples가 고정되고 read_errors만 증가했다. 부팅/통신 중단 후 토크 OFF인데 기존 hostrun은 RESTART(잠금 해제)만 보내고 토크를 확인하지 않았다.
- `imu-v6.8-recovery`: I2C1 PB8/PB9를 오픈드레인으로 최대 9클록+STOP 후 주변장치를 재초기화한다. 1초 간격으로 제한하고, 물리적으로 LOW인 버스는 실패로 보고한다. 센서 통신 복구 시 기존 yaw/보정값을 유지하고 긴 공백을 적분하지 않는다. 초기 센서 실패도 재시도한다. 초기화/복구 대기는 RTOS 양보 방식으로 변경했다.
- 통신 두절 시 모터 정지·토크 해제, 명령 watchdog, 이전 속도 미재생은 유지한다. 자동으로 토크를 재활성화하지 않는다.
- M1 준비 작업자는 새로운 IMU 데이터/증가하는 sample 수/정상 진단/정지 odom을 확인해야 토크를 켠다. hostrun은 팔 초기 이동 전에 기존 M1/M2 host-ready를 호출한다. --parked는 전달하지 않는다. 미정리 주문이 있으면 기존 복구 화면 경로를 유지한다.
- ARM 빌드 성공: FLASH 178420B / RAM 98128B. C 오류 주입·회귀 11개 실행 파일 및 호스트 준비 Python 24개 검사 통과.
- 현재 플래시 512KiB 백업 후 OpenOCD Verified OK. ELF SHA256 `6b51e373c0bb543cfb1c2e98df1ca20cf7eb74db71dbbf2215b3117a6d933eb8`.
- M1 백업: `/home/robot/M3_stm32_recovery_20261020/backup.pc2JP62P/flash.bin`. 호스트 보관: `.runtime/diagnostics/m1-recovery-20261020/`. 소스 overlay는 기록된 base-commit 위에 적용한다.
- 실제 준비 요청 `M1-20261020T160101539214`: success=true, movement_sent=false, parked=false. 양쪽 바퀴 상태 1(토크 ON), 속도 0, 엔코더 3052/3052 유지, owner idle, move IDLE.
- 20초 수신: IMU 445개, 최대 공백 302ms; odom 160개, 최대 공백 376ms; 배터리 11.2V. 후속 samples=9782, read_errors=0, recovery=0/0. 실제 I2C fault 주입 및 주행/도킹 시험은 하지 않았고, 물리 배선 이상이나 장시간 무오류를 보증하는 검증은 아니다.

### 같은 날 최종 보완: 첫 오류 빠른 복구

첫 적용 후 정지 관찰 중 실제 I2C 오류 2회가 발생했고 `recovery=2/2`, 토크 ON, 엔코더 3052/3052 유지로 자동 복구를 확인했다. 따라서 물리 통신 오류 자체가 사라졌다는 뜻은 아니다. 첫 오류의 대기 시간을 다음 IMU 주기(20ms)로 줄이고 복구 실패 시에만 1초 backoff를 적용했다. RTOS 스케줄링·통신을 포함한 실제 복구 완료 시간이 20ms라는 보장은 아니다.

- 최종 ELF SHA256: `f898f3b3b181c38a5a9b75e40b0fbdaed36760ce74be0de7adfe41cb7eb34718`, FLASH 178436B / RAM 98128B.
- 동일 오류 주입·회귀 11개 실행 파일 재통과 후 백업·쓰기·Verified OK.
- 최종 준비 요청 `M1-20261020T161143839908`: success=true, movement_sent=false, parked=false.
- 보관 ELF·source-overlay.tar.gz는 최종 보완본으로 갱신했다. 첫 적용 후 실제 복구 기록은 `first-recovery-run-telemetry.json`, 최종 확인은 `final-telemetry.json`.
