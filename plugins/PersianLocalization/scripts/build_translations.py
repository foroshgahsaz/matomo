#!/usr/bin/env python3
"""
Build plugins/PersianLocalization/lang/fa.json with missing Persian strings.
Run after Matomo upgrade to fill new English keys. Requires argostranslate + en→fa language pack.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import argostranslate.translate

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1] / "lang" / "fa.json"

PLACEHOLDER_RE = re.compile(
    r"(%+\d*\$?[sdif]|%\d*\$?[sdif]|%%|<[^>]+>|&[a-zA-Z]+;|\{[a-zA-Z0-9_]+\})"
)


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


PLUGIN_LANG_DIR = Path(__file__).resolve().parents[1] / "lang"


def merge_fa() -> dict:
    merged: dict = {}
    dirs = [ROOT / "lang"] + sorted(ROOT.glob("plugins/*/lang"), key=lambda p: str(p).lower())
    for d in dirs:
        if d.resolve() == PLUGIN_LANG_DIR.resolve():
            continue
        fa = d / "fa.json"
        if not fa.is_file():
            continue
        data = load_json(fa)
        for ns, keys in data.items():
            if not isinstance(keys, dict):
                continue
            merged.setdefault(ns, {}).update(keys)
    return merged


def merge_en() -> dict:
    merged: dict = {}
    dirs = [ROOT / "lang"] + sorted(ROOT.glob("plugins/*/lang"), key=lambda p: str(p).lower())
    for d in dirs:
        en = d / "en.json"
        if not en.is_file():
            continue
        data = load_json(en)
        for ns, keys in data.items():
            if not isinstance(keys, dict):
                continue
            merged.setdefault(ns, {}).update(keys)
    return merged


def protect(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(match: re.Match) -> str:
        tokens.append(match.group(0))
        return f"__PH{len(tokens) - 1}__"

    return PLACEHOLDER_RE.sub(repl, text), tokens


def restore(text: str, tokens: list[str]) -> str:
    for i, token in enumerate(tokens):
        text = text.replace(f"__PH{i}__", token)
    return text


def post_process(text: str) -> str:
    return (
        text.replace("Matomo", "ماتومو")
        .replace("PIWIK", "ماتومو")
        .replace("Piwik", "ماتومو")
    )


LATIN_RE = re.compile(r"[A-Za-z]{3,}")
PERSIAN_RE = re.compile(r"[\u0600-\u06FF]")


def needs_override(en_value: str, fa_value: str | None) -> bool:
    if fa_value is None:
        return True
    if fa_value == en_value:
        return True
    if LATIN_RE.search(fa_value) and not PERSIAN_RE.search(fa_value):
        return True
    return False


def collect_missing(en: dict, fa: dict) -> dict:
    overrides: dict = {}
    for ns, keys in en.items():
        for key, value in keys.items():
            if not isinstance(value, str):
                continue
            current = fa.get(ns, {}).get(key)
            if needs_override(value, current):
                overrides.setdefault(ns, {})[key] = value
    return overrides


def should_skip_machine_translation(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return True
    if re.fullmatch(r"[A-Za-z0-9_\-\.]+", stripped):
        return True
    return False


def translate_one(text: str) -> str:
    if should_skip_machine_translation(text):
        return post_process(text)
    protected, tokens = protect(text)
    try:
        raw = argostranslate.translate.translate(protected, "en", "fa")
        if raw:
            return post_process(restore(raw, tokens))
    except Exception:
        pass
    return post_process(text)


def translate_batch(strings: list[str]) -> list[str]:
    return [translate_one(s) for s in strings]


def main() -> None:
    en = merge_en()
    fa = merge_fa()
    overrides = collect_missing(en, fa)

    flat: list[tuple[str, str, str]] = []
    for ns, keys in overrides.items():
        for key, value in keys.items():
            flat.append((ns, key, value))

    print(f"Missing keys to translate: {len(flat)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)

    batch_size = 50

    for i in range(0, len(flat), batch_size):
        batch = flat[i : i + batch_size]
        texts = [b[2] for b in batch]
        translated = translate_batch(texts)
        for (ns, key, _), tr in zip(batch, translated):
            overrides[ns][key] = tr
        done = min(i + batch_size, len(flat))
        print(f"  translated {done}/{len(flat)}", flush=True)
        if done % 200 == 0 or done == len(flat):
            with OUT.open("w", encoding="utf-8") as f:
                json.dump(overrides, f, ensure_ascii=False, indent=2)
                f.write("\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(overrides, f, ensure_ascii=False, indent=4)
        f.write("\n")

    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
