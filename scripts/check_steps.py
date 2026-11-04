#!/usr/bin/env python3
"""Check that every Gherkin step in features/ uses a sentence from the glossary catalog.

Usage: python3 scripts/check_steps.py [--stats]
Exit code 1 if any step is not in the catalog.
"""
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "docs" / "glossary.md"
FEATURES = ROOT / "features"

STEP_KEYWORDS = ("조건", "먼저", "만일", "만약", "그러면", "그리고", "하지만", "단", "*")
PARTICLES = {
    "이/가": "(?:이|가)",
    "을/를": "(?:을|를)",
    "은/는": "(?:은|는)",
    "와/과": "(?:와|과)",
    "으로/로": "(?:으로|로)",
}
KIND = "(?:반복 TODO|TODO|이슈|배포|알림|프로젝트|업무|고객사)"
ATTRIBUTE = "[가-힣A-Za-z ]+?"
VALUE = '"[^"]*"'


def load_catalog() -> list[tuple[str, re.Pattern[str]]]:
    text = GLOSSARY.read_text(encoding="utf-8")
    blocks = re.findall(r"```steps\n(.*?)```", text, re.S)
    sentences = [line.strip() for block in blocks for line in block.splitlines() if line.strip()]
    return [(s, to_regex(s)) for s in sentences]


def to_regex(sentence: str) -> re.Pattern[str]:
    sentence = sentence.removesuffix(":표").strip()
    parts = re.split(r"(\{[^}]+\}|이/가|을/를|은/는|와/과|으로/로)", sentence)
    out = []
    for part in parts:
        if part == "{종류}":
            out.append(KIND)
        elif part == "{속성}":
            out.append(ATTRIBUTE)
        elif part.startswith("{"):
            out.append(VALUE)
        elif part in PARTICLES:
            out.append(PARTICLES[part])
        else:
            out.append(re.escape(part))
    return re.compile("".join(out))


def iter_steps() -> Iterator[tuple[str, int, str]]:
    for path in sorted(FEATURES.glob("*.feature")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            keyword = next((k for k in STEP_KEYWORDS if line.startswith(k + " ")), None)
            if keyword:
                text = line[len(keyword) + 1:].strip()
                # Scenario Outline placeholders always sit inside quoted values.
                text = re.sub(r"<[^>]+>", "X", text)
                yield path.name, lineno, text


def main() -> int:
    catalog = load_catalog()
    usage = Counter()
    unmatched = []
    total = 0
    for name, lineno, text in iter_steps():
        total += 1
        match = next((s for s, rx in catalog if rx.fullmatch(text)), None)
        if match:
            usage[match] += 1
        else:
            unmatched.append(f"{name}:{lineno}: {text}")

    print(f"steps: {total}, catalog sentences: {len(catalog)}, used: {len(usage)}")
    if "--stats" in sys.argv:
        for sentence, n in usage.most_common():
            print(f"{n:4} {sentence}")
        unused = [s for s, _ in catalog if s not in usage]
        if unused:
            print("\nunused catalog sentences:")
            for s in unused:
                print(f"     {s}")
    if unmatched:
        print(f"\n{len(unmatched)} step(s) not in docs/glossary.md catalog:")
        print("\n".join(unmatched))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
