"""Human-auditable protocol baseline self-audit helpers for ALETHEIA.

Patch 101 adds a local hash comparison against a known baseline manifest. The
result is intentionally review support only: it can flag changed, missing, or
unknown files for human review, but it cannot approve a release, prove safety,
or make the repository tamper-proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PROTOCOL_BASELINE_AUDIT_VERSION = "protocol-baseline-human-audit-v0.1"
DEFAULT_MANIFEST_PATH = Path("data/protocol_baseline_manifest.json")

PROTOCOL_BASELINE_NOTICE = (
    "Protocol Baseline Self-Audit is a local hash comparison for human review. "
    "It is not a security guarantee, tamper-proof control, automated approval, "
    "certification, enforcement mechanism, or final truth claim."
)

HUMAN_REVIEW_REQUIRED_NOTE = (
    "Only humans can audit, interpret, approve, reject, or release changes. "
    "ALETHEIA may surface baseline differences, but it does not certify its own integrity."
)

IGNORED_UNKNOWN_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}
IGNORED_UNKNOWN_SUFFIXES = {".pyc", ".pyo", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico"}


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for a file without executing it."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_baseline_manifest(root: str | Path = ".", manifest_path: str | Path | None = None) -> dict[str, Any]:
    """Load the local protocol baseline manifest as review evidence."""
    root_path = Path(root)
    manifest = Path(manifest_path) if manifest_path is not None else DEFAULT_MANIFEST_PATH
    if not manifest.is_absolute():
        manifest = root_path / manifest
    return json.loads(manifest.read_text(encoding="utf-8"))


def _iter_reviewable_files(root: Path) -> list[str]:
    paths: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORED_UNKNOWN_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() in IGNORED_UNKNOWN_SUFFIXES:
            continue
        paths.append(rel.as_posix())
    return sorted(paths)


def audit_protocol_baseline(
    root: str | Path = ".",
    manifest_path: str | Path | None = None,
    *,
    include_unknown: bool = False,
) -> dict[str, Any]:
    """Compare watched protocol files against a baseline manifest.

    Statuses are deliberately human-review oriented:
    - MATCHES_BASELINE
    - MODIFIED_REQUIRES_HUMAN_REVIEW
    - MISSING_REQUIRES_HUMAN_REVIEW
    - UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW
    """
    root_path = Path(root).resolve()
    manifest = load_baseline_manifest(root_path, manifest_path)
    watched: dict[str, str] = dict(manifest.get("files", {}))

    rows: list[dict[str, Any]] = []
    status_counts = {
        "MATCHES_BASELINE": 0,
        "MODIFIED_REQUIRES_HUMAN_REVIEW": 0,
        "MISSING_REQUIRES_HUMAN_REVIEW": 0,
        "UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW": 0,
    }

    for rel_path, expected_hash in sorted(watched.items()):
        path = root_path / rel_path
        if not path.exists():
            status = "MISSING_REQUIRES_HUMAN_REVIEW"
            actual_hash = None
        else:
            actual_hash = sha256_file(path)
            status = "MATCHES_BASELINE" if actual_hash == expected_hash else "MODIFIED_REQUIRES_HUMAN_REVIEW"
        status_counts[status] += 1
        rows.append({
            "path": rel_path,
            "status": status,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "human_review_required": status != "MATCHES_BASELINE",
        })

    if include_unknown:
        for rel_path in _iter_reviewable_files(root_path):
            if rel_path in watched:
                continue
            status_counts["UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW"] += 1
            rows.append({
                "path": rel_path,
                "status": "UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW",
                "expected_sha256": None,
                "actual_sha256": sha256_file(root_path / rel_path),
                "human_review_required": True,
            })

    differences = [row for row in rows if row["status"] != "MATCHES_BASELINE"]
    return {
        "audit_mode": "Human-Auditable Protocol Baseline Self-Audit",
        "audit_version": PROTOCOL_BASELINE_AUDIT_VERSION,
        "baseline_id": manifest.get("baseline_id"),
        "manifest_version": manifest.get("manifest_version"),
        "notice": PROTOCOL_BASELINE_NOTICE,
        "human_review_required_note": HUMAN_REVIEW_REQUIRED_NOTE,
        "scope_note": manifest.get("scope_note"),
        "include_unknown": include_unknown,
        "watched_file_count": len(watched),
        "review_row_count": len(rows),
        "difference_count": len(differences),
        "status_counts": status_counts,
        "release_requires_human_review": True,
        "difference_requires_human_review": bool(differences),
        "rows": rows,
    }


def render_protocol_baseline_audit_text(report: dict[str, Any]) -> str:
    """Render a compact human-readable self-audit report."""
    lines = [
        "ALETHEIA PROTOCOL BASELINE SELF-AUDIT",
        f"Audit version: {report.get('audit_version')}",
        f"Baseline ID: {report.get('baseline_id')}",
        "",
        str(report.get("notice")),
        str(report.get("human_review_required_note")),
        "",
        f"Watched files: {report.get('watched_file_count')}",
        f"Differences requiring human review: {report.get('difference_count')}",
        "Status counts:",
    ]
    for status, count in (report.get("status_counts") or {}).items():
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Review rows:")
    for row in report.get("rows", []):
        marker = "REVIEW" if row.get("human_review_required") else "OK"
        lines.append(f"- [{marker}] {row.get('path')}: {row.get('status')}")
    return "\n".join(lines).strip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run ALETHEIA's human-auditable protocol baseline self-audit.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--manifest", default=None, help="Manifest path. Defaults to data/protocol_baseline_manifest.json.")
    parser.add_argument("--include-unknown", action="store_true", help="Also flag files not listed in the baseline manifest.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of text.")
    args = parser.parse_args(argv)

    report = audit_protocol_baseline(args.root, args.manifest, include_unknown=args.include_unknown)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_protocol_baseline_audit_text(report), end="")
    return 0 if report["difference_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
