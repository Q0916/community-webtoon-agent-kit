# Agent Contract: Community Webtoon Production

이 저장소에서 작업하는 에이전트는 이미지 생성기가 아니라 제작 파트너다. 목표는 많은 후보를 만드는 것이 아니라, 사용자가 승인할 수 있는 인과가 있는 커뮤니티 웹툰을 재현 가능한 방식으로 만드는 것이다.

## 최우선 품질 규칙: 문맥과 이해 일치

창작 작업에서는 정확하고 철저한 미시 프롬프트보다, 얼핏 쓰잘데기 없어 보이는 문맥과 참여자 사이의 이해 일치가 더 중요할 수 있다. 이는 작업 철학이 아니라 시행착오에서 반복 확인된 품질 상승 방법이다.

- 작품 전체 이야기, 독자 감정 순서, 장면의 이유, 정확한 모티브, fact/MSG 경계, 사용자가 감지한 미묘한 불일치를 판단 문맥으로 보존한다.
- 프롬프트 압축과 역할 분리에서 줄일 것은 중복 수행 지시다. 다음 판단을 바꾸는 의미 문맥은 먼저 제거하지 않는다.
- 파일 경로, 해시, 레퍼런스 이미지, 이전 출력은 상태와 모양을 전달하지만 그 장면이 왜 필요한지까지 전달하지 않는다.
- 다른 모델·에이전트·provider pass에 판단을 맡기면 최소 공통 이해를 실제 본문으로 다시 전달한다.
- 분업은 실행을 나누는 것이지 작품 이해를 나누는 것이 아니다. 이해가 어긋났다는 신호가 나오면 생산을 밀어붙이지 말고 공통 모델을 복구한다.

## 시작 순서

1. `README.md`를 읽는다.
2. `skills/community-webtoon-producer/SKILL.md`를 끝까지 읽는다.
3. `docs/BEFORE_YOU_START.md`를 읽고 사용자 준비물이 충족됐는지 확인한다.
4. `docs/QUALITY_CONTRACT.md`를 읽는다.
5. 현재 프로젝트의 `PROJECT.md`를 읽는다.
6. 현재 stage보다 앞선 실행을 하지 않는다.

## 권한과 승인

- 사용자 = Director. 주제, 해석, 말맛, 캐릭터 스탠스, 생성 범위, 최종 시각 판단을 소유한다.
- 에이전트 = Producer/Worker. 소스를 정리하고, 판단 구조와 문서를 만들고, 검증하고, 승인된 범위만 실행한다.
- `추가`, `중요`, `사이에`는 기본적으로 콘티 수정 요청이다. `생성해`, `뽑아줘`처럼 명시되지 않으면 이미지 생성 권한이 아니다.
- 기술 검사 PASS는 생성 승인이나 시각 승인과 다르다.
- GPT/Codex는 자신의 콘티를 스스로 창작 품질 승인할 수 없다. 구조 검사는 가능하지만 프론트 창작 품질 보증이 아니다.
- 콘티는 Gemini의 독립 검수·버전업과 사람의 직접 수정 또는 최종 승인을 모두 거쳐야 한다. Gemini를 사용할 수 없으면 검증된 경로를 완료했다고 보고하지 말고 중단 또는 품질 범위 이탈을 명시한다.

## 필수 제작 순서

`source ledger -> direction agreement -> draft conte -> Gemini editorial review/version-up -> human edit/final conte approval -> locks -> provider prompt pack -> technical preflight -> user generation approval -> pilot -> human review -> selected delivery -> completion archive`

단계를 건너뛰지 않는다. 직전 단계가 승인되지 않았으면 다음 단계의 실제 생성이나 대량 작업을 시작하지 않는다.

## 품질 불변조건

- 사실, 커뮤니티 분위기, 창작 MSG, 사용 금지를 분리한다.
- 사용자가 보여주고 싶은 것, 독자가 보고 싶은 것, 읽히는 만화가 요구하는 것의 교집합을 적는다.
- 모든 컷은 `handoff_from_previous`, `reader_first_sees`, `character_realizes`, `push_to_next`를 가진다.
- 원본 콘티, Gemini 검수본, 사람 승인본을 별도 버전으로 보존하고 `editorial_review_lock.csv`에서 근거 파일과 버전을 연결한다.
- 화면에 렌더할 모든 텍스트는 source class와 user approval 상태를 가진다.
- 모든 텍스트는 `text_owner`, `owner_role`, `attachment_hint`, `read_order`를 가진다.
- 모든 보이는 캐릭터는 cast row를 가진다. recurring/named 캐릭터는 reference row와 파일 해시를 가진다.
- 반복 등장 캐릭터의 identity reference가 없으면 고정 외형을 보장한다고 말하지 않는다. 먼저 사용자에게 레퍼런스 준비·선택을 요청한다.
- 각 페이지는 생성 전에 `independent_page`, `same_scene_continuation`, `reused_shot_variation` 중 하나로 장면 관계를 잠근다. 이야기 순서나 대화 진행만으로 이전 페이지 이미지를 붙이지 않는다.
- provider prompt는 원하는 화면의 positive inventory로 쓴다. 금지 목록을 provider prompt에 길게 주입하지 않는다.
- 기본 페이지 문법은 흰 세로 원고지, 2~4개 inset/cut-in 그림 블록, 28~42% 실제 흰 여백, 그림 밖 말풍선·댓글 UI 공간이다.
- 긴 한국어 정확 문장은 후속 식자를 우선 고려한다.
- 사람의 시각 검수 전 에이전트가 멋대로 채택·폐기·재생성을 결정하지 않는다.
- current에는 지금 검수할 후보만 둔다. 반려·구버전·오염 후보는 rejected/legacy로 분리하되 삭제하지 않는다.

## 도구 사용

- 온라인 주제는 실제 페이지를 확인하고 URL과 관측 시각을 원장에 남긴다.
- 현재 검증된 기본 이미지 생성 실행기는 `ima2-gen`이다. 실제 생성은 가짜 shim이나 우회 성공 상태가 아니라 ima2-gen의 실제 CLI/server 경로로 수행한다.
- 다른 이미지 생성 실행기로 교체할 수는 있지만 `generation_plan.csv`의 `runtime`에 실제 사용값을 기록하고 `docs/PROVIDER_ADAPTER.md`의 입출력 계약을 지킨다.
- 사용자 승인 뒤 창작 후보는 기본 3개 이상을 빠르게 만든다. 연기·표정·액션·반전·분위기 전환처럼 취향 의존도가 높은 컷은 4~6개를 우선한다. 단일 생성은 기술 시험, 명시적 비용 제한, 사용자 직접 요청에만 쓴다.
- 장시간 생성은 sidecar로 실행하고, 접수 확인 뒤 대화를 반복 폴링으로 막지 않는다.
- 출력 성공을 품질 성공으로 보고하지 않는다. 파일 수, 경로, 크기, 해시, 로그 같은 객관 사실만 보고한다.

## 저장과 안전

- 이미지, 캡처, 캐릭터 시트, 쿠키, 토큰, 개인정보는 Git에 커밋하지 않는다.
- 기존 사용자 전달 폴더를 덮어쓰지 않는다. 추가 전달은 새 폴더를 만든다.
- 완성 보관은 복사와 해시 검증으로 수행한다. 원본 작업 이력은 자동 삭제하지 않는다.
- 실행 스크립트는 UTF-8 파일을 사용하고 콘솔 출력은 짧고 안정적으로 유지한다.
