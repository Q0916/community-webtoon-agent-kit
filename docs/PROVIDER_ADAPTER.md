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
