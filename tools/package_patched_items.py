"""Package only patched ALETHEIA files listed in a manifest.

Usage:
    python tools/package_patched_items.py PATCH_36_1_MANIFEST.txt ALETHEIA_patch36_1_patched_items_only.zip
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_manifest(path: Path) -> list[str]:
    items: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        items.append(line.replace("\\", "/"))
    return items


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python tools/package_patched_items.py <manifest.txt> <output.zip>")
        return 2
    manifest = ROOT / argv[1]
    output = ROOT / argv[2]
    if not manifest.exists():
        print(f"Manifest not found: {manifest}")
        return 1
    items = read_manifest(manifest)
    if not items:
        print("Manifest is empty.")
        return 1
    missing = [item for item in items if not (ROOT / item).exists()]
    if missing:
        print("Missing manifest items:")
        for item in missing:
            print(f" - {item}")
        return 1
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            zf.write(ROOT / item, item)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
