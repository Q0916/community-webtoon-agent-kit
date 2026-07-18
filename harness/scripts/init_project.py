#!/usr/bin/env python3
"""Create a portable community-webtoon project without overwriting existing work."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


SAFE_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    return parser.parse_args()


def create_project(root: Path, slug: str, title: str) -> Path:
    if not SAFE_SLUG.fullmatch(slug):
        raise ValueError("slug must use only ASCII letters, numbers, dot, dash, and underscore")

    target = root.expanduser().resolve() / slug
    if target.exists():
        raise FileExistsError(f"target already exists: {target}")

    repo_root = Path(__file__).resolve().parents[2]
    templates = repo_root / "harness" / "templates"
    code = re.sub(r"[^A-Za-z0-9]+", "-", slug).strip("-").upper() or "PROJECT"

    directories = [
        "01_sources",
        "02_direction",
        "03_conte",
        "03_conte/reviews",
        "04_locks",
        "05_prompts",
        "06_candidates/current",
        "06_candidates/selected",
        "06_candidates/rejected",
        "06_candidates/legacy",
        "07_logs",
        "08_completion",
    ]
    for relative in directories:
        (target / relative).mkdir(parents=True, exist_ok=False)

    project_md = f"""# {title}

## Current State

- slug: `{slug}`
- stage: `source`
- status: `active`
- current_authority: `PROJECT.md`
- next_action: fill `01_sources/source_ledger.md`

## Director Decisions

- topic: pending
- sweet_spot: pending
- conte: pending
- generation_scope: not_authorized
- final_selection: pending

## Current Surfaces

- sources: `01_sources/source_ledger.md`
- direction: `02_direction/creative_brief.md`
- conte: `03_conte/image_ready_conte.md`
- locks: `04_locks/`
- provider prompts: `05_prompts/`
- current candidates: `06_candidates/current/`
- selected candidates: `06_candidates/selected/`
- logs: `07_logs/`
- completion: `08_completion/`

## Legacy Rule

Move superseded or rejected work out of current surfaces. Preserve it under `06_candidates/rejected` or `06_candidates/legacy`; do not delete evidence.
"""
    (target / "PROJECT.md").write_text(project_md, encoding="utf-8")

    copy_map = {
        "source_ledger.md": "01_sources/source_ledger.md",
        "creative_brief.md": "02_direction/creative_brief.md",
        "image_ready_conte.md": "03_conte/image_ready_conte.md",
        "visible_text_source_lock.csv": "04_locks/visible_text_source_lock.csv",
        "visible_text_routing_lock.csv": "04_locks/visible_text_routing_lock.csv",
        "page_cast_lock.csv": "04_locks/page_cast_lock.csv",
        "reference_manifest.csv": "04_locks/reference_manifest.csv",
        "generation_plan.csv": "04_locks/generation_plan.csv",
        "editorial_review_lock.csv": "04_locks/editorial_review_lock.csv",
        "panel_prompt.txt": "05_prompts/P001.txt",
    }
    for source_name, destination_name in copy_map.items():
        source = templates / source_name
        destination = target / destination_name
        shutil.copy2(source, destination)
        text = destination.read_text(encoding="utf-8").replace("PROJECT", code)
        destination.write_text(text, encoding="utf-8", newline="\n")

    for relative in [
        "06_candidates/current/.gitkeep",
        "03_conte/reviews/.gitkeep",
        "06_candidates/selected/.gitkeep",
        "06_candidates/rejected/.gitkeep",
        "06_candidates/legacy/.gitkeep",
        "07_logs/.gitkeep",
        "08_completion/.gitkeep",
    ]:
        (target / relative).write_text("", encoding="utf-8")

    return target


def main() -> int:
    args = parse_args()
    try:
        create_project(args.root, args.slug, args.title)
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"failed: {exc}")
        return 1
    print("PROJECT_CREATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
