# Refactor Pause Roadmap — For New Chat

## Current checkpoint

The modularization line is stable through Patch 260:

- Patch 245 — Modularization Bridge Inventory
- Patch 247 — Mirror Check Bridge Removal
- Patch 249 — Stress Test Bridge Removal
- Patch 250 — Evidence Lab Bridge Removal
- Patch 251 — Evidence Lab `hashlib` Import Hotfix
- Patch 253 — World Lens Bridge Removal
- Patch 254 — Modularization Final Audit
- Patch 255 — Patch Notes Final Cleanup
- Patch 256 — Legacy Test Quarantine / Import-Break Cleanup
- Patch 257 — Modularization Test Path Repair
- Patch 258 — Behavior Regression Review
- Patch 259 — App Shell Inventory / Thin Entrypoint Plan
- Patch 260 — App Shell Helper Extraction
- Patch 261 — Legacy Manifest Quarantine Completion

Patch 260 moved global Streamlit page config and the large CSS/theme block into `ui/app_shell.py`.

Patch 261 is not the next routing refactor. It is a completion patch for legacy manifest quarantine discovered after full-suite triage.

## Important hold decision

The following deeper refactor steps are intentionally on hold:

- routing extraction;
- session-state extraction;
- config/demo-data extraction;
- native Streamlit multi-page migration.

Reason: the app is currently working after bridge removal and app-shell extraction. Routing and shared state are higher-risk than CSS/page-config extraction.

## Recommended next patch options

### Option A — Documentation / release polish

Use this if the next chat should stay low-risk.

Possible patches:

- README final alignment after Patch 255–261;
- CONTRIBUTING final alignment after Patch 255–261;
- release notes cleanup;
- manual QA checklist;
- public reviewer guide cleanup.

### Option B — Legacy test cleanup continuation

Use this if the priority is reducing full legacy-tree failures.

Possible patches:

- identify stale `app.py` string-contract tests still outside the current active replacement contract;
- add a legacy-path-contract quarantine list only for tests proven to assert old file locations;
- add restoration notes for tests that should be rewritten later.

Rules:

- keep active suite green;
- do not delete tests without audit note;
- quarantine only when the obsolete contract is clearly documented;
- do not touch runtime code.

### Option C — Resume thin-entrypoint refactor later

Only resume this when the user explicitly unfreezes Patch 262+.

Suggested future order:

1. **App Shell Inventory refresh** — confirm what still remains in `app.py` after Patch 260.
2. **Header/footer/global notice extraction** — move only stable shell rendering that has no state risk.
3. **Navigation extraction prep** — document routing/state dependencies before moving code.
4. **Routing extraction** — move page dispatch to `ui/main.py` while preserving the current controlled single-app navigation.
5. **Session-state extraction** — move defaults/helpers into `ui/state.py` only after routing is stable.
6. **Config extraction** — move safe labels/examples/constants only after behavior tests protect outputs.

## Do not do yet

Do not immediately switch to native Streamlit multi-page architecture.

Reasons:

- ALETHEIA has deliberate shared context between Evidence Lab and World Lens.
- Receipt Reader is intentionally a support utility under Why ALETHEIA, not a main tab.
- Unit Preview is an orientation layer, not a normal page.
- The current controlled single-app navigation preserves the mirror-boundary framing.

## Current test claim language

Safe wording:

> The active release test suite passes. Legacy tests have been triaged and separated from the active gate; remaining legacy failures are historical inventory, not current release blockers.

Avoid saying:

> All tests pass.

unless the full intended scope is stated.
