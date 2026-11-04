# Work Manager

한 팀(관리자 1명 + 팀원)이 TODO, 이슈, 배포일정, 연차를 관리하고 팀 슬랙 채널로 알림을 받는 업무 관리 도구.
유지보수 업무가 많아서 프로젝트(시스템 단위) > 업무 > TODO 구조로 일을 묶는다. 요청의 원본은 전사 도구 "플로우"에 있고, 이 도구는 처리 기록을 남긴다.

현재 단계: **기획 완료, 코드 없음.** 다음은 모노레포 뼈대(Spring Boot + React + Cucumber-JVM).

## 작업 방식: 명세 주도 개발 (SDD + BDD)

출처: Jaroslaw Wasowski, "SDD Writing Specifications for AI: BDD as the Missing Link" (Level Up Coding). 상세 규칙은 [docs/sdd-workflow.md](docs/sdd-workflow.md).

- **명세가 실행 계약이다.** `features/*.feature`가 기준이고, 코드는 시나리오를 통과시키기 위해 쓴다. 시나리오에 없는 동작은 만들지 않는다.
- **바꿀 때는 위에서 아래로**: 결정 기록 → PRD/권한 → 용어집 → 시나리오 → 검사 → ERD → 코드. 코드부터 고치지 않는다.
- **시나리오는 용어집의 표준 문장만 쓴다.** 새 문장은 [docs/glossary.md](docs/glossary.md) 6장 카탈로그에 먼저 추가한다.
- **구현은 시나리오 하나씩**: Step Definition 작성 → 실패 확인 → 최소 구현 → 통과 → 정리 → 다음 시나리오.
- 사람이 정할 일(범위, 정책, 권한)은 임의로 정하지 말고 묻는다. 정한 것은 [docs/open-questions.md](docs/open-questions.md)에 남긴다.

## 문서 지도

| 문서 | 내용 |
|---|---|
| [docs/PRD.md](docs/PRD.md) | 문제, 역할, 기능, 단계, 범위 밖 |
| [docs/open-questions.md](docs/open-questions.md) | 결정 사항과 미결 항목 (결정의 근거는 여기서 찾는다) |
| [docs/permissions.md](docs/permissions.md) | 관리자/팀원 권한 표, 비활성화 정책 |
| [docs/glossary.md](docs/glossary.md) | 용어 ↔ 코드명, 값 형식, 화면 이름, 시나리오 작성 규칙, 표준 문장 카탈로그 |
| [docs/erd.md](docs/erd.md) | 테이블, 제약, 핵심 설계 결정 |
| [docs/sdd-workflow.md](docs/sdd-workflow.md) | 명세 계층, 변경 순서, 구현 루프, 완료 기준 |
| `features/*.feature` | 한국어 Gherkin 시나리오 (`# language: ko`) |

## 명령

```bash
python3 scripts/check_steps.py           # 모든 단계가 카탈로그 문장인지 검사 (실패 시 exit 1)
python3 scripts/check_steps.py --stats   # 문장별 사용 횟수
```

## 기술 결정

- Backend: Java 21, Spring Boot 3, Spring Data JPA, MySQL 8 (로컬은 Docker), Flyway, 서버 세션
- Frontend: React + TypeScript (Vite)
- 인수 테스트: Cucumber-JVM, 한국어 Gherkin
- 단일 레포: `backend/`, `frontend/`, `docs/`, `features/`, `scripts/`

## 놓치기 쉬운 규칙

- 관리자는 **정확히 1명**이고 위임으로만 바뀐다. DB의 UNIQUE 생성 컬럼으로 보장한다 ([docs/erd.md](docs/erd.md) 3.1).
- 모든 업무 데이터는 팀 전체 공개. 수정과 삭제는 **본인이 만든 것만**, 관리자도 예외 없음.
- TODO는 작성자 = 수행자. 다른 사람에게 할당하지 않는다.
- TODO, 이슈, 배포의 연결은 **업무 / 프로젝트만 / 없음** 중 하나. 업무를 고르면 프로젝트는 자동이고 따로 바꿀 수 없다.
- 시간은 `Clock`, 무작위는 `RandomGenerator`, 슬랙은 인터페이스로 주입한다. 테스트가 시간을 움직일 수 있어야 한다.
- 시각은 UTC로 저장하고 `Asia/Seoul`로 표시한다. 날짜 값은 `DATE`.

## 커밋

- 형식: `<type>: <description>` (feat, fix, refactor, docs, test, chore, perf, ci)
- 사용자와는 한국어로 소통한다. 코드 식별자와 기술 용어는 원어 그대로 쓴다.
