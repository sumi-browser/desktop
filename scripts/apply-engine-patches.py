"""
engine/ への手動パッチを再適用するスクリプト。
surfer reset / surfer download --force 後に実行する。

Usage:
    python scripts/apply-engine-patches.py
"""

import re
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent / "engine"


def patch_mozconfig_utf8():
    """mozconfig.py: Japanese Windows での UnicodeDecodeError を修正。
    subprocess.check_output() に errors='replace' を追加。
    """
    target = ENGINE / "python/mozbuild/mozbuild/mozconfig.py"
    if not target.exists():
        print(f"  SKIP: {target} not found")
        return False

    content = target.read_text(encoding="utf-8")

    if 'errors="replace"' in content:
        print("  SKIP: already patched")
        return False

    # encoding="utf-8" の次の行に errors="replace" を追加
    old = """                encoding="utf-8",
            )"""
    new = """                encoding="utf-8",
                errors="replace",
            )"""

    if old not in content:
        print("  WARN: expected pattern not found, manual patch needed")
        return False

    content = content.replace(old, new)
    target.write_text(content, encoding="utf-8")
    print("  OK: added errors='replace' to subprocess.check_output()")
    return True


def patch_unified_prefix():
    """data.py: Unified ファイル名の切り詰めロジックを修正。
    末尾20文字ではなく最後のパスコンポーネントを使い、衝突を回避。
    """
    target = ENGINE / "python/mozbuild/mozbuild/frontend/data.py"
    if not target.exists():
        print(f"  SKIP: {target} not found")
        return False

    content = target.read_text(encoding="utf-8")

    if "last_component = unified_prefix.rsplit" in content:
        print("  SKIP: already patched")
        return False

    old = """            unified_prefix = context.relsrcdir
            if len(unified_prefix) > 20:
                unified_prefix = unified_prefix[-20:].split("/", 1)[-1]
            unified_prefix = unified_prefix.replace("/", "_")"""

    new = """            unified_prefix = context.relsrcdir
            if len(unified_prefix) > 20:
                # Take the last path component to preserve uniqueness,
                # then truncate if still too long.
                last_component = unified_prefix.rsplit("/", 1)[-1]
                if len(last_component) > 20:
                    last_component = last_component[-20:]
                unified_prefix = last_component
            unified_prefix = unified_prefix.replace("/", "_")"""

    if old not in content:
        print("  WARN: expected pattern not found, manual patch needed")
        return False

    content = content.replace(old, new)
    target.write_text(content, encoding="utf-8")
    print("  OK: fixed unified prefix truncation logic")
    return True


def main():
    print("Applying engine patches...")
    print()

    print("[1/2] mozconfig.py UTF-8 fix:")
    patch_mozconfig_utf8()
    print()

    print("[2/2] data.py unified prefix fix:")
    patch_unified_prefix()
    print()

    print("Done.")


if __name__ == "__main__":
    main()
