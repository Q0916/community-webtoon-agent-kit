#!/usr/bin/env python3
"""Copy explicit final artifacts into a hash-verified completion archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_list(path: Path, project: Path) -> list[Path]:
    if not path.is_file():
        raise FileNotFoundError(path)
    result: list[Path] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        candidate = Path(value).expanduser()
        if not candidate.is_absolute():
            candidate = project / candidate
        candidate = candidate.resolve()
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
        result.append(candidate)
    if not result:
        raise ValueError(f"empty file list: {path}")
    return result


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[<>:\"/\\|?*]+", "_", value).strip(" .")
    return cleaned or "community-toon"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--name")
    parser.add_argument("--final-list", type=Path, required=True)
    parser.add_argument("--approved-list", type=Path, required=True)
    parser.add_argument("--materials-list", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.expanduser().resolve()
    if not (project / "PROJECT.md").is_file():
        print("failed: PROJECT.md missing")
        return 1
    try:
        groups = {
            "01_final": read_list(args.final_list.expanduser().resolve(), project),
            "02_approved_sources": read_list(args.approved_list.expanduser().resolve(), project),
            "03_used_materials": read_list(args.materials_list.expanduser().resolve(), project),
        }
    except (FileNotFoundError, ValueError) as exc:
        print(f"failed: {exc}")
        return 1

    name = safe_name(args.name or project.name)
    destination = args.archive_root.expanduser().resolve() / f"{date.today().isoformat()}_{name}"
    if destination.exists():
        print("failed: archive destination already exists")
        return 1

    for group_name, sources in groups.items():
        names = [source.name.casefold() for source in sources]
        if len(names) != len(set(names)):
            print(f"failed: duplicate filenames in {group_name}")
            return 1

    if not args.apply:
        total = sum(len(sources) for sources in groups.values())
        print(f"DRY_RUN_OK files={total}")
        return 0

    manifest: dict[str, object] = {
        "schema": "community-webtoon-completion-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project": str(project),
        "archive": str(destination),
        "groups": {},
    }
    destination.mkdir(parents=True)
    for group_name, sources in groups.items():
        group_dir = destination / group_name
        group_dir.mkdir()
        entries = []
        for source in sources:
            target = group_dir / source.name
            shutil.copy2(source, target)
            source_hash = sha256_file(source)
            target_hash = sha256_file(target)
            if source_hash != target_hash:
                print("failed: copy hash mismatch")
                return 1
            entries.append(
                {
                    "source": str(source),
                    "archived": str(target),
                    "bytes": target.stat().st_size,
                    "sha256": target_hash,
                }
            )
        manifest["groups"][group_name] = entries

    (destination / "ARCHIVE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (destination / "README.md").write_text(
        "# Completed Community Webtoon Archive\n\n"
        "This folder freezes viewing finals, exact user-approved sources, and materials actually used. "
        "See `ARCHIVE_MANIFEST.json` for provenance, sizes, and SHA-256 hashes.\n",
        encoding="utf-8",
    )
    print(f"ARCHIVE_CREATED files={sum(len(items) for items in groups.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
