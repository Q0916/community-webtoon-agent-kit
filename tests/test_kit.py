from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "harness" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from freeze_completion import main as freeze_main  # noqa: E402
from init_project import create_project  # noqa: E402
from validate_project import run_validation  # noqa: E402


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


class KitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = create_project(self.root / "work", "demo-toon", "Demo Toon")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_valid_project(self) -> None:
        (self.project / "01_sources" / "source_ledger.md").write_text(
            "# Source Ledger\n\n"
            "| source_id | role | URL or local evidence | observed fact/reaction | usable phrase | confidence | use decision |\n"
            "|---|---|---|---|---|---|---|\n"
            "| S001 | primary_fact | https://example.com/post | A tool changed. | changed today | high | use |\n",
            encoding="utf-8",
        )
        (self.project / "02_direction" / "creative_brief.md").write_text(
            "# Creative Direction Brief\n\n"
            "## Director Intent\nShow the reversal.\n\n"
            "## Community Reader Payoff\nUse the observed phrase.\n\n"
            "## Comic Readability Need\nSetup, reversal, reaction.\n\n"
            "## Approved Sweet Spot\nA short reaction gag.\n\n"
            "## Approval\n- status: approved\n- approved_by: director\n- approved_at: 2026-01-01\n",
            encoding="utf-8",
        )
        (self.project / "03_conte" / "image_ready_conte.md").write_text(
            "# Image-Ready Conte\n\n"
            "## Version Lock\n\n"
            "- current_version: v3\n"
            "- draft_artifact: 03_conte/reviews/draft_v1.md\n"
            "- gemini_reviewed_version: v2\n"
            "- human_approved_version: v3\n\n"
            "## DEMO-TOON-PKT-001 - Setup\n\n"
            "- handoff_from_previous: Opening beat.\n"
            "- reader_first_sees: A quiet community board.\n"
            "- character_realizes: The headline changed.\n"
            "- push_to_next: The character reacts.\n"
            "- story_role: Setup and turn.\n"
            "- exact_visible_cast: CHAR001.\n"
            "- allowed_visible_objects: One board and one phone.\n"
            "- non_text_visual_information: Sudden body recoil.\n"
            "- background_budget: feed_board_only.\n"
            "- illustrated_block_boundaries: Two inset blocks.\n"
            "- visible_text_rows: TXT001.\n"
            "- positive_composition_lock: Board above, reaction below.\n"
            "- reference_roles: none for generic silhouette.\n"
            "- review_destination: current candidates.\n",
            encoding="utf-8",
        )
        reviews = self.project / "03_conte" / "reviews"
        (reviews / "draft_v1.md").write_text("# Draft v1\n", encoding="utf-8")
        (reviews / "gemini_v2.md").write_text("# Gemini review v2\n", encoding="utf-8")
        gemini_hash = hashlib.sha256((reviews / "gemini_v2.md").read_bytes()).hexdigest().upper()
        human_hash = hashlib.sha256((self.project / "03_conte" / "image_ready_conte.md").read_bytes()).hexdigest().upper()
        locks = self.project / "04_locks"
        write_csv(
            locks / "editorial_review_lock.csv",
            ["review_id", "reviewer_type", "reviewer_name", "input_conte_version", "output_conte_version", "artifact_path", "artifact_sha256", "status", "reviewed_at"],
            [
                ["REV001", "gemini", "Gemini", "v1", "v2", "03_conte/reviews/gemini_v2.md", gemini_hash, "completed", "2026-01-01"],
                ["REV002", "human", "Director", "v2", "v3", "03_conte/image_ready_conte.md", human_hash, "approved", "2026-01-02"],
            ],
        )
        write_csv(
            locks / "visible_text_source_lock.csv",
            ["text_id", "text", "type", "basis", "status"],
            [["TXT001", "오늘 바뀜", "gallery phrase", "S001", "approved"]],
        )
        write_csv(
            locks / "visible_text_routing_lock.csv",
            ["page_id", "text_id", "text_owner", "owner_role", "attachment_hint", "read_order"],
            [["P001", "TXT001", "BOARD001", "sign", "inside top board", "1"]],
        )
        write_csv(
            locks / "page_cast_lock.csv",
            ["page_id", "role_id", "visible", "reference_id", "acting_note"],
            [["P001", "CHAR001", "true", "", "recoil"]],
        )
        write_csv(
            locks / "reference_manifest.csv",
            ["reference_id", "role_id", "ref_role", "ref_path", "sha256", "visual_role_verified", "notes"],
            [],
        )
        write_csv(
            locks / "generation_plan.csv",
            ["page_id", "packet_id", "scene_relation", "runtime", "prompt_path", "output_dir", "status", "user_authorization_reference"],
            [["P001", "DEMO-TOON-PKT-001", "independent_page", "ima2-gen", "05_prompts/P001.txt", "06_candidates/current", "pending", "user-message"]],
        )
        prompt = (ROOT / "harness" / "templates" / "panel_prompt.txt").read_text(encoding="utf-8")
        values = {
            "Page ID:": "Page ID: P001",
            "Story role:": "Story role: setup and reversal",
            "Required source rows:": "Required source rows: S001",
            "Scene relation:": "Scene relation: independent_page",
            "Whole-comic story and reader-emotion sequence:": "Whole-comic story and reader-emotion sequence: quiet discovery, reversal, then amused release",
            "Why this page exists and state before/after:": "Why this page exists and state before/after: turn a neutral board into the cause of the reaction",
            "Fact/inference/MSG boundary:": "Fact/inference/MSG boundary: S001 fact; the reaction is approved MSG",
            "Exact visible cast and reference roles:": "Exact visible cast and reference roles: CHAR001, generic silhouette",
            "Scene-continuity references:": "Scene-continuity references: none",
            "Allowed visible object and information-prop inventory:": "Allowed visible object and information-prop inventory: board, phone",
            "Non-text visual information:": "Non-text visual information: recoil",
            "Background budget:": "Background budget: feed_board_only",
            "Illustrated-block and background boundaries:": "Illustrated-block and background boundaries: two insets",
            "Exact readable-text rows and owners:": "Exact readable-text rows and owners: TXT001 by BOARD001",
            "Bubble/caption/comment/SFX attachment plan:": "Bubble/caption/comment/SFX attachment plan: sign inside board",
            "Character posture, gesture, expression, silhouette, and color:": "Character posture, gesture, expression, silhouette, and color: sharp recoil, dark silhouette",
            "Camera and composition:": "Camera and composition: board above, reaction below",
            "Positive composition lock:": "Positive composition lock: two clean blocks",
            "Reference sanity check:": "Reference sanity check: no named character reference needed",
            "Review destination:": "Review destination: 06_candidates/current",
        }
        prompt = "\n".join(values.get(line, line) for line in prompt.splitlines()) + "\n"
        (self.project / "05_prompts" / "P001.txt").write_text(prompt, encoding="utf-8")

    def test_initializer_creates_expected_surfaces(self) -> None:
        self.assertTrue((self.project / "PROJECT.md").is_file())
        self.assertTrue((self.project / "05_prompts" / "P001.txt").is_file())
        self.assertTrue((self.project / "06_candidates" / "legacy").is_dir())

    def test_blank_project_fails_strict_pre_generation(self) -> None:
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertGreater(len(report.failures), 0)

    def test_filled_project_passes_strict_pre_generation(self) -> None:
        self.make_valid_project()
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "pass", report.failures)
        self.assertEqual(report.facts["packet_count"], 1)

    def test_gemini_and_human_conte_reviews_are_both_mandatory(self) -> None:
        self.make_valid_project()
        write_csv(
            self.project / "04_locks" / "editorial_review_lock.csv",
            ["review_id", "reviewer_type", "reviewer_name", "input_conte_version", "output_conte_version", "artifact_path", "artifact_sha256", "status", "reviewed_at"],
            [[
                "REV002",
                "human",
                "Director",
                "v2",
                "v3",
                "03_conte/image_ready_conte.md",
                hashlib.sha256((self.project / "03_conte" / "image_ready_conte.md").read_bytes()).hexdigest().upper(),
                "approved",
                "2026-01-02",
            ]],
        )
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("Gemini" in failure for failure in report.failures))

    def test_reference_hash_is_verified(self) -> None:
        self.make_valid_project()
        ref = self.project / "04_locks" / "character-ref.bin"
        ref.write_bytes(b"reference-bytes")
        digest = hashlib.sha256(ref.read_bytes()).hexdigest().upper()
        write_csv(
            self.project / "04_locks" / "reference_manifest.csv",
            ["reference_id", "role_id", "ref_role", "ref_path", "sha256", "visual_role_verified", "notes"],
            [["REF001", "CHAR001", "identity_primary", "04_locks/character-ref.bin", digest, "true", "checked"]],
        )
        write_csv(
            self.project / "04_locks" / "page_cast_lock.csv",
            ["page_id", "role_id", "visible", "reference_id", "acting_note"],
            [["P001", "CHAR001", "true", "REF001", "recoil"]],
        )
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "pass", report.failures)

    def test_scene_relation_must_be_declared(self) -> None:
        self.make_valid_project()
        write_csv(
            self.project / "04_locks" / "generation_plan.csv",
            ["page_id", "packet_id", "scene_relation", "runtime", "prompt_path", "output_dir", "status", "user_authorization_reference"],
            [["P001", "DEMO-TOON-PKT-001", "", "ima2-gen", "05_prompts/P001.txt", "06_candidates/current", "pending", "user-message"]],
        )
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("scene relation" in failure for failure in report.failures))

    def test_prompt_requires_shared_understanding_context(self) -> None:
        self.make_valid_project()
        prompt_path = self.project / "05_prompts" / "P001.txt"
        prompt = prompt_path.read_text(encoding="utf-8").replace(
            "Whole-comic story and reader-emotion sequence: quiet discovery, reversal, then amused release",
            "Whole-comic story and reader-emotion sequence:",
        )
        prompt_path.write_text(prompt, encoding="utf-8")
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("Whole-comic story" in failure for failure in report.failures))

    def test_generation_runtime_must_be_declared(self) -> None:
        self.make_valid_project()
        write_csv(
            self.project / "04_locks" / "generation_plan.csv",
            ["page_id", "packet_id", "scene_relation", "runtime", "prompt_path", "output_dir", "status", "user_authorization_reference"],
            [["P001", "DEMO-TOON-PKT-001", "independent_page", "", "05_prompts/P001.txt", "06_candidates/current", "pending", "user-message"]],
        )
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("generation runtime" in failure for failure in report.failures))

    def test_independent_page_rejects_continuity_reference(self) -> None:
        self.make_valid_project()
        prompt_path = self.project / "05_prompts" / "P001.txt"
        prompt = prompt_path.read_text(encoding="utf-8").replace(
            "Scene-continuity references: none",
            "Scene-continuity references: previous-page.png",
        )
        prompt_path.write_text(prompt, encoding="utf-8")
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("independent page" in failure for failure in report.failures))

    def test_continuing_scene_requires_reference(self) -> None:
        self.make_valid_project()
        write_csv(
            self.project / "04_locks" / "generation_plan.csv",
            ["page_id", "packet_id", "scene_relation", "runtime", "prompt_path", "output_dir", "status", "user_authorization_reference"],
            [["P001", "DEMO-TOON-PKT-001", "same_scene_continuation", "ima2-gen", "05_prompts/P001.txt", "06_candidates/current", "pending", "user-message"]],
        )
        prompt_path = self.project / "05_prompts" / "P001.txt"
        prompt = prompt_path.read_text(encoding="utf-8").replace(
            "Scene relation: independent_page",
            "Scene relation: same_scene_continuation",
        )
        prompt_path.write_text(prompt, encoding="utf-8")
        report = run_validation(self.project, "pre-generation", True)
        self.assertEqual(report.status, "fail")
        self.assertTrue(any("lacks a scene reference" in failure for failure in report.failures))

    def test_completion_archive_copies_and_hashes(self) -> None:
        files = []
        for name in ["final.txt", "approved.txt", "material.txt"]:
            path = self.project / "07_logs" / name
            path.write_text(name, encoding="utf-8")
            files.append(path)
        list_paths = []
        for index, source in enumerate(files):
            path = self.project / "07_logs" / f"list-{index}.txt"
            path.write_text(str(source) + "\n", encoding="utf-8")
            list_paths.append(path)

        old_argv = sys.argv
        try:
            sys.argv = [
                "freeze_completion.py",
                "--project",
                str(self.project),
                "--archive-root",
                str(self.root / "completed"),
                "--name",
                "demo",
                "--final-list",
                str(list_paths[0]),
                "--approved-list",
                str(list_paths[1]),
                "--materials-list",
                str(list_paths[2]),
                "--apply",
            ]
            self.assertEqual(freeze_main(), 0)
        finally:
            sys.argv = old_argv
        manifests = list((self.root / "completed").glob("*/ARCHIVE_MANIFEST.json"))
        self.assertEqual(len(manifests), 1)
        data = json.loads(manifests[0].read_text(encoding="utf-8"))
        self.assertEqual(sum(len(group) for group in data["groups"].values()), 3)


if __name__ == "__main__":
    unittest.main()
