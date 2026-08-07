---
name: community-webtoon-producer
description: Use when turning an online community post, forum incident, meme thread, live gallery mood, or user-supplied issue into a short Korean vertical info-gag webtoon; includes source collection, fact-mood-MSG separation, sweet-spot approval, causal storyboard packets, cast-text-reference locks, ima2-gen-first generation preflight, human review, and completion archiving.
---

# Community Webtoon Producer

## Objective

Produce a readable Korean community webtoon without hallucinating the community, skipping causal story work, or confusing successful image generation with user approval.

## Primary Quality Rule

Treat shared context and understanding alignment as a production input, not as conversational polish. A precise micro-prompt cannot recover a missing whole-story reason, reader-emotion sequence, recognizable motif, fact/MSG boundary, or user-observed mismatch.

Preserve context that may look irrelevant to the immediate command when it changes creative judgment. Re-state the minimum common understanding inside every downstream packet that asks another model or pass to decide. Paths, hashes, references, and previous images prove state or appearance; they do not explain why the work should look or feel that way.

This rule comes from repeated quality improvement after failed prompt-only passes. It is not an abstract collaboration philosophy.

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
4. Write and preserve a rough Director/producer beat skeleton. When a deliberate blank is part of the brief, leave it open instead of pre-solving it before the creative pass.
5. Give the skeleton and the full source/fact/MSG boundary to Gemini as a blank-filling or staging pass. Preserve the raw Gemini output beside the raw skeleton; do not overwrite either artifact.
6. Review the two artifacts with the Director and record each substantial proposal as `adopt`, `adapt`, or `reject`. Codex may enter the work to correct facts or continuity; that correction can remain visible when it serves the comic.
7. Consolidate the accepted result into one canonical conte. Give every cut `handoff_from_previous`, `reader_first_sees`, `character_realizes`, and `push_to_next`, then reduce density only after causality is visible.
8. Require a human to read, edit if needed, and explicitly approve that canonical conte. Record the raw skeleton, raw Gemini pass, joint review, and human-approved canonical version in `editorial_review_lock.csv`.
9. Promote the human-approved conte into page/cut packets with stable packet IDs.
10. Classify every page as `independent_page`, `same_scene_continuation`, or `reused_shot_variation`. Page order and dialogue progression alone do not prove visual continuity.
11. Lock visible text source class and approval state.
12. Lock visible text routing: owner, role, attachment, read order.
13. Lock visible cast, reference roles, hashes, and co-appearance rules. If a recurring character has no human-approved identity reference, stop and request one instead of claiming identity consistency.
14. Write one self-contained provider-bound prompt per page using the generation contract.
15. Run `validate_project.py --stage pre-generation --strict`.
16. Wait for explicit user authorization to generate.
17. Use ima2-gen as the default runtime and record the actual runtime, inputs, and outputs. After authorization, generate at least three independent candidates; prefer four to six for acting, expression, action, reveal, or atmosphere. Use a single candidate only for a technical probe, explicit cost limit, or direct user request.
   - If one independent job fails while later work remains, carry only the missing job into the next live wave immediately, ahead of ordinary jobs, without rebooting or cancelling successful in-flight work. After the final wave, make one isolated tail retry and leave any remaining failure explicit.
18. Hand every candidate to the user for visual judgment. Report only objective facts unless critique is explicitly requested.
19. Move unselected or superseded candidates out of current. Do not delete evidence.
20. After final approval, freeze final composites, approved sources, and actually used materials with SHA-256 manifests.

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

This is a structural gate, not a guarantee that GPT/Codex wrote a strong conte. The production path is incomplete until the raw Gemini creative pass has been preserved, its proposals have been jointly adopted/adapted/rejected, and a human has approved the consolidated canonical version.

If a reveal jumps too abruptly, insert a stacked two-subpanel bridge and delay the actual reveal to the next packet.

## Page Relation Gate

Choose the relationship before building references:

- `independent_page`: use character identity/style references only. A later dialogue or reaction page can still be independent.
- `same_scene_continuation`: add the previous approved/current image as a separate scene-state reference while retaining identity references.
- `reused_shot_variation`: use the approved/current shot as the variation source while retaining identity references.

The skill owns this semantic judgment. The harness validates the declared relation and prompt/reference consistency; the provider runtime only executes the job. Do not describe a harness-binding error as an action-scene decision, or ask the harness to infer story meaning from page numbers.

The currently verified default provider runtime is `ima2-gen`. This is an execution choice, not a transfer of story judgment: the skill decides meaning, the harness validates declared bindings, and ima2-gen submits the actual generation job. Alternative runtimes must still record their real name and preserve the same adapter evidence.

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
