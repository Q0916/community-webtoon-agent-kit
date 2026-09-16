# Provider Adapter Contract

이 키트의 현재 검증된 기본 실행기는 [**ima2-gen**](https://github.com/lidge-jun/ima2-gen)입니다. 실제 생성은 ima2-gen의 실제 CLI/server 경로로 수행하며, 별도 shim이나 성공을 흉내 내는 우회 경로를 만들지 않습니다. 다른 provider/runtime으로 교체할 수는 있지만 아래 입력·증거 계약은 그대로 지켜야 합니다.

기본 실행 예시는 `ima2 gen "..."`이며 설치형 CLI가 없으면 `npx ima2-gen <command>`를 사용합니다. 서버 주소가 필요할 때는 출력이나 ima2의 server state를 확인하고 특정 포트를 가정하지 않습니다.

## 입력

- provider-bound page prompt 한 개
- generation plan에 기록된 실제 `runtime` 이름(기본값 `ima2-gen`)
- 작품 전체 이야기, 독자 감정 순서, 현재 페이지의 이유와 전후 상태, fact/MSG 경계
- generation plan에 잠근 `scene_relation`
- 해당 페이지의 character/style/continuity reference 목록
- 출력 디렉터리
- 페이지 ID와 시도 ID
- 기술 사전검사 결과
- 사용자의 현재 생성 승인 근거

각 page prompt는 다른 전역 문서를 읽지 않아도 독립적으로 완전해야 합니다. `COMMUNITY_TOON_GENERATION_CONTRACT_V1` 블록과 작품 공통 이해, 페이지별 캐스트·텍스트·소품·구도 정보가 같은 파일 안에 있어야 합니다. 정확한 수행 지시만 보내고 작품 전체 이유와 감정선을 생략하지 않습니다.

Adapter는 page ID나 제출 순서에서 continuity를 추론하지 않습니다. `independent_page`에는 scene-continuity reference가 없어야 하고, `same_scene_continuation` 또는 `reused_shot_variation`에는 선언된 scene reference가 있어야 합니다.

## 생성지침의 WHY와 문맥 전달

승인된 provider 스킬은 임의 요약용 자료가 아니라 실제 입력 본문이다. 원문의 목적·인과·예시·협력 요청을 보존하고 작품별 장면을 이어 붙인다. 가설·협력이라는 단어와 비율만 남긴 입력은 문맥 전달의 증거가 아니다. 큰 흰 원고와 간결한 주변 묘사는 중요한 얼굴·손·몸짓·소품·글자를 더 잘 표현하려는 수단이므로, 핵심 표현을 충분히 보여주는 것과 함께 판단한다.

사용자가 부정형·보험 문구 분리를 요청하면 해당 범위만 내부 주의사항으로 옮기고, 주변 WHY와 예시는 유지한다. 필요한 긍정형 변경은 원문 해시와 정확한 before/after, 이유·사용자 결정 근거를 가진 내부 목록으로 관리한다. 내부 주의사항과 변경 목록은 생성 모델에 첨부하거나 발췌·링크로 넣지 않는다. 이미 승인받은 범위는 다시 묻지 않는다.

본문 조립과 기존 사전검사 연결:

```bash
python harness/scripts/provider_instruction_integrity.py --source approved-provider.md --emit provider-body.txt
python harness/scripts/validate_project.py --project work/my-first-toon --stage pre-generation --strict --provider-instruction approved-provider.md
```

첫 명령으로 만든 파일의 전문을 각 `05_prompts/*.txt`에 삽입한다. 승인된 변경이 있으면 조립에는 `--amendments`, 검증에는 `--provider-amendments`로 같은 JSON을 전달한다. JSON 형식은 `{"source_sha256":"원문 파일 SHA-256","changes":[{"before":"유일한 원문 구절","after":"승인된 변경 구절","reason":"변경 이유","user_decision_reference":"실제 사용자 결정 근거"}]}`다. BOM·줄바꿈·YAML 설치 메타데이터만 전송 형식 차이로 처리한다. 자동 검사는 텍스트 보존과 근거 필드의 존재를 확인하며, 사용자 승인 사실과 의미는 제작자가 확인한다.

준비 때 원문 대조를 한 번 수행하고, 실행기가 그 결과에 프롬프트·원문·변경 목록의 해시를 묶었다면 제출 직전에는 기존 해시 검사로 변경 여부를 확인한다. 이 경우 같은 전문 대조를 반복할 필요가 없다. 이 공개 키트의 검증 보고서만으로 제출 시점의 해시 결합까지 제공된다고 해석하지 않는다. 그러한 실행기가 없으면 실제 제출 입력을 다시 대조한다. `--provider-instruction`을 생략한 기존 호환 경로는 provider 전문 보존을 검사했다고 주장할 수 없다.

규칙을 줄이기 전에는 기능이 막는 실패와 이유를 회수한다. 첫 입력부터 축약됐는지 확인하는 전문 대조와, 검증 뒤 파일이 바뀌었는지 확인하는 해시는 역할이 다르다. 이유가 불명확한 항목은 유지하고, 같은 역할을 중복 수행하는 부분만 통합한다.

## 출력 증거

provider adapter는 가능한 범위에서 다음을 남깁니다.

- 실제 전송한 prompt 또는 그 SHA-256
- 실제 첨부한 reference 경로와 SHA-256
- provider/model/size/quality 파라미터
- 제출 시각과 완료 시각
- 생성 파일 경로와 바이트 크기
- 오류 원문

`refsCount: 3`처럼 개수만 남기는 기록은 어떤 파일이 붙었는지 증명하지 못합니다.

## 파일럿

첫 파일럿은 다음을 확인합니다.

1. 한국어가 provider까지 손상 없이 전달됐는가?
2. 올바른 레퍼런스 파일이 붙었는가?
3. 흰 원고지와 inset/cut-in 구조가 prompt에 실제 포함됐는가?
4. 출력이 완료됐는가?

1~3은 기술·입력 검증입니다. 이미지의 매력과 채택 여부는 사람 검수입니다.

## Sidecar 운영

긴 생성은 대화 밖 sidecar로 실행합니다. 요청이 접수됐거나 active 상태가 된 것을 한 번 확인한 뒤, 완료 알림 또는 사용자의 상태 요청 전까지 반복 폴링하지 않습니다.

독립 job 하나가 실패했지만 뒤의 job이나 다음 wave가 남아 있다면 전체 완료까지 기다렸다가 수동으로 발견하지 않습니다. 실패한 job만 다음 live wave의 맨 앞에 즉시 승계하고, 이미 성공했거나 실행 중인 job과 서버는 취소·재부팅하지 않습니다. 마지막 ordinary wave 뒤에도 남은 실패는 한 번 별도 tail retry하고, 그래도 실패하면 재시도 입력과 오류를 보존한 채 partial 상태로 보고합니다.
