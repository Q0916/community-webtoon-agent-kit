# 기존 Git와 Drive로 Claude Code 집필하기

2026-10-09 확인 기준 기록입니다(이후 시점에 UI·상품 구성을 별도 재검증하지 않았습니다). 일반 Claude Code Cloud 세션에 공개 스킬·하네스 저장소(`Q0916/community-webtoon-agent-kit`)를 연결하고, 작품에 필요한 자료만 Google Drive 또는 직접 첨부로 제공하는 구성입니다. 스킬을 작품마다 복제해 별도 정본으로 관리할 필요는 없습니다.

Cloud 환경에서 기본 저장소를 고르고 추가 저장소를 연결할 수 있습니다. 저장소별 브랜치를 지정한 뒤 필요한 `SKILL.md`와 참고 문서(`docs/CRAFT_REVIEW.md`, `docs/CUT_BASED_PRODUCTION.md`, `docs/UPLOAD_DELIVERY.md` 등)의 실제 본문을 읽게 합니다. 참고용 스킬 저장소와 새 원고를 작성할 작업 위치를 구별하고, 현재 사용자의 지시와 작품의 채택 결정을 전달합니다. 저장소를 연결했다는 사실 자체가 모든 스킬을 자동 적용하거나 외부 모델을 호출하는 권한을 뜻하지는 않습니다.

Google Drive는 Claude 계정의 Customize → Connectors에서 연결합니다. 다른 AI 앱의 Drive 인증과는 별개입니다. 실제 세션에서 지정한 자료의 검색과 본문 읽기가 되는지 직접 확인하고, 커넥터 연결 표시만 보고 자료를 읽었다고 답하지 않습니다. 작품 폴더·파일 이름 또는 ID를 명확히 알려주고 원글·댓글, 사용자 원문, 채택된 전작과 현재 캐릭터 참조만 골라 읽게 합니다. 계정 전체 자료를 무관하게 긁어모으지 않으며, 없던 자료의 업로드와 공유 범위는 사용자의 요청을 먼저 확인합니다.

클라우드 세션은 사용자의 로컬 PC 파일이나 로컬 이미지 생성 서버(`ima2-gen` 등)를 직접 읽거나 호출할 수 없습니다. 필요한 문서와 이미지 자체를 세션에 제공하고, 접근하지 못한 자료는 분명히 밝혀 적습니다. Windows 전용 스크립트나 로컬 실행기를 클라우드에서 연결 완료된 것처럼 보고하지 않습니다.

첫 요청에는 무엇을 왜 만드는지, 현재 작업 단계(전편→장면→컷 작법 퇴고, 대사 다듬기 등), 확정된 내용과 열린 선택지, 실제 자료 위치를 적습니다. 아직 소재를 탐색하는 대화라면 페이지/컷 수나 전체 콘티, 생성 계획을 자동으로 확정하지 않습니다.

역할 분담에서 사용자는 의미·취향·각색·최종 선택을 맡고, AGY(Gemini)는 위임받은 집필·문장 편집(거친 뼈대 빈칸 채우기, 자유 집필, 완성문 퇴고 포함)을 맡으며, Codex는 사실·연속성 확인과 제작 실행을 맡습니다. 집필 모델은 사용자가 정할 수 있지만, 이 공개 키트의 기존 `validate_project.py --stage pre-generation` 검증은 Gemini 원출력과 사람 채택 기록(`04_locks/editorial_review_lock.csv` 및 해시)을 요구합니다. 따라서 Claude(Sonnet 등) 집필 세션을 만들었다는 이유만으로 공개 검증기의 Gemini 원출력 요건을 통과했다거나 동일한 창작 검증 이력을 갖췄다고 주장하지 않습니다.

Cloud 세션 URL을 기록해 두면 같은 Claude 계정의 웹과 Desktop Code 탭에서 작업을 이어갈 수 있습니다. 지급된 Cloud 보너스의 적용 범위와 만료 시점은 공식 안내 및 계정 Usage에서 확인합니다. 일반 세션과 Projects/Routines·로컬 Remote Control을 구별하며, 이 구성을 이유로 추가 유료 결제를 임의로 켜지 않습니다.

공식 안내: [Desktop Cloud와 다중 저장소](https://code.claude.com/docs/en/desktop#run-long-running-tasks-in-the-cloud), [계정 커넥터 전달](https://code.claude.com/docs/en/mcp#how-connectors-reach-claude-code), [Cloud 보너스](https://support.claude.com/en/articles/17152539-cloud-sessions-bonus-credit-promotion).
