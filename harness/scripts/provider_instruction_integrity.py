"""Transfer approved provider prose verbatim; keep amendments outside prompts."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def normalized(text):
    return text.replace('\r\n', '\n').replace('\r', '\n').lstrip('\ufeff')


def approved_body(source, amendments=None):
    raw = source.read_bytes()
    body = re.sub(r'\A---\n.*?\n---\n', '', normalized(raw.decode('utf-8')), count=1, flags=re.S).strip('\n')
    if amendments:
        data = json.loads(amendments.read_text(encoding='utf-8-sig'))
        if data.get('source_sha256') != hashlib.sha256(raw).hexdigest():
            raise ValueError('AMENDMENT_SOURCE_HASH_MISMATCH')
        for change in data['changes']:
            if not str(change.get('user_decision_reference', '')).strip() or not str(change.get('reason', '')).strip():
                raise ValueError('AMENDMENT_DECISION_AND_REASON_REQUIRED')
            before = normalized(change['before'])
            if not before or body.count(before) != 1:
                raise ValueError('AMENDMENT_TARGET_NOT_UNIQUE')
            body = body.replace(before, normalized(change['after']), 1)
    if not body.strip():
        raise ValueError('EMPTY_APPROVED_BODY')
    return body


def check(source, prompt_dir, amendments=None, glob='*.txt'):
    body = approved_body(source, amendments)
    files = sorted(prompt_dir.glob(glob))
    if not files:
        raise ValueError('NO_PROMPTS')
    missing = [p.name for p in files if body not in normalized(p.read_text(encoding='utf-8-sig'))]
    if missing:
        raise ValueError('PROVIDER_BODY_NOT_VERBATIM ' + ', '.join(missing))
    return len(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--amendments', type=Path)
    parser.add_argument('--prompt-dir', type=Path)
    parser.add_argument('--glob', default='*.txt')
    parser.add_argument('--emit', type=Path)
    args = parser.parse_args()
    try:
        if args.emit:
            if args.emit.exists():
                raise ValueError('OUTPUT_ALREADY_EXISTS')
            args.emit.write_text(approved_body(args.source, args.amendments) + '\n', encoding='utf-8')
        if args.prompt_dir:
            count = check(args.source, args.prompt_dir, args.amendments, args.glob)
            print(f'PROVIDER_INSTRUCTION_INTEGRITY_PASS prompts={count}')
        if not args.emit and not args.prompt_dir:
            parser.error('--emit or --prompt-dir required')
    except (ValueError, KeyError, OSError) as error:
        print(f'PROVIDER_INSTRUCTION_INTEGRITY_FAIL {error}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
