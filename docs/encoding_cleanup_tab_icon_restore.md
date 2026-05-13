# Patch 127 — Encoding Cleanup and Tab Icon Restore

Patch 127 repairs visible text-encoding corruption introduced during the late structural-refactor review chain.

The patch restores the public tab icons and normal Unicode punctuation in the app surface and in extracted public documentation. Examples include restored tab labels such as `🪞 Mirror Check`, `🚀 Stress Test`, `🤖 AI Integrity Mirror`, `📊 Evidence Lab`, `🌐 World Lens`, `📜 Protocol Guide`, and `ℹ️ Why ALETHEIA`.

## Scope

This is a public UI text cleanup only. It fixes mojibake such as broken emoji bytes, broken dashes, broken bullets, and related punctuation where it appeared in the app shell/public page surface.

## Boundary preserved

Patch 127 does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, upload handling, download handling, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, analytics, storage, identity sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
