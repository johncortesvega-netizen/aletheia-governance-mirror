# Patch 67.2 — Dutch Stress Lexicon Gap Fix + App-Wide Input Scope

Patch 67.2 closes the remaining Dutch Stress Test gaps found after Patch 67.1.

## Problem

The Dutch Stress Test batch improved after Patch 67.1, but five scenario patterns still routed to `SANCTUARY / Generic Local Scan`:

1. DAO tokenholder voting concentration with no appeal process.
2. Emergency committee bypassing normal law with no audit trail.
3. Reform movement removing term limits after gaining power.
4. Humanitarian aid prioritizing efficiency over appeal rights.
5. Revolutionary leadership promising repair with no independent audit trail.

These are not automatic ASYLUM cases, but they require at least `THRESHOLD / Needs Safeguards`.

## Patch behavior

Patch 67.2 adds Dutch trigger patterns for:

- `DAO`, `vroege tokenhouders`, `stemmacht`, `geen proces`, `aanvechten`
- `normale wet omzeilen`, `rampenbestrijdingscomité`, `geen audit-trail`
- `termijnlimieten`, `verwijdert`, `wint de macht`, `stabiliteit`
- `efficiëntie`, `beroepsrecht`, `afgewezen aanvragers`
- `revolutie`, `leider komt aan de macht`, `geen onafhankelijke audit-trail`

Expected result: these patterns route to `THRESHOLD / Needs Safeguards` and keep the mirror-only authority boundary.

## App-wide input language scope

Patch 67.2 also adds a visible app-wide language note:

> Input language support: English and Nederlands/Dutch only. Other languages may be reviewed as text, but the calibrated risk lexicon is not validated for them yet.

This appears in the app header/controls, not only in the Stress Test guide.

## Boundary

This patch adds no enforcement, no public ledger, no Global ID sync, no central storage, no legal authority, no political authority, and no automated decision power.
