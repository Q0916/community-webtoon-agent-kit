# Provider Adapter Contract

이 키트는 특정 이미지 생성 서비스에 묶이지 않습니다. 에이전트는 사용하는 provider에 아래 입력과 증거를 전달할 수 있어야 합니다.

## 입력

- provider-bound page prompt 한 개
- 해당 페이지의 character/style/continuity reference 목록
- 출력 디렉터리
- 페이지 ID와 시도 ID
- 기술 사전검사 결과
- 사용자의 현재 생성 승인 근거

각 page prompt는 다른 전역 문서를 읽지 않아도 독립적으로 완전해야 합니다. `COMMUNITY_TOON_GENERATION_CONTRACT_V1` 블록과 페이지별 캐스트·텍스트·소품·구도 정보가 같은 파일 안에 있어야 합니다.

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
