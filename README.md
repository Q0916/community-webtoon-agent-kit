# Community Webtoon Agent Kit

한국 온라인 커뮤니티의 글, 댓글, 밈, 실시간 이슈를 짧은 세로형 정보·개그 웹툰으로 만드는 **에이전트용 제작 스킬과 검증 하네스**입니다.

이 저장소는 완성 이미지나 이미지 생성 모델 자체를 배포하지 않습니다. 대신 결과의 품질을 좌우했던 제작 순서, 승인 게이트, 콘티 구조, 텍스트·캐스트·레퍼런스 잠금, 프롬프트 계약, 사람 검수, 완성 보관 절차를 제공합니다. **현재 검증된 기본 이미지 생성 실행기는 [ima2-gen](https://github.com/lidge-jun/ima2-gen)입니다.** 다른 실행기를 연결할 수는 있지만, 이 문서와 실제 사례에서 `provider runtime`이라고 쓰는 기본값은 ima2-gen입니다.

## 가장 중요한 품질 규칙

> 창작 작업은 정확하고 철저한 프롬프트보다, 얼핏 쓰잘데기 없어 보이는 문맥과 참여자 사이의 이해 일치가 더 중요하다.

여기서 문맥은 작품 전체 이야기, 독자가 느껴야 할 감정 순서, 이 장면을 만드는 이유, 사용자가 감지한 미묘한 불일치, 참조를 알아봐야 하는 이유, 각 모델과 사람의 역할을 포함합니다. 작업 지시와 직접 관련 없어 보여도 다음 창작 판단을 바꾸는 정보라면 제거하지 않습니다.

이는 협업 철학을 선언하기 위한 문장이 아닙니다. 정확한 미시 프롬프트만 전달했을 때보다, 이런 문맥과 이해를 패스마다 다시 공유했을 때 결과 품질이 반복해서 상승한 시행착오 기반 제작 방법입니다. 분업은 실행을 나누는 것이지 작품 이해를 나누는 것이 아닙니다.

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

프로젝트 초기화와 검증 하네스에는 Python 3.10 이상만 필요하며 외부 패키지는 없습니다. 실제 이미지 생성에는 Node.js 20+와 ima2-gen이 필요합니다.

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
7. `generation_plan.csv`에서 각 페이지를 `independent_page`, `same_scene_continuation`, `reused_shot_variation` 중 하나로 잠급니다.
8. `generation_plan.csv`의 `runtime`을 기본값 `ima2-gen`으로 기록하고, `05_prompts`에 각 페이지가 독립적으로 완전한 provider-bound 프롬프트를 갖게 합니다.
9. 생성 전 검사를 실행합니다.

```bash
python harness/scripts/validate_project.py --project work/my-first-toon --stage pre-generation --strict
```

10. 사용자 생성 승인 뒤 ima2-gen으로 최소 3개의 독립 후보를 빠르게 생성하고 사람이 직접 판단합니다. 연기·표정·액션·반전·분위기가 중요한 컷은 4~6개를 우선합니다.
11. 승인된 파일만 별도 전달 폴더로 복사합니다.
12. 최종 승인 후 완성본, 승인 원본, 실제 사용 소재를 해시와 함께 동결합니다.

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

## 실제 제작 사례

- [Amazon × OpenAI 500억 달러 특갤툰 제작 사례](examples/amazon-openai-50b/README.md)
- [개인정보를 제거한 제작 대화와 교정 기록](examples/amazon-openai-50b/conversation.md)
- [실제 게시 결과물: 특갤툰) AGI 떴냐?!?!](https://gall.dcinside.com/thesingularity/1347863)

이 사례는 5페이지·13컷의 대화형 정보 개그툰을 17개 독립 후보로 생성하고, 사람이 페이지별 후보를 선택해 완성한 기록입니다. `이야기 진행`을 `액션/동일 샷 연속성`으로 잘못 읽었던 순간과, 이를 스킬 판단·하네스 검증·런타임 실행으로 다시 분리한 과정도 포함합니다.

## 저장소 정책

- Git에 넣음: 스킬, 지침, 템플릿, 검증 스크립트, 작은 텍스트 예시.
- Git에 넣지 않음: 생성 이미지, 원본 캡처, 캐릭터 시트, 개인정보, 쿠키, API 키, 대형 로그.
- 이 저장소의 코드와 문서는 MIT 라이선스입니다. 사용자가 별도로 넣는 소스, 이미지, 캐릭터, 상표의 권리는 각 권리자에게 있습니다.

## 크레딧

기본 이미지 생성 실행기는 **[ima2-gen](https://github.com/lidge-jun/ima2-gen)** 이며, 원작자·관리자는 **[lidge-jun](https://github.com/lidge-jun)** 입니다. 이 공개킷은 ima2-gen 자체가 아니라 그 위에서 사용하는 커뮤니티 웹툰 제작 스킬·검증 하네스를 제공합니다.
