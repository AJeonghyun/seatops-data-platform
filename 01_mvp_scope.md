# SeatOps 1차 MVP 범위

## 1. 해결하려는 문제

가상의 티켓팅 과정에서 발생한 이벤트를 원본 파일부터 분석 가능한 Mart까지 안정적으로 처리한다.

1차 MVP는 웹 서비스나 좌석 선점 API를 만들지 않는다. 대신 데이터 엔지니어링 파이프라인에서 자주 발생하는 다음 문제를 직접 다룬다.

- 원본 이벤트를 손실 없이 보존하는 방법
- 잘못된 이벤트를 정상 데이터와 분리하는 방법
- 같은 입력을 다시 처리해도 결과가 중복되지 않게 만드는 방법
- 오류 이벤트를 수정한 뒤 재처리 이력을 남기는 방법
- 파이프라인 각 단계의 입력, 성공, 실패, 중복 건수를 검증하는 방법

## 2. 핵심 시나리오

Python 이벤트 생성기가 정상 이벤트와 의도적인 오류 이벤트를 함께 만든다.

Airflow DAG는 JSON Lines Raw 파일을 PostgreSQL에 적재하고, Raw 계층의 payload는 원본 그대로 보존한다. 검증을 통과한 이벤트는 Staging 계층으로 이동하고, 검증에 실패한 이벤트는 오류 코드와 원인과 함께 Quarantine 계층에 저장한다. Staging 데이터는 일별·세션별 Mart로 집계된다.

같은 입력 파일과 같은 실행 날짜로 파이프라인을 다시 실행해도 Raw, Staging, Mart 결과가 중복 증가하지 않아야 한다. Quarantine 이벤트를 수정해 재처리할 때도 기존 처리 이력과 충돌하지 않아야 한다.

## 3. MVP에 포함할 기능

### 이벤트 생성

- 정상 티켓 이벤트 생성
- 필수 필드 누락, 잘못된 이벤트 타입, 중복 이벤트 등 의도적인 오류 이벤트 생성
- JSON Lines 파일 저장
- seed 기반 재현성 보장
- Python 단위 테스트

### PostgreSQL 데이터 모델링

- Raw, Staging, Quarantine, Mart 계층 역할 정의
- 각 테이블의 Grain 정의
- PK, Unique Key, FK, 인덱스 초안 작성
- 원본 payload 보존
- 중복 적재 방지

### 데이터 품질 검증

- 필수 필드 누락 검사
- 허용되지 않은 `event_type` 검사
- timestamp 형식과 허용 범위 검사
- 중복 `event_id` 검사
- 존재하지 않는 세션 또는 좌석 참조 검사
- 이벤트 순서 또는 상태 충돌 검사
- 지원하지 않는 `schema_version` 검사
- 오류 코드, 심각도, Quarantine 여부, 재처리 가능 여부 기록

### 파이프라인 자동화

- Docker Compose 기반 PostgreSQL과 Airflow 실행 환경
- Raw 적재 Task
- 품질 검증 Task
- Staging 변환 Task
- Mart 생성 Task
- Task 의존성 설정
- 실패 시 후속 Task 중단
- 재실행 시 멱등성 검증

### 재처리와 이력

- Quarantine 이벤트 수정 후 재처리
- 재처리 결과 중복 방지
- Pipeline Run 단위 이력 기록
- 단계별 입력, 성공, 실패, 중복 건수 기록
- 실패 원인과 해결 과정 문서화

### 테스트와 CI

- pytest 단위 테스트
- SQL 검증 쿼리
- 중복 실행 테스트
- 잘못된 입력 테스트
- 부분 실패와 재시작 테스트
- GitHub Actions 기반 자동 테스트

## 4. 구현하지 않을 기능

다음 기능은 1차 MVP에서 제외한다.

- FastAPI 기반 티켓팅 API
- 좌석 선점 요청 API
- 실제 동시성 제어
- 좌석 상태 머신 중심 서비스
- Transactional Outbox
- Kafka 또는 실시간 스트리밍
- Spark 기반 분산 처리
- Kubernetes
- Terraform
- 클라우드 배포
- Prometheus와 Grafana 대시보드
- 실제 티켓 사이트 UI 복제
- 실제 티켓 사이트 자동 접속
- 결제 시스템
- 보안문자 우회

