# SeatOps — 클라우드 엔지니어 학습 프로젝트

가상의 티켓 이벤트를 생성·수집·검증·집계하는 SeatOps를 **직접 하나씩 구현하며** Python·SQL과 AWS 인프라·운영 기술을 익히는 프로젝트입니다.

이 저장소는 현재 **개발 계획과 사전 진단 풀이 단계**입니다. 이벤트 생성기, DB 파이프라인, Docker, Terraform, CI, AWS 배포는 아직 구현되지 않았습니다. 아래 문서의 구성도·파일명·검증 명령은 앞으로 구현할 설계 후보와 목표입니다.

## 이번 목표

기존 Airflow 중심 계획을 **클라우드 엔지니어 취업을 위한 2주 MVP 학습 계획**으로 조정합니다. 이벤트 생성, JSONL 원본, PostgreSQL Raw/Staging/Quarantine/Mart, 품질 검증, 멱등성·재처리라는 기존 주제는 유지합니다.

AWS EC2·S3·IAM·VPC·CloudWatch와 Terraform을 학습 범위에 넣고, Airflow 전체 DAG·RDS·Kafka·Spark·Kubernetes는 후속 단계로 미룹니다. 복잡한 웹 UI·예약 API·실제 결제는 이번 범위에 넣지 않습니다.

## 목표 흐름 — 아직 미구현

```text
Python 이벤트 생성 → JSONL → S3
                             ↓
                     EC2 / Docker 배치
                             ↓
                       PostgreSQL Raw
                        ├─ Staging → 일별 Mart
                        └─ Quarantine → 수정·재처리

Terraform: VPC / EC2 / IAM / S3 / CloudWatch 구성
GitHub Actions: 테스트 / 이미지 빌드 / Terraform 검증
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
| `docs/MVP_2WEEK_PLAN.md` | 10영업일 목표 및 작은 과제 순서 |
| `docs/AWS_ARCHITECTURE.md` | 목표 아키텍처·학습자가 결정할 설계 항목 |
| `docs/MVP_ACCEPTANCE_CRITERIA.md` | 향후 구현과 학습 이해도를 확인할 기준 |
| 파이프라인·Docker·Terraform·CI·AWS 배포 | 미구현 |

과제 열람용 SeatOps 학습 사이트는 별도 학습 도구이며 플랫폼 구현 증거가 아닙니다.

## 계획 문서

- [현재 MVP 범위](01_mvp_scope.md)
- [2주 학습·구현 계획](docs/MVP_2WEEK_PLAN.md)
- [AWS 아키텍처 초안과 결정할 질문](docs/AWS_ARCHITECTURE.md)
- [완료 조건과 검증 기준](docs/MVP_ACCEPTANCE_CRITERIA.md)

## 진행 시작점

새 코드를 대량 생성하지 않고 기존 `preview_test.py`의 풀이와 남은 진단 결과부터 확인합니다. 진단으로 이미 아는 내용은 건너뛰고 부족한 개념만 복습한 뒤 첫 구현 과제를 정합니다. 각 과제는 ‘이번 작업 / 필요한 개념 / 내가 먼저 결정할 것 / 구현 과제 / 완료 조건 / 검증 방법 / 개념 확인 질문 / 다음 단계 조건’ 형식으로 제공합니다.

실제 AWS 리소스 생성과 비용 발생 작업은 사용자가 비용·대상 계정을 확인하고 승인한 뒤에만 진행합니다. Access Key·비밀번호·Terraform state는 Git에 올리지 않습니다.
