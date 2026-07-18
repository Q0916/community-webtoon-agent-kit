# Community Webtoon Agent Kit

한국 온라인 커뮤니티의 글, 댓글, 밈, 실시간 이슈를 짧은 세로형 정보·개그 웹툰으로 만드는 **에이전트용 제작 스킬과 검증 하네스**입니다.

이 저장소는 완성 이미지나 특정 이미지 생성 모델을 배포하지 않습니다. 대신 결과의 품질을 좌우했던 제작 순서, 승인 게이트, 콘티 구조, 텍스트·캐스트·레퍼런스 잠금, 프롬프트 계약, 사람 검수, 완성 보관 절차를 제공합니다.

중요: 자료 해석·콘티·연출 같은 프론트 창작 작업은 GPT/Codex 단독 품질을 보증하지 않습니다. 이 키트의 검증된 경로는 **Gemini의 별도 콘티 검수·버전업과 사람의 직접 수정 또는 최종 승인**을 모두 거치는 것입니다. 둘 중 하나라도 생략한 결과는 이 키트가 말하는 품질 보장 범위 밖입니다.

## 다른 에이전트에게 첨부하는 법

저장소 전체를 작업공간에 넣고 다음 문장을 전달하세요.

```text
이 저장소의 AGENTS.md와 skills/community-webtoon-producer/SKILL.md를 먼저 끝까지 읽어라.
그 지침을 현재 작업 계약으로 사용하되, 이미지 생성 전에 소스 원장, 방향 합의, 텍스트 콘티, 캐스트/텍스트/레퍼런스 잠금, 사람 승인을 순서대로 통과하라.
먼저 새 프로젝트를 초기화하고, 지금 필요한 단계의 문서만 작성하라.
```

Codex 개인 스킬로 설치하려면 `skills/community-webtoon-producer` 폴더를 `$CODEX_HOME/skills/` 아래에 복사할 수 있습니다. 다른 에이전트에서는 루트 `AGENTS.md`와 스킬 파일을 직접 읽게 하면 됩니다.

## 빠른 시작

Python 3.10 이상만 필요합니다. 외부 패키지는 없습니다.

```bash
python harness/scripts/init_project.py --root work --slug my-first-toon --title "첫 커뮤니티툰"
```

생성된 프로젝트의 `PROJECT.md`부터 열고 다음 순서로 진행합니다.

1. `01_sources/source_ledger.md`: 사실, 분위기, MSG, 사용 금지를 분리합니다.
2. `02_direction/creative_brief.md`: 사용자 의도, 커뮤니티 기대, 만화 가독성의 교집합을 승인받습니다.
3. `03_conte/image_ready_conte.md`: 인과가 보이는 텍스트 콘티와 컷 패킷을 작성합니다.
4. 콘티를 Gemini가 별도로 검수·버전업하고, 사람이 최종본을 직접 고쳐 보거나 승인합니다.
5. `04_locks/editorial_review_lock.csv`에 Gemini 검수본과 사람 승인본의 버전·근거 파일을 기록합니다.
6. `04_locks`: 화면 텍스트, 화자, 캐스트, 레퍼런스를 잠급니다.
7. `05_prompts`: 각 페이지가 독립적으로 완전한 provider-bound 프롬프트를 갖게 합니다.
8. 생성 전 검사를 실행합니다.

```bash
python harness/scripts/validate_project.py --project work/my-first-toon --stage pre-generation --strict
```

9. 작은 파일럿을 생성하고 사람이 직접 판단합니다.
10. 승인된 파일만 별도 전달 폴더로 복사합니다.
11. 최종 승인 후 완성본, 승인 원본, 실제 사용 소재를 해시와 함께 동결합니다.

```bash
python harness/scripts/freeze_completion.py \
  --project work/my-first-toon \
  --archive-root completed \
  --final-list work/my-first-toon/07_logs/final_files.txt \
  --approved-list work/my-first-toon/07_logs/approved_sources.txt \
  --materials-list work/my-first-toon/07_logs/used_materials.txt \
  --apply
```

## 무엇이 결과를 바꾸는가

- 커뮤니티 반응을 추측하지 않고 실제 소스와 MSG를 분리합니다.
- 펀치라인부터 쓰지 않고, 컷마다 다음 행동을 만드는 원인을 적습니다.
- 이미지 생성 전에 대사 내용뿐 아니라 대사가 **누구에게 어디로 붙는지** 잠급니다.
- 캐릭터 이름만 쓰지 않고 레퍼런스 역할과 해시를 기록합니다.
- 배경을 채우는 대신 흰 원고지, inset 그림 블록, 말풍선 공간을 설계합니다.
- 생성 성공과 창작 승인을 분리합니다. 최종 미감 판단은 사람이 합니다.
- 실패 후보를 현재 입력면에서 치워 다음 생성에 섞이지 않게 합니다.

처음 사용하는 사람과 에이전트는 반드시 [사용 전 준비와 품질 전제](docs/BEFORE_YOU_START.md)를 먼저 확인하세요. 특히 반복 등장 캐릭터를 고정하려면 사용자가 미리 레퍼런스 파일을 준비하고 역할별로 매핑해야 합니다. 프롬프트만으로 동일 캐릭터를 유지하는 것은 이 키트의 품질 보장 범위가 아닙니다.

자세한 기준은 [품질 계약](docs/QUALITY_CONTRACT.md)과 [provider 연결 안내](docs/PROVIDER_ADAPTER.md)를 참고하세요.

## 저장소 정책

- Git에 넣음: 스킬, 지침, 템플릿, 검증 스크립트, 작은 텍스트 예시.
- Git에 넣지 않음: 생성 이미지, 원본 캡처, 캐릭터 시트, 개인정보, 쿠키, API 키, 대형 로그.
- 이 저장소의 코드와 문서는 MIT 라이선스입니다. 사용자가 별도로 넣는 소스, 이미지, 캐릭터, 상표의 권리는 각 권리자에게 있습니다.