서비스·스트리밍·운영 기술은 1차 MVP가 끝난 뒤, 현재 구조만으로 해결하기 어려운 한계가 확인될 때 확장 후보로 검토한다. 실제 티켓 사이트 UI 복제·자동 접속, 결제 시스템, 보안문자 우회는 확장 계획에도 포함하지 않는다.

## 5. 성공 기준

1차 MVP는 다음 결과가 확인될 때 완료로 본다.

- 같은 seed로 같은 JSON Lines 입력 파일을 재현할 수 있다.
- Raw 계층에 원본 이벤트 payload가 보존된다.
- 동일 Raw 파일을 두 번 적재해도 중복 데이터가 증가하지 않는다.
- 검증을 통과한 이벤트만 Staging 계층에 저장된다.
- 검증에 실패한 이벤트가 Quarantine 계층에 오류 코드와 원인으로 저장된다.
- Quarantine 이벤트를 수정하고 재처리해도 중복이 발생하지 않는다.
- Mart에서 일별·세션별 주요 지표를 SQL로 조회할 수 있다.
- Pipeline Run 이력에서 입력, 성공, 실패, 중복 건수를 확인할 수 있다.
- 정상 입력, 오류 입력, 중복 실행, 부분 실패, 재처리 테스트가 pytest로 검증된다.
- GitHub Actions에서 테스트가 자동 실행된다.
- README의 완료 표시는 실제 코드, 테스트, 실행 결과와 연결된다.

## 6. 단계별 진행 순서

### Phase 1: Python·SQL 복구와 이벤트 생성

목표는 이벤트 스키마 초안을 직접 설계하고, 정상 이벤트와 오류 이벤트를 JSON Lines로 재현 가능하게 생성하는 것이다.

완료 증거:

- 이벤트 생성 코드
- JSON Lines 샘플
- seed 재현성 테스트
- 필드 의미 설명 기록

### Phase 2: PostgreSQL 데이터 모델링과 적재

목표는 Raw 계층에 원본을 보존하고, 같은 파일을 다시 적재해도 중복이 늘지 않게 만드는 것이다.

완료 증거:

- 계층별 Grain 정의
- DDL
- Raw 적재 코드 또는 SQL
- 중복 적재 방지 테스트
- 적재 결과 검증 SQL

### Phase 3: 데이터 품질과 변환

목표는 오류 이벤트를 규칙 기반으로 탐지하고, 정상 데이터와 Quarantine 데이터를 분리하는 것이다.

완료 증거:

- 품질 규칙 명세
- 검증 로직
- 품질 규칙 단위 테스트
- Staging 및 Quarantine 검증 SQL

### Phase 4: Airflow 파이프라인

목표는 적재, 검증, 변환, Mart 생성을 하나의 DAG로 자동화하는 것이다.

완료 증거:

- Docker Compose 실행 환경
- Airflow DAG
- Task 의존성
- 실패 로그 확인 방법
- DAG 재실행 멱등성 검증

### Phase 5: 재처리·테스트·CI

목표는 Quarantine 재처리와 통합 테스트, CI를 완성하고 결과 중심 README로 정리하는 것이다.

완료 증거:

- Quarantine 재처리 절차
- Pipeline Run 이력
- 통합 테스트
- GitHub Actions 실행 결과
- 실패 시나리오 기록
- README 결과 링크

## 7. 2차 확장 기준

1차 MVP가 끝난 뒤 서비스 이벤트 수집이 필요해질 때 다음을 검토한다.

- FastAPI
- 좌석 선점 API
- PostgreSQL 동시성 제어
- Transactional Outbox
- Outbox Worker
- Worker 장애와 복구
- Locust 부하 테스트

배치 처리의 한계가 확인되면 Kafka, 실시간 Consumer, 중복 메시지 처리, Consumer 재시작, Schema evolution을 스트리밍 확장 후보로 검토한다.

도입 전에는 반드시 해결하려는 한계와 SQL 또는 배치 파이프라인만으로 가능한 대안을 먼저 기록한다.

## 8. 3차 확장 기준

데이터 크기, 운영 배포, 관측성 측면의 한계가 확인되면 다음을 검토한다.

- AWS S3
- AWS RDS
- MWAA 또는 Airflow 배포
- dbt
- Spark
- Prometheus와 Grafana

3차 확장은 1차 MVP의 테스트와 재처리 흐름이 안정화된 뒤에만 진행한다.
