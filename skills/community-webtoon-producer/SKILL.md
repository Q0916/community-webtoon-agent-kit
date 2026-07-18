---
name: community-webtoon-producer
description: Use when turning an online community post, forum incident, meme thread, live gallery mood, or user-supplied issue into a short Korean vertical info-gag webtoon; includes source collection, fact-mood-MSG separation, sweet-spot approval, causal storyboard packets, cast-text-reference locks, provider-neutral generation preflight, human review, and completion archiving.
---

# Community Webtoon Producer

## Objective

Produce a readable Korean community webtoon without hallucinating the community, skipping causal story work, or confusing successful image generation with user approval.

## First Read

From the repository root, read:

1. `AGENTS.md`
2. `docs/BEFORE_YOU_START.md`
3. `docs/QUALITY_CONTRACT.md`
4. the active project's `PROJECT.md`

If no project exists, initialize one with `harness/scripts/init_project.py`.

## Required Workflow

1. Collect the primary post and a narrow sample of surrounding reaction sources. Record URLs and observed times.
2. Separate `primary_fact`, `mood_source`, `MSG`, and `do_not_use` in the source ledger.
3. Discuss and obtain approval for the sweet spot: Director intent, community reader expectation, and comic pacing.
4. Write an overfull draft conte, then reduce it only after causality is visible. Preserve this version.
5. Give every cut these fields: `handoff_from_previous`, `reader_first_sees`, `character_realizes`, `push_to_next`.
6. Send the full source basis and current conte to Gemini for an independent editorial review and version-up. Preserve the Gemini artifact as a new version; do not overwrite the draft.
7. Require a human to read, edit if needed, and explicitly approve the final conte version. GPT/Codex structural checks do not certify front-end creative quality.
8. Record Gemini and human evidence in `editorial_review_lock.csv`, with the human-approved output version matching the current conte version.
9. Promote the human-approved conte into page/cut packets with stable packet IDs.
10. Lock visible text source class and approval state.
11. Lock visible text routing: owner, role, attachment, read order.
12. Lock visible cast, reference roles, hashes, and co-appearance rules. If a recurring character has no human-approved identity reference, stop and request one instead of claiming identity consistency.
13. Write one self-contained provider-bound prompt per page using the generation contract.
14. Run `validate_project.py --stage pre-generation --strict`.
15. Wait for explicit user authorization to generate.
16. Generate one pilot or a small batch. Record provider inputs and outputs.
17. Hand every candidate to the user for visual judgment. Report only objective facts unless critique is explicitly requested.
18. Move unselected or superseded candidates out of current. Do not delete evidence.
19. After final approval, freeze final composites, approved sources, and actually used materials with SHA-256 manifests.

## Source Scope

For a fast live topic, prefer a narrow current window. A useful default is the newest two feed pages, the first recommended/trending page, and posts with meaningful discussion. User-provided anchor posts always override discovery scope.

Do not present invented lines as quotations or observed consensus. Label them as MSG.

## Conte Gate

Do not turn a broad summary directly into image prompts. Each packet needs:

- source ledger rows and story purpose
- exact visible cast
- allowed visible object and information-prop inventory
- non-text visual information
- background budget
- visible-text source and routing rows
- positive composition lock
- next-cut hook
- review destination

This is a structural gate, not a guarantee that GPT/Codex wrote a strong conte. The production path is incomplete until Gemini has independently reviewed/versioned the conte and a human has approved the final version.

If a reveal jumps too abruptly, insert a stacked two-subpanel bridge and delay the actual reveal to the next packet.

## Image Page Contract

Default to a 1024x1536 pure-white vertical manuscript page with 2-4 inset/cut-in illustration blocks and 28-42% continuous blank white page space for pacing and text. Bubbles, captions, comment cards, and SFX may sit outside the illustrated blocks.

Use a full-page or poster composition only when the Director explicitly requests it.

Build provider prompts as a positive inventory. Keep rejected concepts and contamination risks in audit files rather than teaching them to the provider through long negative lists.

## Review And Delivery

The user owns visual quality judgment. Do not silently filter candidates, mark visual failures, or regenerate based on assistant vision unless the user asked for visual critique.

Delivery folders are user workbenches. Never rebuild or overwrite an earlier delivery. Create a fresh delivery for later candidates.

## Completion

Final approval is not complete until the archive contains:

- viewing/posting finals
- exact user-approved source pages/cuts
- materials actually used
- a hash manifest and reconstruction notes

Preserve the remaining working history as legacy; do not delete it during packaging.
