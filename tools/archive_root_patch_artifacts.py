"""Archive root-level ALETHEIA patch artifacts without deleting the audit trail.

Patch 143 adds this helper for repository hygiene. It moves historical
PATCH_*_MANIFEST.txt and PATCH_*_RECOVERY_NOTE.md files from the repository
root into docs/patch_archive/. It is intentionally explicit and local-only.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = ROOT / "docs" / "patch_archive"


def _target_for(path: Path) -> Path | None:
    name = path.name
    if not name.startswith("PATCH_"):
        return None
    if name.endswith("_MANIFEST.txt"):
        return ARCHIVE_ROOT / "manifests" / name
    if name.endswith("_RECOVERY_NOTE.md"):
        return ARCHIVE_ROOT / "recovery_notes" / name
    return None


def discover_patch_artifacts(root: Path = ROOT) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        target = _target_for(path)
        if target is not None:
            pairs.append((path, target))
    return pairs


def archive_patch_artifacts(*, dry_run: bool = False) -> list[tuple[str, str]]:
    moved: list[tuple[str, str]] = []
    for source, target in discover_patch_artifacts(ROOT):
        moved.append((source.relative_to(ROOT).as_posix(), target.relative_to(ROOT).as_posix()))
        if dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            # Preserve existing archived copy and remove the root duplicate.
            source.unlink()
        else:
            shutil.move(str(source), str(target))
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive ALETHEIA root patch artifacts without deleting the audit trail.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned moves without changing files.")
    args = parser.parse_args()
    moves = archive_patch_artifacts(dry_run=args.dry_run)
    mode = "DRY RUN" if args.dry_run else "ARCHIVED"
    print(f"{mode}: {len(moves)} patch artifacts")
    for source, target in moves:
        print(f"- {source} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
