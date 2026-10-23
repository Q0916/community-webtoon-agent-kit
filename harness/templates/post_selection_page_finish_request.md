# Post-Selection Page Finish Request

Status: experimental opt-in. Use only after a human selects the source page and confirms that its page structure, core acting, cast, and story beat already work.
(실험적 선택 과정: 사람이 원본 페이지나 컷 후보를 직접 골라 구도·핵심 연기·인물·이야기 흐름이 이미 살아 있다고 확인한 뒤, 국소적인 식자나 세부 시각 수선이 필요할 때만 사용한다. 사용자가 기존 생성 글자를 그대로 유지하기로 결정한 경우에는 불필요하게 글자를 다시 덮어쓰지 않는다.)

## Source

- page/cut ID:
- selected source path:
- selected source SHA-256:
- why this candidate was selected:

Do not overwrite the selected source. Produce a new candidate.
(선택된 성공 원본 파일은 덮어쓰지 않고 보존하며, 수정본은 새 후보 경로로 생성한다.)

## Replace All Visible Text

When full lettering replacement is authorized, remove or replace every old readable speech bubble, thought bubble, caption, comment card, label, and SFX. Render only this final locked table. Metadata guides placement and must not render. If existing lettering is to be kept, omit this section.
(글자 교체가 필요한 경우에만 아래 확정 표의 한국어 문구만 정확히 렌더링한다. 표의 메타데이터 컬럼은 위치 안내용이며 화면에 글자로 그려지면 안 된다.)

| read_order | cut | text_owner | owner_role | attachment_hint | text_class | exact Korean text |
|---:|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |

Preserve exact Korean spelling, spacing, punctuation, ownership, and reading order. Add no labels, quotes, subtitles, or explanatory text.
(맞춤법, 띄어쓰기, 문장부호, 발화자 귀속, 읽는 순서를 정확히 지키며 설명 라벨이나 임의의 부제를 덧붙이지 않는다. 스마트폰 축소 표시에서도 읽히도록 글자 대비와 말풍선 안 여백을 확보한다.)

## Visual Repairs

Use natural descriptions of the intended result. Do not redesign the page.
(전체 구도를 새로 갈아엎지 말고, 실제로 화면에 보여야 할 자연스러운 결과 상태를 묘사한다.)

1. cut / subject / current failure / desired natural result:

## Keep

- page geometry and whitespace rhythm;
- named-character identity and accepted acting;
- unlisted props, backgrounds, effects, and composition;
- full canvas, dimensions, and edges.

## Output And Review

- output path/branch ID:
- reviewer: User/Director
- on failure, branch from the selected original or last accepted output, never from a degraded rejected edit.
- regenerate instead when structure, causal beat, core acting, identity, source/fact boundary, or most of the page is wrong.
