#!/usr/bin/env python3
"""Verify that the public kit is portable, text-first, and free of generated media."""

from __future__ import annotations

import re
from pathlib import Path


MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".psd", ".clip"}
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "skills/community-webtoon-producer/SKILL.md",
    "docs/QUALITY_CONTRACT.md",
    "docs/PROVIDER_ADAPTER.md",
    "harness/scripts/init_project.py",
    "harness/scripts/validate_project.py",
    "harness/scripts/freeze_completion.py",
    "harness/templates/panel_prompt.txt",
    "harness/templates/editorial_review_lock.csv",
]
FORBIDDEN_TEXT = [
    re.compile("D:" + r"\\image", re.IGNORECASE),
    re.compile("C:" + r"\\Users\\" + "fatel", re.IGNORECASE),
    re.compile("gho" + r"_[A-Za-z0-9_]+"),
]


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    failures: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            failures.append(f"missing: {relative}")

    media = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in MEDIA_SUFFIXES]
    for path in media:
        failures.append(f"media file tracked in kit: {path.relative_to(root)}")

    for path in root.rglob("*"):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix.lower() in MEDIA_SUFFIXES
            or path.suffix.lower() in {".pyc", ".pyo"}
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF8 file: {path.relative_to(root)}")
            continue
        for pattern in FORBIDDEN_TEXT:
            if pattern.search(text):
                failures.append(f"private/local path or token pattern: {path.relative_to(root)}")

    skill = root / "skills" / "community-webtoon-producer" / "SKILL.md"
    if skill.is_file():
        header = skill.read_text(encoding="utf-8").split("---", 2)
        if len(header) < 3 or "name: community-webtoon-producer" not in header[1] or "description:" not in header[1]:
            failures.append("invalid skill frontmatter")

    if failures:
        print(f"REPOSITORY_VERIFY_FAIL failures={len(failures)}")
        for failure in failures:
            print(f"- {failure}")
        return 1
    files = sum(
        1
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    print(f"REPOSITORY_VERIFY_PASS files={files} media=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
