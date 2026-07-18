#!/usr/bin/env python3
"""Validate objective community-webtoon production gates without judging image taste."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


STAGE_ORDER = {
    "source": 1,
    "direction": 2,
    "conte": 3,
    "pre-generation": 4,
}

PACKET_FIELDS = [
    "handoff_from_previous",
    "reader_first_sees",
    "character_realizes",
    "push_to_next",
    "story_role",
    "exact_visible_cast",
    "allowed_visible_objects",
    "non_text_visual_information",
    "background_budget",
    "illustrated_block_boundaries",
    "positive_composition_lock",
    "review_destination",
]

PROMPT_TOKENS = [
    "COMMUNITY_TOON_GENERATION_CONTRACT_V1",
    "page_canvas_lock",
    "white_gutter_lock",
    "outside_text_space",
    "Exact visible cast and reference roles:",
    "Allowed visible object and information-prop inventory:",
    "Exact readable-text rows and owners:",
    "Background budget:",
    "Positive composition lock:",
]


@dataclass
class Report:
    project: str
    stage: str
    strict: bool
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts: dict[str, object] = field(default_factory=dict)

    @property
    def status(self) -> str:
        return "pass" if not self.failures else "fail"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "project": self.project,
            "stage": self.stage,
            "strict": self.strict,
            "failures": self.failures,
            "warnings": self.warnings,
            "facts": self.facts,
        }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_csv(path: Path, report: Report) -> list[dict[str, str]]:
    if not path.is_file():
        report.failures.append(f"missing file: {path.name}")
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def value_after_label(section: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.*)$", section, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def validate_source(project: Path, report: Report) -> None:
    path = project / "01_sources" / "source_ledger.md"
    if not path.is_file():
        report.failures.append("missing source ledger")
        return
    text = path.read_text(encoding="utf-8")
    roles = {"primary_fact", "mood_source", "MSG", "do_not_use"}
    report.facts["source_roles_present"] = sorted(role for role in roles if role in text)
    if report.strict:
        data_rows = [line for line in text.splitlines() if line.startswith("|") and "S00" in line]
        filled = [line for line in data_rows if "URL or local evidence" not in line and not re.search(r"\|\s*\|\s*\|", line)]
        if not filled:
            report.failures.append("source ledger has no filled evidence row")


def validate_direction(project: Path, report: Report) -> None:
    path = project / "02_direction" / "creative_brief.md"
    if not path.is_file():
        report.failures.append("missing creative direction brief")
        return
    text = path.read_text(encoding="utf-8")
    for heading in ["Director Intent", "Community Reader Payoff", "Comic Readability Need", "Approved Sweet Spot"]:
        if f"## {heading}" not in text:
            report.failures.append(f"direction brief missing heading: {heading}")
    if report.strict:
        if re.search(r"- status:\s*approved\b", text, flags=re.IGNORECASE) is None:
            report.failures.append("creative direction is not approved")
        if text.count("TBD"):
            report.failures.append("creative direction still contains TBD")


def validate_conte(project: Path, report: Report) -> set[str]:
    path = project / "03_conte" / "image_ready_conte.md"
    if not path.is_file():
        report.failures.append("missing image-ready conte")
        return set()
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+([A-Z0-9-]+-PKT-\d+)\s+-.*$", text, flags=re.MULTILINE))
    packet_ids = [match.group(1) for match in matches]
    if not packet_ids:
        report.failures.append("conte has no packet heading")
        return set()
    if len(packet_ids) != len(set(packet_ids)):
        report.failures.append("conte has duplicate packet IDs")
    report.facts["packet_count"] = len(packet_ids)
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.start():end]
        for label in PACKET_FIELDS:
            value = value_after_label(section, label)
            if not value:
                report.failures.append(f"{packet_ids[index]} missing value: {label}")
    return set(packet_ids)


def validate_pre_generation(project: Path, report: Report, packet_ids: set[str]) -> None:
    lock_dir = project / "04_locks"
    editorial_rows = read_csv(lock_dir / "editorial_review_lock.csv", report)
    source_rows = read_csv(lock_dir / "visible_text_source_lock.csv", report)
    routing_rows = read_csv(lock_dir / "visible_text_routing_lock.csv", report)
    cast_rows = read_csv(lock_dir / "page_cast_lock.csv", report)
    reference_rows = read_csv(lock_dir / "reference_manifest.csv", report)
    plan_rows = read_csv(lock_dir / "generation_plan.csv", report)

    conte_path = project / "03_conte" / "image_ready_conte.md"
    conte_text = conte_path.read_text(encoding="utf-8") if conte_path.is_file() else ""
    current_match = re.search(r"^- current_version:\s*(\S+)\s*$", conte_text, flags=re.MULTILINE)
    gemini_version_match = re.search(r"^- gemini_reviewed_version:\s*(\S+)\s*$", conte_text, flags=re.MULTILINE)
    human_version_match = re.search(r"^- human_approved_version:\s*(\S+)\s*$", conte_text, flags=re.MULTILINE)
    current_version = current_match.group(1) if current_match else ""
    gemini_version = gemini_version_match.group(1) if gemini_version_match else ""
    human_version = human_version_match.group(1) if human_version_match else ""
    if not current_version:
        report.failures.append("conte current_version is missing")
    if not gemini_version:
        report.failures.append("conte gemini_reviewed_version is missing")
    if not human_version:
        report.failures.append("conte human_approved_version is missing")
    if current_version and human_version and current_version != human_version:
        report.failures.append("human-approved conte version does not match current_version")

    valid_editorial: dict[str, list[dict[str, str]]] = {"gemini": [], "human": []}
    for row in editorial_rows:
        reviewer_type = (row.get("reviewer_type") or "").strip().lower()
        status = (row.get("status") or "").strip().lower()
        input_version = (row.get("input_conte_version") or "").strip()
        output_version = (row.get("output_conte_version") or "").strip()
        artifact_raw = (row.get("artifact_path") or "").strip()
        artifact_hash = (row.get("artifact_sha256") or "").strip().upper()
        reviewed_at = (row.get("reviewed_at") or "").strip()
        if reviewer_type not in valid_editorial:
            continue
        allowed_status = {"reviewed", "completed", "approved", "final"}
        if status not in allowed_status or not input_version or not output_version or not artifact_raw or not reviewed_at:
            continue
        artifact = Path(artifact_raw)
        if not artifact.is_absolute():
            artifact = project / artifact
        if not artifact.is_file():
            report.failures.append(f"editorial review artifact missing: {reviewer_type}")
            continue
        if not artifact_hash or sha256_file(artifact) != artifact_hash:
            report.failures.append(f"editorial review artifact hash mismatch: {reviewer_type}")
            continue
        valid_editorial[reviewer_type].append(row)

    if not valid_editorial["gemini"]:
        report.failures.append("missing completed Gemini conte review/version-up evidence")
    if not valid_editorial["human"]:
        report.failures.append("missing completed human conte approval evidence")
    if valid_editorial["gemini"] and gemini_version:
        outputs = {(row.get("output_conte_version") or "").strip() for row in valid_editorial["gemini"]}
        if gemini_version not in outputs:
            report.failures.append("Gemini review output version does not match conte version lock")
    if valid_editorial["human"] and current_version:
        outputs = {(row.get("output_conte_version") or "").strip() for row in valid_editorial["human"]}
        if current_version not in outputs:
            report.failures.append("human review output version does not match current conte version")
    report.facts["editorial_review_gate"] = {
        "gemini": bool(valid_editorial["gemini"]),
        "human": bool(valid_editorial["human"]),
        "current_version": current_version,
    }

    approved_text_ids: set[str] = set()
    for row in source_rows:
        text_id = (row.get("text_id") or "").strip()
        status = (row.get("status") or "").strip().lower()
        text = (row.get("text") or "").strip()
        if not text_id or not text:
            report.failures.append("visible-text source lock contains an empty ID or text")
            continue
        if status in {"", "pending", "needs user approval", "hold"}:
            report.failures.append(f"visible text is not approved: {text_id}")
        else:
            approved_text_ids.add(text_id)

    routed_ids = {(row.get("text_id") or "").strip() for row in routing_rows}
    for text_id in approved_text_ids - routed_ids:
        report.failures.append(f"approved text lacks routing row: {text_id}")
    for row in routing_rows:
        for key in ["page_id", "text_id", "text_owner", "owner_role", "attachment_hint", "read_order"]:
            if not (row.get(key) or "").strip():
                report.failures.append(f"routing row missing {key}: {(row.get('text_id') or 'unknown')}")

    references = {(row.get("reference_id") or "").strip(): row for row in reference_rows if (row.get("reference_id") or "").strip()}
    for row in cast_rows:
        if (row.get("visible") or "").strip().lower() not in {"true", "yes", "1"}:
            continue
        reference_id = (row.get("reference_id") or "").strip()
        if not reference_id:
            continue
        if reference_id not in references:
            report.failures.append(f"cast row points to unknown reference: {reference_id}")

    seen_hash_roles: dict[str, str] = {}
    for reference_id, row in references.items():
        raw_path = (row.get("ref_path") or "").strip()
        expected = (row.get("sha256") or "").strip().upper()
        verified = (row.get("visual_role_verified") or "").strip().lower()
        if not raw_path:
            report.failures.append(f"reference path is empty: {reference_id}")
            continue
        path = Path(raw_path)
        if not path.is_absolute():
            path = project / path
        if not path.is_file():
            report.failures.append(f"reference file missing: {reference_id}")
            continue
        actual = sha256_file(path)
        if not expected or actual != expected:
            report.failures.append(f"reference hash mismatch: {reference_id}")
        if verified not in {"true", "yes", "1"}:
            report.failures.append(f"reference visual role not human-verified: {reference_id}")
        role_id = (row.get("role_id") or "").strip()
        if actual in seen_hash_roles and seen_hash_roles[actual] != role_id:
            report.failures.append(f"different roles share one reference hash: {seen_hash_roles[actual]} and {role_id}")
        seen_hash_roles[actual] = role_id

    if not plan_rows:
        report.failures.append("generation plan is empty")
        return
    page_ids: set[str] = set()
    for row in plan_rows:
        page_id = (row.get("page_id") or "").strip()
        packet_id = (row.get("packet_id") or "").strip()
        prompt_raw = (row.get("prompt_path") or "").strip()
        if not page_id or not packet_id or not prompt_raw:
            report.failures.append("generation plan row has empty page, packet, or prompt")
            continue
        if page_id in page_ids:
            report.failures.append(f"duplicate page ID in generation plan: {page_id}")
        page_ids.add(page_id)
        if packet_id not in packet_ids:
            report.failures.append(f"generation plan references unknown packet: {packet_id}")
        prompt_path = Path(prompt_raw)
        if not prompt_path.is_absolute():
            prompt_path = project / prompt_path
        if not prompt_path.is_file():
            report.failures.append(f"provider prompt missing: {page_id}")
            continue
        prompt = prompt_path.read_text(encoding="utf-8")
        for token in PROMPT_TOKENS:
            if token not in prompt:
                report.failures.append(f"{page_id} prompt missing contract token: {token}")
        for label in [
            "Page ID",
            "Story role",
            "Required source rows",
            "Exact visible cast and reference roles",
            "Allowed visible object and information-prop inventory",
            "Background budget",
            "Exact readable-text rows and owners",
            "Positive composition lock",
            "Review destination",
        ]:
            match = re.search(rf"^{re.escape(label)}:\s*(.*)$", prompt, flags=re.MULTILINE)
            if not match or not match.group(1).strip():
                report.failures.append(f"{page_id} prompt has empty field: {label}")
        negative_terms = re.findall(r"\b(?:without|avoid)\b|금지|없게", prompt, flags=re.IGNORECASE)
        if negative_terms:
            report.warnings.append(f"{page_id} provider prompt contains negative construction terms")

    cast_pages = {(row.get("page_id") or "").strip() for row in cast_rows if (row.get("page_id") or "").strip()}
    routing_pages = {(row.get("page_id") or "").strip() for row in routing_rows if (row.get("page_id") or "").strip()}
    for page_id in page_ids - cast_pages:
        report.failures.append(f"generation page lacks cast lock: {page_id}")
    for page_id in page_ids - routing_pages:
        report.failures.append(f"generation page lacks text routing: {page_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--stage", choices=STAGE_ORDER, required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def run_validation(project: Path, stage: str, strict: bool) -> Report:
    project = project.expanduser().resolve()
    report = Report(project=str(project), stage=stage, strict=strict)
    if not (project / "PROJECT.md").is_file():
        report.failures.append("missing PROJECT.md")
        return report
    validate_source(project, report)
    if STAGE_ORDER[stage] >= STAGE_ORDER["direction"]:
        validate_direction(project, report)
    packet_ids: set[str] = set()
    if STAGE_ORDER[stage] >= STAGE_ORDER["conte"]:
        packet_ids = validate_conte(project, report)
    if STAGE_ORDER[stage] >= STAGE_ORDER["pre-generation"]:
        validate_pre_generation(project, report, packet_ids)
    return report


def main() -> int:
    args = parse_args()
    report = run_validation(args.project, args.stage, args.strict)
    report_path = args.report or (args.project / "07_logs" / f"validation_{args.stage}.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"VALIDATION_{report.status.upper()} failures={len(report.failures)} warnings={len(report.warnings)}")
    print(f"REPORT={report_path}")
    return 0 if report.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
