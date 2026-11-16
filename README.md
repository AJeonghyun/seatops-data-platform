# SeatOps — 클라우드 엔지니어 학습 프로젝트

가상의 티켓 이벤트를 생성·수집·검증·집계하는 SeatOps를 **직접 하나씩 구현하며** Python·SQL과 AWS 인프라·운영 기술을 익히는 프로젝트입니다.

이 저장소는 현재 **개발 계획과 사전 진단 풀이 단계**입니다. 이벤트 생성기, DB 파이프라인, Docker, Terraform, CI, AWS 배포는 아직 구현되지 않았습니다. 아래 문서의 구성도·파일명·검증 명령은 앞으로 구현할 설계 후보와 목표입니다.

## 이번 목표

기존 Airflow 중심 계획을 **SeatOps 로컬 완성 → AWS 배포·운영 학습의 두 페이즈**로 조정합니다. 기존 2주는 참고 일정이며, 1페이즈 완료 후 2페이즈 날짜를 정합니다. 이벤트 생성, JSONL 원본, PostgreSQL Raw/Staging/Quarantine/Mart, 품질 검증, 멱등성·재처리라는 기존 주제는 유지합니다.

AWS EC2·S3·IAM·VPC·CloudWatch와 Terraform을 학습 범위에 넣고, Airflow 전체 DAG·RDS·Kafka·Spark·Kubernetes는 후속 단계로 미룹니다. 복잡한 웹 UI·예약 API·실제 결제는 이번 범위에 넣지 않습니다.

## 두 페이즈 — 아직 미구현

| 구분 | Phase 1: SeatOps 만들기 | Phase 2: 배포하며 배우기 |
|---|---|---|
| 입력 | 로컬 JSONL | S3 원본 |
| 핵심 작업 | 생성·적재·검증·집계·중복 방지·수정 재처리 | EC2 배포·IAM·VPC·Terraform·CloudWatch |
| 실행·검증 | 로컬 PostgreSQL/Compose, pytest, 기본 CI, 실패·재시작 실험 | 검증한 이미지로 AWS 실행, 인프라 CI, AWS 복구 실험 |
| 완료 결과 | AWS 없이 동작하고 본인이 설명할 수 있는 SeatOps 로컬 MVP | AWS에서도 동작·보안·로그·복구를 확인한 운영 환경 |

**Phase 1 완료 전에는 AWS 구현을 시작하지 않습니다.** 로컬 Docker는 서비스 실행 환경을 맞추는 용도입니다. Phase 2에서는 핵심 처리 로직을 재사용하고 S3 연결과 배포·운영 설정을 추가합니다.

```text
Phase 1: Python 생성 → 로컬 JSONL → PostgreSQL Raw
                                      ├─ Staging → Mart
                                      └─ Quarantine → 수정·재처리
         + 로컬 로그 / 테스트 / Compose / 기본 CI

Phase 2: 위 서비스를 EC2에서 실행 + S3 원본 연결
         + VPC / IAM / Terraform / CloudWatch / AWS 복구 검증
```

## 학습 방식

**AI가 프로젝트를 완성해 주는 방식으로 진행하지 않습니다.**

1. 필요한 개념과 실제 사용 이유를 짧게 복습합니다.
2. 한 번에 60~90분짜리 과제 하나만 진행합니다.
3. 학습자가 설계 초안과 핵심 코드를 먼저 작성합니다.
4. AI는 정답으로 교체하기 전에 문제점·위험·힌트를 제공합니다.
5. 학습자가 수정하고 테스트 결과와 개념 질문 답을 제출합니다.
6. 완료 조건을 확인한 뒤에만 다음 과제로 넘어갑니다.

핵심 데이터 모델·SQL·검증·변환 로직은 학습자가 먼저 작성합니다. 전체 예시는 두 번 이상 막혔거나 명시적으로 요청했을 때만 제공합니다. 환경설정도 필요한 단계에서 최소한만 돕고 파일 역할을 설명합니다. 일정이 늦어지면 날짜를 조정하며 AI 대행으로 완료 체크를 채우지 않습니다.

## 현재 파일과 구현 상태

| 항목 | 실제 상태 |
|---|---|
| `preview_test.py` | 학습자가 작성한 Python 이벤트 분류 진단 풀이. 프로젝트 생성기/품질 파이프라인은 아님 |
| `README.md`, `01_mvp_scope.md` | 목적·범위·진행 원칙 |
| `docs/PHASE1_DAILY_PLAN.md` | Phase 1 최신 일별 계획: 하루 60~90분, 10주·50학습일 체크리스트 |
| `docs/MVP_2WEEK_PLAN.md` | 두 페이즈 목표·완료 조건의 기존 개요 |
| `docs/AWS_ARCHITECTURE.md` | 목표 아키텍처·학습자가 결정할 설계 항목 |
| `docs/MVP_ACCEPTANCE_CRITERIA.md` | 향후 구현과 학습 이해도를 확인할 기준 |
| 파이프라인·Docker·Terraform·CI·AWS 배포 | 미구현 |

과제 열람용 SeatOps 학습 사이트는 별도 학습 도구이며 플랫폼 구현 증거가 아닙니다.

## 계획 문서

- **[Phase 1 하루씩 학습 체크리스트 — 여기부터 시작](docs/PHASE1_DAILY_PLAN.md)**
- [현재 MVP 범위](01_mvp_scope.md)
- [두 페이즈 학습·구현 계획](docs/MVP_2WEEK_PLAN.md)
- [AWS 아키텍처 초안과 결정할 질문](docs/AWS_ARCHITECTURE.md)
- [완료 조건과 검증 기준](docs/MVP_ACCEPTANCE_CRITERIA.md)

## 진행 시작점

“첫째 날 뭐 해야 해?”라고 물으면 [일별 계획의 Day 01](docs/PHASE1_DAILY_PLAN.md#day-01--기존-코드를-실행하고-이벤트-한-개-찾기)을 기준으로 기존 `preview_test.py`의 입력·함수·출력을 함께 읽습니다. 설명 → 작은 실습 → 직접 작성 → 검증 순서로 한 과제만 진행합니다. 진단은 시작을 막는 시험이 아니며, 모르는 개념은 필요한 시점에 설명합니다.

일별 계획은 하루 60~90분·주 5회이며 매주 다섯째 날은 복습·미완료 과제 보완입니다. 현재 진도는 일별 계획의 ‘현재 진도 기록’에 남깁니다. 기능·SQL·DDL·테스트 정답을 미리 생성하지 않고, 실제 실행 결과와 본인의 설명을 확인한 뒤 다음 Day로 넘어갑니다.

실제 AWS 리소스 생성과 비용 발생 작업은 사용자가 비용·대상 계정을 확인하고 승인한 뒤에만 진행합니다. Access Key·비밀번호·Terraform state는 Git에 올리지 않습니다.
