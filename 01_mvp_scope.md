# SeatOps 현재 MVP 범위 — 학습 계획

상태: **계획**. 이 문서는 구현 완료 보고가 아닙니다.

## 목표와 변경 이유

가상의 티켓 이벤트를 원본부터 분석 마트까지 처리하는 작은 시스템을 직접 만들고, AWS에서 배포·권한·로그·복구를 설명할 수 있게 됩니다.

기존 목표는 Airflow 중심 데이터 엔지니어링이었습니다. 현재 목표는 신입 클라우드 엔지니어 학습이므로 우선순위를 다음처럼 조정합니다.

| 기존 항목 | 현재 계획 | 이유 |
|---|---|---|
| Python·SQL·JSONL·Raw/Staging/Quarantine/Mart | 유지 | 운영할 실제 작업과 데이터 흐름이 필요 |
| 품질 검증·중복 방지·재처리·pytest | 유지 | 정상 실행 외 실패와 복구를 입증 |
| Docker Compose·GitHub Actions | 유지 | 실행 환경과 변경 검증을 재현 |
| Terraform·AWS 클라우드 배포 | Phase 2로 이동 | 클라우드 네트워크·권한·IaC를 직접 익힘 |
| Airflow 전체 DAG | 후속 단계 | 우선 배치 CLI 하나의 실행·복구부터 이해 |
| PostgreSQL RDS | 후속 단계 | 초기에는 EC2 Compose로 비용·복잡도 축소 |
| API·Outbox·Kafka·Spark·Kubernetes | 후속 검토 | 현재 한계가 확인될 때만 추가 |

## 두 페이즈의 경계

1. **SeatOps 자체 완성:** AWS 없이 로컬 파일→Raw→Staging/Quarantine→Mart를 구현한다. 중복 방지·수정 재처리·실행 이력·로컬 로그·테스트·Docker Compose·기본 CI까지 완료하고 본인이 설명한다.
2. **완성한 SeatOps 배포:** 1페이즈를 통과한 후 EC2·S3·IAM·VPC·Terraform·CloudWatch를 배우며 같은 서비스를 배포한다. 인프라 CI와 AWS 환경 복구 검증을 추가한다.

서비스 핵심 기능의 미완료분을 AWS 단계로 넘기지 않는다. 최초 2주 일정은 참고이며 1페이즈가 끝나야 2페이즈의 실제 날짜를 정한다. 현재 두 페이즈 모두 미완료다.

## 필수 목표 — 모두 향후 구현

- [ ] 같은 seed와 기준 날짜로 재현 가능한 티켓 이벤트를 만든다.
- [ ] 정상·오류 이벤트를 JSONL로 저장한다.
- [ ] 원본을 S3에 업로드하고 EC2에서 읽는다.
- [ ] PostgreSQL Raw에 원본을 보존한다.
- [ ] 정상은 Staging, 오류는 이유와 함께 Quarantine으로 분리한다.
- [ ] 일별 이벤트 수와 좌석 선점 성공률을 Mart에서 조회한다.
- [ ] 같은 입력을 다시 처리해도 중복이 증가하지 않는다.
- [ ] 오류를 수정하고 원본·재처리 이력을 추적한다.
- [ ] Docker Compose로 앱과 DB를 실행한다.
- [ ] Terraform으로 VPC·EC2·IAM·S3·CloudWatch를 정의한다.
- [ ] CI에서 테스트·이미지 빌드·Terraform 검증을 실행한다.
- [ ] 로그와 처리 건수를 기록하고 실패·재시작·복구를 검증한다.

테스트 없는 기능은 완료로 표시하지 않습니다. 실제 AWS 확인 전에는 로컬 성공을 AWS 성공으로 표시하지 않습니다.

## 직접 설계할 내용

여섯 이벤트는 기존 후보를 사용합니다: SESSION_STARTED, SEAT_VIEWED, SEAT_HOLD_ATTEMPTED, SEAT_HOLD_SUCCEEDED, SEAT_HOLD_FAILED, SESSION_ENDED.

`event_id`, `event_type`, `occurred_at`, `session_id`, `user_id`, `seat_id`, `request_id`, `payload`, `schema_version`는 필드 후보입니다. 각 필드의 의미·필수 여부·타입을 학습자가 먼저 제안합니다.

Raw/Staging/Quarantine/Mart/실행 이력은 역할 후보입니다. **Grain → 컬럼 → PK/Unique/FK → 검증 SQL** 순서로 초안을 작성합니다. 중복 식별 키, 원본 보존 방법, 수정 이력, Mart 분모는 완성된 답으로 제공하지 않습니다.

품질 규칙은 필수값·이벤트 유형·timestamp·버전·중복부터 작게 시작합니다. 각 규칙의 ID·대상·실패 조건·오류 코드·심각도·격리 여부·재처리 가능 여부·테스트를 직접 정의합니다. 세션/좌석 참조와 상태 순서 검사는 기본 흐름 이후 시간 여유와 필요성을 검토합니다.

## 범위 밖

이번에는 복잡한 웹 UI, 사용자 인증, 실제 예약·결제, 마이크로서비스, Kafka/Spark, Kubernetes/EKS, Multi-AZ HA, RDS, 관리형 Airflow, 전체 Airflow DAG를 구현하지 않습니다. ECR/OIDC 자동 CD도 필수 흐름이 안정된 뒤 선택 과제로 다룹니다.

## 진행 원칙

한 번에 작은 과제 하나를 수행합니다. 설명 → 직접 작성 → 힌트 중심 리뷰 → 테스트 → 개념 확인 순서를 지킵니다. 핵심 코드를 AI가 미리 만들지 않습니다. 본인의 결정은 해당 단계에서 ADR 또는 작업 기록으로 남깁니다. 2주는 목표 일정이며 이해·검증이 끝나지 않으면 후속 날짜를 옮깁니다.
