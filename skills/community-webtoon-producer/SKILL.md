---
name: community-webtoon-producer
description: Use when turning an online community post, forum incident, meme thread, live gallery mood, or user-supplied issue into a short Korean vertical info-gag webtoon; includes source collection, fact-mood-MSG separation, sweet-spot approval, causal storyboard packets, cast-text-reference locks, ima2-gen-first generation preflight, human review, and completion archiving.
---

# Community Webtoon Producer

## Objective

온라인 커뮤니티 반응을 임의로 지어내지 않고, 전편·장면·컷의 인과와 말맛을 살려 읽히는 한국어 세로형 정보·개그 웹툰을 제작한다. 기술적 생성 성공이나 검사 통과를 사용자의 창작·시각 승인과 혼동하지 않는다.

## Primary Quality Rule

공유된 맥락과 이해 일치를 단순한 대화 예절이 아니라 핵심 제작 입력으로 다룬다. 아무리 정교한 미시 프롬프트라도 작품 전체의 이유(WHY), 독자의 감정 순서, 핵심 모티브, 사실과 MSG의 경계, 사용자가 짚어낸 어색함이 빠지면 좋은 결과를 복원할 수 없다.

당장 실행할 명령과 직접 관계없어 보이는 맥락이라도 창작·연출 판단을 바꾼다면 보존한다. 다른 모델이나 다음 생성 패스에 판단을 넘길 때는 전체 흐름·현재 구간·앞뒤 상태·정확한 대사·WHY를 실제 본문에 다시 적어 전달한다. 파일 경로, 해시, 레퍼런스, 이전 이미지는 상태와 외형을 증명할 뿐 왜 그렇게 보여야 하는지 설명하지 못한다.

이 원칙은 프롬프트만 다듬어 실패했던 시행착오를 거쳐 반복 확인된 품질 기준이다. 가설을 검증된 모델 내부 기제처럼 과장하지 않고, 목적·이유·실패 배경·예시를 살려 전달한다.

## First Read

새 작품은 `docs/WORKFLOW.md`와 이번 작업 경로에서 쓰는 단계별 매뉴얼을 처음부터 끝까지 읽고 작품의 `PRODUCTION_CHECKLIST.md`를 만든다. 각 단계 진입 시 해당 매뉴얼·예시와 직전 결과를 읽고, 종료 시 실제 원고·입력·결과에서 적용 여부를 확인해 갱신한 뒤 다음 단계 문서를 읽는다. 유효한 통과 증거는 재사용한다. AGY에는 내부 체크리스트를 넘기지 않고 짧은 자연어와 실제 자료를 전달한다.

저장소 루트에서 다음 문서를 먼저 읽는다.

1. `AGENTS.md`
2. `docs/BEFORE_YOU_START.md`
3. `docs/QUALITY_CONTRACT.md`
4. 현재 프로젝트의 `PROJECT.md`

창작 협업과 퇴고·편집·전달을 위해 `docs/CREATIVE_ROLES.md`, `docs/CREATIVE_CONTINUITY.md`, `docs/CRAFT_REVIEW.md`, `docs/CUT_BASED_PRODUCTION.md`, `docs/PANEL_LAYOUT_REVISION.md`, `docs/PANELING_AND_PACING.md`, `docs/UPLOAD_DELIVERY.md`를 읽고, 관련 전문 판단과 WHY·현재 위임 범위를 실제 요청 본문에 담는다. 소재를 본격 제작으로 옮길 준비가 되면 `harness/scripts/init_project.py`로 프로젝트를 초기화한다.

공개 저장소(`Q0916/community-webtoon-agent-kit`)는 Python 3.10+ 표준 라이브러리 기반의 `init_project.py`, `validate_project.py`, `provider_instruction_integrity.py`, `freeze_completion.py`, `verify_repository.py`를 제공한다. 생성 실행기(`ima2-gen`), 누적 receipt, 컷 시트 분리·재배치, 업로드 무손실 분할 및 용량·높이 검사 도구는 공개 키트에 포함되지 않으므로 사용자가 별도로 준비한 환경을 사용한다.

## Required Workflow

