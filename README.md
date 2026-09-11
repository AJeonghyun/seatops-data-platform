# SeatOps Data Platform

SeatOps는 가상의 티켓팅 이벤트를 생성하고, JSON Lines 원본 파일에서 PostgreSQL 분석 마트까지 적재·검증·가공하는 데이터 엔지니어링 포트폴리오 프로젝트입니다.

이 저장소의 1차 목표는 티켓팅 웹 서비스를 만드는 것이 아닙니다. 주니어 데이터 엔지니어에게 필요한 Python 처리, SQL 검증, PostgreSQL 모델링, ETL/ELT 파이프라인, Airflow 자동화, 데이터 품질 관리, 멱등성, 재처리, 테스트, CI를 코드와 실행 결과로 증명하는 것입니다.

## 현재 상태

현재 저장소는 1차 MVP 범위를 정의한 문서 단계입니다. 데이터 생성기, PostgreSQL DDL, Airflow DAG, 테스트, CI는 아직 구현하지 않았습니다.

구현된 기능만 완료로 체크하고, README의 주요 주장마다 코드, 테스트 또는 실행 결과를 연결합니다.

상세 범위는 [1차 MVP 범위](01_mvp_scope.md)에 기록합니다. 과제 열람·답안 작성용 학습 사이트는 별도 학습 도구이며 데이터 플랫폼의 웹 UI나 구현 완료 증거에 포함하지 않습니다.

## 1차 MVP 데이터 흐름

```text
Python Event Generator
        ↓
JSON Raw Files
        ↓
Airflow DAG
        ↓
PostgreSQL Raw Layer
        ↓
Validation / Transformation
   ├─ Staging Clean Data
   └─ Quarantine Data
        ↓
Daily Data Mart
        ↓
SQL Analysis
```

## 1차 MVP 범위

### 반드시 구현

- [ ] Python으로 가상 티켓 이벤트를 생성한다.
- [ ] 이벤트를 JSON Lines 형식의 Raw 파일로 저장한다.
- [ ] 같은 seed를 사용하면 같은 입력 데이터를 재현할 수 있다.
- [ ] Airflow DAG가 Raw 파일을 PostgreSQL Raw 계층에 적재한다.
- [ ] Raw 계층에 원본 payload를 보존한다.
- [ ] 검증을 통과한 이벤트를 Staging 계층으로 분리한다.
- [ ] 오류 이벤트를 오류 코드, 원인, 재처리 가능 여부와 함께 Quarantine에 저장한다.
- [ ] Staging 데이터를 사용해 일별·세션별 Mart를 생성한다.
- [ ] 같은 입력과 실행 날짜로 파이프라인을 다시 실행해도 데이터가 중복되지 않는다.
- [ ] Quarantine 이벤트를 수정한 뒤 안전하게 재처리할 수 있다.
- [ ] 각 단계의 입력 건수, 성공 건수, 실패 건수, 중복 건수를 기록한다.
- [ ] pytest로 정상 입력, 잘못된 입력, 중복 실행, 부분 실패, 재처리를 검증한다.
- [ ] GitHub Actions에서 테스트를 자동 실행한다.

### 1차 MVP에서 제외

- FastAPI
- 좌석 선점 API
- 동시성 제어
- Transactional Outbox
- Kafka
- Spark
- Kubernetes
- Terraform
- 복잡한 웹 UI
- Prometheus
- Grafana
- 클라우드 배포

위 항목은 포트폴리오에 좋아 보이기 때문에 추가하지 않습니다. 1차 MVP가 끝난 뒤 현재 구조에서 실제 한계가 확인될 때만 확장합니다.

## 기술 스택

| 영역 | 1차 MVP 기술 |
| --- | --- |
| Language | Python 3.11 이상 |
| Data Format | JSON Lines |
| Database | PostgreSQL |
| Workflow | Apache Airflow |
| Query | SQL |
| Test | pytest |
| Container | Docker Compose |
| CI | GitHub Actions |
| Version Control | Git, GitHub |

다음 기술은 필요할 때만 사용합니다.

| 기술 | 도입 기준 |
| --- | --- |
| SQLAlchemy | 표준 DB 드라이버와 SQL만으로 반복 코드가 과도해질 때 |
| Alembic | 수동 DDL 변경 이력을 추적하기 어려워질 때 |
| Pydantic | 이벤트 스키마 검증 코드가 복잡해질 때 |
| Pandas | SQL 또는 표준 Python만으로 집계·검증 코드가 불필요하게 복잡해질 때 |

## 초기 이벤트 후보

1차 MVP의 이벤트 종류는 작게 시작합니다.

- `SESSION_STARTED`
- `SEAT_VIEWED`
- `SEAT_HOLD_ATTEMPTED`
- `SEAT_HOLD_SUCCEEDED`
- `SEAT_HOLD_FAILED`
- `SESSION_ENDED`

초기 이벤트 스키마 후보는 다음 필드를 검토합니다.

- `event_id`
- `event_type`
- `occurred_at`
- `session_id`
- `user_id`
- `seat_id`
- `request_id`
- `payload`
- `schema_version`

이 필드는 아직 확정된 정답이 아닙니다. 각 필드가 필요한 이유를 설명하고, 초안 설계 후 리뷰를 통해 확정합니다.

## 데이터 계층 후보

다음 테이블을 기본 후보로 두되, 전체 DDL은 설계 리뷰 후 작성합니다.

- `raw_ticket_events`
- `stg_ticket_events`
- `quarantine_ticket_events`
- `mart_daily_session_metrics`
- `pipeline_run_history`

각 테이블은 먼저 역할과 Grain을 정의합니다. 그 다음 컬럼, PK, Unique Key, FK, 인덱스를 설계합니다.

## 데이터 품질 규칙 후보

