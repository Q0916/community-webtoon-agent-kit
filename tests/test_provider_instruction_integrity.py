import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness" / "scripts"))

from provider_instruction_integrity import approved_body, check


class InstructionIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'SKILL.md'
        self.source.write_text('---\nname: example\n---\n\nWHY: preserve cause and context.\nPlease cooperate.\nKeep the focal face large.\n', encoding='utf-8')
        self.prompts = self.root / 'prompts'
        self.prompts.mkdir()
        self.prompt = self.prompts / 'P001.txt'

    def test_full_body_and_scene_pass(self):
        self.prompt.write_text('Scene context\n' + approved_body(self.source) + '\nScene action', encoding='utf-8')
        self.assertEqual(check(self.source, self.prompts), 1)

    def test_keyword_summary_fails(self):
        self.prompt.write_text('WHY: cooperate; focus face.', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'NOT_VERBATIM'):
            check(self.source, self.prompts)

    def test_single_missing_sentence_and_missing_page_fail(self):
        self.prompt.write_text(approved_body(self.source), encoding='utf-8')
        (self.prompts / 'P002.txt').write_text(approved_body(self.source).replace('Keep the focal face large.', ''), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'P002'):
            check(self.source, self.prompts)

    def test_line_endings_only_are_normalized(self):
        self.prompt.write_bytes(approved_body(self.source).replace('\n', '\r\n').encode('utf-8'))
        self.assertEqual(check(self.source, self.prompts), 1)

    def amendment(self, reference='User: change this sentence'):
        p = self.root / 'amendments.json'
        p.write_text(json.dumps({'source_sha256': hashlib.sha256(self.source.read_bytes()).hexdigest(), 'changes': [{'before': 'Please cooperate.', 'after': 'Please help with this aim.', 'reason': 'User requested wording change only.', 'user_decision_reference': reference}]}), encoding='utf-8')
        return p

    def test_exact_amendment_and_stale_source(self):
        amendments = self.amendment()
        body = approved_body(self.source, amendments)
        self.assertIn('WHY: preserve cause and context.', body)
        self.prompt.write_text(body, encoding='utf-8')
        self.assertEqual(check(self.source, self.prompts, amendments), 1)
        self.source.write_text('new source', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'HASH_MISMATCH'):
            approved_body(self.source, amendments)

    def test_missing_decision_fails(self):
        with self.assertRaisesRegex(ValueError, 'DECISION'):
            approved_body(self.source, self.amendment(''))


if __name__ == '__main__':
    unittest.main()