1. 원문 게시글과 주변 반응 샘플을 수집하고 URL과 관측 시각을 기록한다.
2. `source_ledger.md`에서 `primary_fact`, `mood_source`, `MSG`, `do_not_use`를 분리한다.
3. Director의 의도, 커뮤니티 독자의 기대, 웹툰 호흡이 만나는 지점(sweet spot)을 논의하고 승인받는다.
4. Director/Producer의 거친 장면 뼈대나 기획 원안을 보존한다. 빈칸 채우기를 맡길 때는 의도된 빈칸을 미리 메우지 않고, 자유 집필이나 완성문 퇴고를 맡길 때는 사용자의 위임 범위를 그대로 따른다.
5. 원안과 전체 소스·사실/MSG 경계·WHY를 Gemini(AGY)에게 전달해 집필·연출 패스를 받는다. Gemini 원출력은 원안 옆에 별도 파일로 그대로 보존하며 덮어쓰지 않는다.
6. 수정하거나 재작성을 요청하기 전에 AGY 원출력을 Director에게 먼저 그대로 보여준다. 검토 의견은 분리해 기록하고 제안별로 `adopt`, `adapt`, `reject`를 정리한 뒤 합의된 범위만 수정한다. 초안 확정 후 편집·배치·식자·생성 준비는 Codex가 맡고, AGY 재참여는 사용자의 새 요청이 있을 때만 진행한다.
7. 채택된 결과를 바탕으로 **전편(감정·인과·보상) → 장면 연결 → 컷 설계** 순서로 작법 퇴고를 수행해 하나의 canonical 콘티로 정리한다(`docs/CRAFT_REVIEW.md`). 무엇을 왜 유지·수정했는지는 기존 콘티 메모에 남기며 매 컷 새 보고서나 승인 절차를 추가하지 않는다. 모든 컷에 `handoff_from_previous`, `reader_first_sees`, `character_realizes`, `push_to_next`를 부여하고 인과가 선명해진 뒤에 불필요한 밀도를 덜어낸다.
8. 사람이 canonical 콘티를 읽고 필요시 직접 수정한 뒤 명시적으로 승인한다. 원 뼈대, Gemini 원출력, 공동 검토, 사람 승인 canonical 버전과 해시를 `editorial_review_lock.csv`에 기록한다.
9. 사람 승인 콘티를 안정된 ID를 가진 페이지/컷 패킷으로 승격한다. 공개 `validate_project.py`는 기존 `page_id` 기반 잠금을 검사하며 새 1-2컷 시트 프로필을 자동 검증하지 않으므로, 기존 양식으로 검증되는 범위와 별도 컷 시트 편집 범위를 구별한다.
10. 모든 생성 단위를 `independent_page`, `same_scene_continuation`, `reused_shot_variation` 중 하나로 분류한다. 이야기 순서나 대사 진행만으로 시각적 연속성을 단정하지 않는다.
11. 화면에 표시할 텍스트의 source class와 사용자 승인 상태를 잠근다.
12. 화면 텍스트의 라우팅(`text_owner`, `owner_role`, `attachment_hint`, `read_order`)을 잠근다. 폰 최종 표시 폭과 축소에서도 잘 읽히도록 글자·대비·말풍선 공간의 목적을 함께 정리한다.
13. 등장 캐스트, 레퍼런스 역할, 파일 해시, 동시 등장 규칙을 잠근다. 반복 등장 캐릭터에 사람 승인 identity reference가 없으면 외형 일관성을 보장한다고 주장하지 말고 멈춰서 레퍼런스를 요청한다.
14. 전체 흐름·현재 구간·앞뒤 상태·정확한 대사·WHY를 담아 자기완결적인 provider-bound 프롬프트를 작성한다. 분리 가능한 1-2컷 시트 후보를 뽑을 때는 생성 시트 내부 배치와 최종 세로 스크롤 배치가 다른 단계임을 명시한다(`docs/CUT_BASED_PRODUCTION.md`).
15. `validate_project.py --stage pre-generation --strict`를 실행한다. 승인된 provider instruction 원문을 사용할 때는 `docs/PROVIDER_ADAPTER.md`에 따라 `--provider-instruction`과 허용된 `--provider-amendments`를 함께 전달한다.
16. 사용자의 명시적인 생성 승인을 기다린다.
17. 기본 실행기인 `ima2-gen`을 사용해 실제 runtime, 입력, 출력을 기록한다. 첫 도입이나 입력 변경 시 수행하는 pilot은 실제 전달 확인이 목적이며 매번 소규모 배치만 강제하지 않는다. 승인 후에는 최소 3개 이상의 독립 후보를 생성하고, 연기·표정·액션·공개·분위기가 중요한 구간은 4-6개를 우선한다. 단일 후보는 기술 점검, 명시적 비용 제한, 사용자 직접 요청에만 쓴다.
   - 승인된 장수·비용 안에서 단위 시간당 사람이 고를 만한 후보 수를 최우선으로 확보한다. 후보 풀·wave 크기·동시 실행 수를 구별하며, 개별 실패율 상승만으로 소규모 보수 모드로 자동 전환하지 않는다. 실제 시간당 완료량이 과부하로 줄어들 때 제출량을 조절한다. 사용자의 수량·재시도 제한을 우선하고, 성공 원본·요청 식별·늦은 성공 회수를 보존하며, 최종 시각 선택은 사용자에게 맡긴다(`docs/PROVIDER_ADAPTER.md`, 「대량 병렬 후보 탐색」).
   - 현재 승인된 수량·재시도 범위 안에서 개별 작업이 실패하면, 진행 중인 성공 작업을 멈추지 않고 실패한 작업만 다음 파동 맨 앞에 재투입한다. 마지막 파동 뒤에도 남은 실패는 숨기지 않고 명확히 보고한다.
