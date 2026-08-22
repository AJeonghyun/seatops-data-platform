# SeatOps

> 동시 좌석 선점 환경에서 발생하는 이벤트를 수집하고, 데이터 품질을 검증하며, 오류 데이터를 안전하게 재처리하는 Data Ops 프로젝트

## 프로젝트 소개

SeatOps는 실제 티켓 사이트와 분리된 가상 티켓팅 환경입니다.

사용자와 확률·규칙 기반 가상 경쟁자가 동일한 좌석을 두고 경쟁하는 상황을 생성하고, 이 과정에서 발생한 사용자 및 시스템 이벤트를 수집합니다.

이 프로젝트의 목적은 티켓팅 게임을 만드는 것이 아니라 다음 데이터 엔지니어링 문제를 직접 구현하고 검증하는 것입니다.

- 동일 좌석에 대한 동시 요청 처리
- 좌석 상태 일관성 보장
- 사용자 및 시스템 이벤트 수집
- 이벤트 데이터 품질 검증
- 오류 데이터 격리 및 재처리
- 중복 이벤트의 멱등 처리
- 사용자 병목 및 시스템 장애 분석
- 서비스 모니터링과 부하 테스트

## 핵심 검증 시나리오

동일한 좌석에 100개의 요청이 동시에 발생하는 상황을 가정합니다.

정상적인 처리 결과는 다음과 같습니다.

- 좌석 선점 성공: 1건
- 좌석 선점 충돌: 99건
- 활성화된 좌석 선점 기록: 1건
- 성공 이벤트: 1건
- 최종 좌석 상태: `HELD`

이를 통해 동시 요청에서도 좌석이 중복 선점되지 않고, 좌석 상태와 이벤트 데이터가 일관되게 기록되는지 검증합니다.

## MVP 범위

### 포함

- [ ] 티켓팅 연습 세션 생성
- [ ] 좌석 목록 및 상태 조회
- [ ] 사용자 좌석 선점
- [ ] 확률·규칙 기반 가상 경쟁자
- [ ] 좌석 상태 머신
- [ ] 원자적 좌석 선점
- [ ] Transactional Outbox
- [ ] Raw Event 수집
- [ ] 데이터 품질 검증
- [ ] 오류 데이터 Quarantine
- [ ] 멱등 재처리
- [ ] 부하 테스트
- [ ] 운영 지표 및 모니터링

### 제외

- 실시간 사용자 PvP
- 결제 시스템
- 실제 티켓 사이트 UI 복제
- 보안문자 우회
- 실제 티켓 사이트 자동 접속
- 머신러닝 기반 Bot

## 예상 데이터 흐름

```text
User / Rule-based Bot
        ↓
     FastAPI
        ↓
PostgreSQL Transaction
 ├─ Seat State
 ├─ Seat Hold
 └─ Outbox Event
        ↓
   Event Worker
        ↓
    Raw Events
        ↓
Data Quality Validation
   ├─ Clean Events
   └─ Quarantine
        ↓
Metrics / Analysis / Reprocessing
```

## 좌석 상태

```text
AVAILABLE → HELD → CONFIRMED
               ↘ EXPIRED → AVAILABLE
               ↘ CANCELLED → AVAILABLE
```

허용되지 않은 상태 전이는 Data Quality 오류로 기록하고 Quarantine 대상으로 분류합니다.

## 기술 스택

| 영역         | 기술                |
| ------------ | ------------------- |
| Language     | Python              |
| API          | FastAPI             |
| Database     | PostgreSQL          |
| ORM          | SQLAlchemy          |
| Migration    | Alembic             |
| Testing      | pytest              |
| Load Testing | Locust              |
| Container    | Docker Compose      |
| Monitoring   | Prometheus, Grafana |
| CI           | GitHub Actions      |

기술 스택은 구현 과정에서 변경될 수 있으며, 중요한 변경 사항은 ADR로 기록합니다.

## 데이터 품질 검증 항목

- 필수 필드 누락
- 중복 `event_id`
- 존재하지 않는 세션 또는 좌석 참조
- 허용되지 않은 좌석 상태 전이
- 비정상적인 이벤트 발생 시각
- 좌석 상태와 성공 이벤트 간 불일치
- 이미 처리된 이벤트의 중복 재처리

## 성공 기준

- [ ] 동일 좌석에 대한 100개 동시 요청 중 정확히 1개만 성공한다.
- [ ] 좌석 상태 변경과 Outbox Event가 하나의 트랜잭션으로 처리된다.
- [ ] 중복 이벤트를 다시 처리해도 결과 데이터가 증가하지 않는다.
- [ ] 잘못된 이벤트가 정상 데이터와 분리되어 Quarantine에 저장된다.
- [ ] Quarantine 이벤트를 수정한 뒤 안전하게 재처리할 수 있다.
- [ ] 부하 테스트 결과를 처리량·지연시간·오류율 기준으로 분석한다.

## 개발 로드맵

### Week 1 — 동시성 제어

- 프로젝트 환경 구성
- 좌석 및 세션 데이터 모델링
- 좌석 상태 머신 구현
- 좌석 선점 API 구현
- 동시 요청 통합 테스트

### Week 2 — 이벤트 수집

- 이벤트 스키마 정의
- Transactional Outbox 구현
- Raw Event 적재
- 규칙 기반 Bot 구현

### Week 3 — Data Quality

- 데이터 품질 검증 규칙 구현
- Clean 및 Quarantine 분리
- 오류 이벤트 재처리
- 멱등성 검증

### Week 4 — 운영 및 검증

- Locust 부하 테스트
- 운영 메트릭 수집
- 모니터링 대시보드
- 장애 시나리오 실험
- 결과 문서화

## 프로젝트 문서

```text
docs/
├── 01_mvp_scope.md
├── architecture.md
├── event_schema.md
├── data_quality_rules.md
├── load_test_report.md
├── incident_reports/
└── adr/
```

## 현재 상태

🚧 MVP 범위를 정의하고 핵심 동시성 시나리오를 설계하는 단계입니다.

구현 진행에 따라 기능 체크리스트, 테스트 결과, 아키텍처와 장애 해결 기록을 지속해서 업데이트할 예정입니다.

## 윤리 및 보안 범위

SeatOps는 학습과 포트폴리오 제작을 위한 독립적인 가상 환경입니다.

실제 티켓 판매 사이트에 접속하거나 요청을 전송하지 않으며, 실제 사이트의 UI 복제, 보안문자 우회, 자동 구매 및 매크로 기능을 제공하지 않습니다.
