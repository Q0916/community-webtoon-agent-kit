# 기존 Git와 Drive로 Claude Code 집필하기

2026-10-09 확인. 일반 Claude Code Cloud 세션에 기존 스킬·하네스 저장소를 연결하고, 작품에 필요한 자료만 Google Drive 또는 첨부로 제공하는 구성입니다. 스킬을 작품마다 복제해 별도 정본으로 관리할 필요는 없습니다.

Cloud 환경에서 저장소를 고르고 추가 저장소를 연결할 수 있습니다. 저장소별 브랜치를 정하고 필요한 `SKILL.md`와 참고문서의 실제 내용을 읽게 합니다. 참고 저장소와 새 원고의 작업 위치를 구별하고, 현재 사용자 지시와 작품의 채택 결정을 전달합니다. 저장소 연결은 모든 스킬을 자동 적용하거나 외부 모델을 호출하는 권한이 아닙니다.

Drive는 Claude 계정의 Customize → Connectors에서 연결합니다. 다른 AI 앱의 Drive 인증과 별개입니다. 실제 세션에서 지정 자료의 검색·본문 읽기를 확인하고, 연결 표시만으로 자료를 읽었다고 말하지 않습니다. 작품 폴더·파일 이름 또는 ID를 알려주고 원글·댓글, 사용자 원문, 채택 전작과 현재 캐릭터 참조만 고릅니다. 계정 전체 자료를 무관하게 모으지 않습니다. 없던 자료의 업로드와 공유 범위는 사용자의 요청에서 확인합니다.

클라우드 환경은 로컬 PC 파일과 이미지 생성 서버를 바로 읽을 수 없습니다. 필요한 문서와 이미지 자체를 제공하고, 접근하지 못한 자료를 분명히 남깁니다. Windows 전용 스크립트나 로컬 실행기를 연결 완료로 보고하지 않습니다.

첫 요청에는 무엇을 왜 만드는지, 현재 단계, 확정 내용과 열린 선택, 실제 자료 위치를 적습니다. 소재 대화라면 페이지 수·전체 콘티·생성을 자동 확정하지 않습니다. 작성자는 사용자가 정한 모델이며, 이 공개 키트의 기존 pre-generation 검증은 Gemini 원출력과 사람 채택 기록을 요구합니다. Sonnet 집필 세션을 만들었다고 그 검증을 통과했거나 같은 창작 이력을 가졌다고 주장하지 않습니다.

Cloud 세션 URL을 기록하면 같은 Claude 계정의 웹과 Desktop Code 탭에서 이어갈 수 있습니다. 지급된 Cloud 보너스의 적용 범위와 만료는 공식 안내 및 계정 Usage에서 확인합니다. 일반 세션과 Projects/Routines·로컬 Remote Control은 구별하며, 이 구성으로 추가 결제를 켜지 않습니다.

공식 안내: [Desktop Cloud와 다중 저장소](https://code.claude.com/docs/en/desktop#run-long-running-tasks-in-the-cloud), [계정 커넥터 전달](https://code.claude.com/docs/en/mcp#how-connectors-reach-claude-code), [Cloud 보너스](https://support.claude.com/en/articles/17152539-cloud-sessions-bonus-credit-promotion).