18. 모든 후보를 사용자에게 전달해 시각 판단을 받는다. 사용자가 비평을 요청하지 않으면 파일 수·경로·크기·해시 등 객관 사실만 보고한다.
19. 사람이 선택한 이미지의 구조·연기·캐스트·서사 호흡은 맞지만 식자나 몇 곳의 국소 결함만 남았을 때는 선택적으로 `harness/templates/post_selection_page_finish_request.md`를 사용할 수 있다. 선택 원본과 해시를 보존하고, 최종 visible text 전체와 라우팅을 다시 적으며, 컷별 국소 수정 사항과 keep list만 지정해 새 후보로 저장한다. 사용자가 기존 글자를 유지하기로 한 결정은 그대로 보존한다. 구조·인과·정체성·fact/MSG 경계나 핵심 연기가 틀렸다면 수정하지 말고 재생성한다.
20. 선택되지 않았거나 대체된 후보는 current에서 분리하되 삭제하지 않는다.
21. 선택된 컷들을 세로 원고로 조립할 때는 각 컷의 크기·정렬과 함께 `앞 컷 아래 흰 여백 + 추가 간격 + 다음 컷 위 흰 여백`으로 실제 거리를 계산해 목표 거리의 부족분만 더한다(`docs/CUT_BASED_PRODUCTION.md`, `docs/PANELING_AND_PACING.md`). 전체 보기본은 별도 보관하고, 커뮤니티 업로드용 파일은 안전한 흰 여백에서 무손실 분할해 번호순으로 전달한다(`docs/UPLOAD_DELIVERY.md`). 최종 승인 후 `freeze_completion.py`로 완성본, 승인 원본, 실제 사용 소재를 SHA-256 매니페스트와 함께 동결한다.

## Source Scope

빠르게 흐르는 실시간 주제는 좁고 선명한 현재 범위를 우선한다. 최신 피드 2페이지, 개념글/추천글 첫 페이지, 의미 있는 토론이 붙은 게시글을 기본 범위로 삼되, 사용자가 직접 지정한 앵커 게시글이 있으면 언제나 최우선으로 따른다.

지어낸 대사를 실제 인용문이나 커뮤니티 합의처럼 적지 않고 반드시 `MSG`로 분류한다.

## Conte Gate

거친 요약문을 곧바로 이미지 프롬프트로 바꾸지 않는다. 각 패킷은 다음 요소를 갖추어야 한다.

- source ledger 연결 행과 서사적 목적(WHY)
- 정확한 등장 캐스트(장면 이해에 필요한 발화자·상대·반응·핵심 볼거리는 살리고 불필요한 구경꾼은 줄이되, 인물 수 자체를 기계적으로 최소화하지 않음)
- 화면에 실제로 보일 소품·정보 요소 목록(화면에 보일 면과 글자만 작화 묘사에 적고, 소품이 필요한 이야기상 이유는 전체 맥락으로 설명)
- 비텍스트 시각 정보와 연기 포인트
- 배경 예산(반복 배경과 연속성 부담 절감)
- visible-text source 및 routing 행
- positive composition lock
- next-cut hook
- review destination

이 관문은 구조 누락을 막는 장치이지 GPT/Codex가 좋은 콘티를 썼다는 창작 보증이 아니다. AGY/Gemini 원출력이 보존되고, 제안별 `adopt / adapt / reject` 검토와 전편→장면→컷 퇴고를 거쳐 사람이 최종 canonical 버전을 승인해야 완결된다. 자료 첨부나 스크립트 PASS를 실제 작법 퇴고로 치환하지 않는다.

전개가 급하게 느껴지면 빠진 감정이나 정보 다리를 찾아 반응·연결·침묵·순서 조정을 선택한다. 대사와 장면 퇴고 뒤에는 `docs/PANEL_LAYOUT_REVISION.md`와 `docs/CUT_BASED_PRODUCTION.md`로 읽기 공간을 다듬는다.

## Page Relation Gate

레퍼런스를 묶기 전에 장면 관계를 먼저 결정한다.

- `independent_page`: 캐릭터 identity/style 레퍼런스만 사용한다. 뒤이어 나오는 대화나 리액션도 시각적으로 독립이면 이 관계를 쓴다.
- `same_scene_continuation`: identity 레퍼런스를 유지한 채 직전 승인/현재 이미지를 별도 scene-state 레퍼런스로 추가한다.
- `reused_shot_variation`: identity 레퍼런스를 유지한 채 승인/현재 샷을 변주 원본으로 사용한다.

