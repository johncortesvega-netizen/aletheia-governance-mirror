"""Archive root-level ALETHEIA patch artifacts without deleting the audit trail.

Patch 147 turns this into the standard root-hygiene helper: keep only the
current patch manifest/recovery note visible at the repository root, then move
older patch artifacts into docs/patch_archive/.

The helper is intentionally local-only. It performs file moves inside the
checkout and never contacts a network service.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = ROOT / "docs" / "patch_archive"
PATCH_RE = re.compile(r"^PATCH_(?P<patch>[0-9]+(?:_[0-9]+)*)_(?:MANIFEST\.txt|RECOVERY_NOTE\.md)$")


def _patch_sort_key(patch_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in patch_id.split("_"))


def discover_latest_patch_id(root: Path = ROOT) -> str | None:
    """Return the highest patch id found in root patch manifest/recovery names."""
    patch_ids: set[str] = set()
    for path in root.iterdir():
        if not path.is_file():
            continue
        match = PATCH_RE.match(path.name)
        if match:
            patch_ids.add(match.group("patch"))
    if not patch_ids:
        return None
    return sorted(patch_ids, key=_patch_sort_key)[-1]


def _target_for(path: Path) -> Path | None:
    name = path.name
    if name.endswith("_MANIFEST.txt"):
        return ARCHIVE_ROOT / "manifests" / name
    if name.endswith("_RECOVERY_NOTE.md"):
        return ARCHIVE_ROOT / "recovery_notes" / name
    if name.startswith("PATCH_README"):
        return ARCHIVE_ROOT / "other_patch_artifacts" / name
    return None


def _is_current_patch_file(path: Path, current_patch: str | None) -> bool:
    if not current_patch:
        return False
    return path.name.startswith(f"PATCH_{current_patch}_")


def discover_patch_artifacts(
    root: Path = ROOT,
    *,
    current_patch: str | None = None,
    keep_current: bool = True,
) -> list[tuple[Path, Path]]:
    """Return root patch artifacts that should move into the archive."""
    pairs: list[tuple[Path, Path]] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        if path.name == "PATCH_STATUS.md":
            continue
        target = _target_for(path)
        if target is None:
            continue
        if keep_current and _is_current_patch_file(path, current_patch):
            continue
        pairs.append((path, target))
    return pairs


def archive_patch_artifacts(
    *,
    current_patch: str | None = None,
    keep_current: bool = True,
    dry_run: bool = False,
) -> list[tuple[str, str]]:
    """Archive historical patch artifacts and return source/target pairs.

    If current_patch is omitted, the helper auto-detects the highest patch id
    visible at the root and keeps that patch visible by default.
    """
    selected_current = current_patch or discover_latest_patch_id(ROOT)
    moved: list[tuple[str, str]] = []
    for source, target in discover_patch_artifacts(
        ROOT,
        current_patch=selected_current,
        keep_current=keep_current,
    ):
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
    parser.add_argument(
        "--current-patch",
        default=None,
        help="Patch id to keep visible at root, e.g. 147 or 146_1. Defaults to the highest root patch id.",
    )
    parser.add_argument(
        "--archive-current",
        action="store_true",
        help="Archive every root patch artifact, including the current one. Usually not wanted.",
    )
    args = parser.parse_args()
    moves = archive_patch_artifacts(
        current_patch=args.current_patch,
        keep_current=not args.archive_current,
        dry_run=args.dry_run,
    )
    mode = "DRY RUN" if args.dry_run else "ARCHIVED"
    current = args.current_patch or discover_latest_patch_id(ROOT) or "none"
    keep_note = "keeping current patch visible" if not args.archive_current else "including current patch"
    print(f"{mode}: {len(moves)} patch artifacts ({keep_note}; current={current})")
    for source, target in moves:
        print(f"- {source} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