1차 MVP에서 고려할 품질 규칙은 다음과 같습니다.

- 필수 필드 누락
- 허용되지 않은 `event_type`
- 잘못된 timestamp 형식
- 미래 시각 또는 비정상적으로 오래된 이벤트
- 중복 `event_id`
- 존재하지 않는 세션 참조
- 존재하지 않는 좌석 참조
- 이벤트 순서상 불가능한 상태
- 성공 이벤트와 실패 이벤트의 논리적 충돌
- 지원하지 않는 `schema_version`

각 규칙은 규칙 ID, 검사 대상, 실패 조건, 오류 코드, 심각도, Quarantine 여부, 재처리 가능 여부, 테스트 사례를 정의한 뒤 구현합니다.

## Data Mart 최소 지표

최종 Mart에서는 SQL로 다음 지표를 조회할 수 있어야 합니다.

- 날짜
- 세션 ID
- 전체 이벤트 수
- 좌석 선점 시도 수
- 좌석 선점 성공 수
- 좌석 선점 실패 수
- 선점 성공률
- 고유 사용자 수
- 고유 좌석 수
- 중복 이벤트 수
- 데이터 품질 오류 수
- 처리 지연시간

Mart SQL은 바로 정답을 만들지 않고, 먼저 Grain과 계산식을 정의한 뒤 구현합니다.

## 개발 로드맵

### Phase 1: Python·SQL 복구와 이벤트 생성

- 개발환경 구성
- 이벤트 스키마 초안
- 정상 이벤트 생성
- 의도적인 오류 이벤트 생성
- JSON Lines 파일 저장
- Python 단위 테스트
- 기본 SQL 복습

완료 조건:

- 정상 및 오류 이벤트를 재현 가능하게 생성한다.
- 동일한 seed를 사용하면 같은 데이터가 생성된다.
- 각 필드의 의미를 설명할 수 있다.

### Phase 2: PostgreSQL 데이터 모델링과 적재

- Raw, Staging, Quarantine, Mart의 역할 정의
- 테이블 Grain 정의
- DDL 작성
- Raw 파일 적재
- 중복 적재 방지
- 적재 결과 검증 SQL 작성

완료 조건:

- Raw 이벤트가 원본 그대로 저장된다.
- 동일 파일을 두 번 적재해도 중복이 증가하지 않는다.
- 입력 건수와 적재 건수가 SQL로 검증된다.

### Phase 3: 데이터 품질과 변환

- 품질 규칙 정의
- 검증 로직 구현
- 정상 데이터와 오류 데이터 분리
- 오류 코드와 원인 저장
- 품질 규칙 단위 테스트

완료 조건:

- 의도적으로 생성한 오류가 예상 규칙에 의해 탐지된다.
- 오류 이벤트가 Staging에 포함되지 않는다.
- 품질 검사 결과를 SQL로 확인할 수 있다.

### Phase 4: Airflow 파이프라인

- Airflow와 PostgreSQL을 Docker Compose로 구성
- 적재 Task
- 품질 검증 Task
- Staging 변환 Task
- Data Mart 생성 Task
- 작업 의존성 설정
- 재실행 및 실패 복구 검증

완료 조건:

- 하나의 DAG 실행으로 전체 파이프라인이 완료된다.
- 중간 Task가 실패하면 후속 Task가 실행되지 않는다.
- 실패 원인을 로그에서 확인할 수 있다.
- DAG를 재실행해도 최종 데이터가 중복되지 않는다.

### Phase 5: 재처리·테스트·CI

- Quarantine 재처리
- Pipeline Run 이력
- 통합 테스트
- GitHub Actions
- 실패 시나리오 기록
- README 결과 중심 개편

완료 조건:

- 오류 이벤트를 수정하고 다시 처리할 수 있다.
- 재처리 결과가 중복되지 않는다.
- 테스트가 CI에서 자동 실행된다.
- README의 주요 주장마다 코드, 테스트 또는 실행 결과가 연결된다.

## 2차 확장 후보

1차 MVP가 완성된 이후, 서비스 이벤트 수집이 필요해질 때 다음을 검토합니다.

- FastAPI
- 좌석 선점 API
- PostgreSQL 동시성 제어
- Transactional Outbox
- Outbox Worker
- Worker 장애와 복구
- Locust 기반 부하 테스트

스트리밍 처리가 실제 한계로 확인되면 다음을 검토합니다.

- Kafka
- 실시간 Consumer
- 중복 메시지 처리
- Consumer 재시작
- Schema evolution

## 3차 확장 후보

로컬 Docker Compose 기반 1차 MVP와 2차 서비스 확장이 안정화된 뒤, 운영·분산 처리 한계가 확인되면 다음을 검토합니다.

- AWS S3
- AWS RDS
- MWAA 또는 Airflow 배포
- dbt
- Spark
- Prometheus와 Grafana

## 학습 진행 원칙

- 한 번에 하나의 작은 작업만 진행한다.
- 핵심 데이터 모델, SQL, 변환 로직, 품질 규칙은 학습자가 먼저 초안을 작성한다.
- 환경설정과 반복적인 보일러플레이트는 자동화할 수 있지만, 생성한 파일의 역할을 설명한다.
- 테스트가 없는 기능은 완료된 것으로 간주하지 않는다.
- 구현하지 않은 기능을 완료된 것처럼 표시하지 않는다.
- 중요한 설계 결정은 ADR 또는 작업 기록으로 남긴다.

## 문서 계획

```text
docs/
├── adr/
├── runbooks/
├── data_quality_rules.md
├── event_schema.md
├── pipeline_runs.md
└── sql_analysis.md
```

문서 디렉터리는 필요한 시점에 생성합니다. 현재 README에는 계획만 기록합니다.