이 의미 판단은 스킬과 편집자가 맡는다. 하네스는 선언된 관계와 프롬프트·레퍼런스 결합이 일치하는지 검증하고, 실행기(`ima2-gen`)는 실제 생성 작업을 제출한다. 하네스 바인딩 오류를 연출 판단처럼 포장하거나 페이지 번호만으로 하네스가 이야기 맥락을 추론하게 두지 않는다.

## Image Page Contract

제작 프로필은 작품에 따라 구별해 적용한다.

- **분리 가능한 1-2컷 시트 + 세로 편집 프로필(`docs/CUT_BASED_PRODUCTION.md`)**: 생성 시트에서는 나중에 깔끔하게 분리할 수 있는 1-2컷 구성과 연기·말풍선 공간에 집중하고, 최종 세로 스크롤에서의 크기·정렬·간격 조립은 후속 세로 편집 단계에서 수행한다.
- **기존 전체 페이지 프로필(`docs/PANEL_LAYOUT_REVISION.md`)**: `1024x1536` 흰 세로 원고지를 시작 캔버스로 삼고, 페이지 안의 블록 수·점유 면적(60%/78% 표현 예산 또는 28-42% 여백 등)·칸 밖 식자를 한 페이지 안에서 설계한다. 이 수치는 전체 페이지 프로필의 지침이며 새 컷 시트 프로필과 억지로 합치지 않는다.

특정 작품의 `1024x1536` 크기, 컷 수, 고정 중앙 흰띠 폭, 인물 수 상한, 의상, 배율과 간격을 모든 작품의 보편 규칙으로 복사하지 않는다. 폰 최종 표시 폭과 축소 상태에서도 글자가 잘 읽히도록 생성 본문에 글자·대비·말풍선 공간의 목적을 전달한다.

provider prompt는 원하는 화면의 positive inventory로 작성한다. 승인된 생성 지침의 WHY, 예시, 협업 의도를 그대로 보존하고 명시적으로 허용된 문구 수정만 반영한다. 반려된 개념이나 내부 주의사항 파일·링크는 모델 입력에 섞지 않되, 주의사항을 분리한다는 이유로 주변의 서사적 이유(WHY)까지 요약해 지우지 않는다. 자세한 조립 방식과 사전 검증은 `docs/PROVIDER_ADAPTER.md`를 따른다.

## Review And Delivery

시각 품질 판단과 최종 채택은 사용자의 권한이다. 사용자가 시각 비평을 요청하지 않는 한 에이전트가 임의로 후보를 걸러내거나 재생성하지 않는다. 데스크톱 화면에서 축소해 보는 것과 실제 모바일 기기에서 읽는 체감은 다르다는 점을 염두에 둔다.

전달 폴더는 사용자의 작업대이므로 이전 전달 폴더를 덮어쓰거나 재구성하지 않고 새 후보 전달 시 새 폴더를 만든다. 원본 이미지는 순서대로(P001의 모든 후보 다음 P002의 모든 후보) 정렬해 사용자가 편하게 열고 확대해 고를 수 있게 한다. 비교·열람용 HTML은 사용자 명시 요청 때만 만들며, 식자·세로 편집·내보내기용 HTML/CSS와 목적을 구별한다.

캐릭터 탐색과 수정에서는 `docs/CREATIVE_CONTINUITY.md`의 원칙을 따른다. 완성 디자인을 바로 요구하기 전에 열린 해석을 먼저 맞추고, 채택된 제작 규칙과 미채택 가설을 구분하며, 압축 과정에서 감정 변화를 잃지 않고, 일부 구간만 수정할 때 사용자가 이미 고른 컷/페이지를 보존한다.

## Completion

최종 완료 보관은 다음 항목이 모두 갖추어졌을 때 끝난다.

- 전체 보기본 및 게시용 전달본(디시인사이드 기준 파일당 20,000,000바이트 미만·세로 9,000px 이하는 2026-10-21 본문 축소 관측 이후 사용자가 채택한 제작 기준이며, 안전한 흰 여백에서 원본 폭·픽셀·행·글자·기존 여백을 유지해 무손실 분할하고 번호순으로 정리한 파일)
- 사용자가 승인한 원본 페이지/컷 시트
- 실제로 사용한 소재와 레퍼런스
- `freeze_completion.py`로 생성한 SHA-256 해시 매니페스트와 재구성 메모(`freeze_completion.py`는 복사와 해시 검증만 수행하므로, 세로 높이·용량 검사 및 분할·재결합 무결성 검사는 별도 도구로 확인)

남은 작업 이력은 legacy로 보존하며 패키징 과정에서 삭제하지 않는다.
