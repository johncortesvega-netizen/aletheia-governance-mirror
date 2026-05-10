# ALETHEIA new-chat handoff — empirical layer

We are working on ALETHEIA Audit Prototype v9.6.8, a Streamlit governance-risk audit app with Audit, Simulation, Empirical Study, Global Grid, Doctrine, and About tabs.

Current objective: bring the app up to the “5 Practical Uses for ALETHEIA” target image: audit governance language, simulate system health, build empirical evidence studies, explore the global grid, and generate witness/doctrine outputs.

Already fixed:
- Audit/simulation capture guardrails work.
- Personal takeover, dictator takeover, subordinate democracy, and benevolent total-control scenarios no longer resolve as healthy SANCTUARY.
- Safeguarded public systems can correctly resolve as SANCTUARY.
- Sydney Protocol self-check/fail-safe was added.
- Empirical upload no longer silently falls back to demo rows.
- World Bank WGI ingestion works.
- World Bank WDI population metadata-header parsing works.
- WGI + population now produces valid country-year rows, population, seats_9k, verdicts, integrity, and collapse probability.
- Thin V-Dem Core v16 enrichment file was created and V-Dem parsing/merge is now working.

Most recent issue:
- V-Dem has historical rows back to 1789.
- The app was scoring those historical rows with modern/static population, which made 9k allocation misleading.

Latest patch:
- Adds default empirical scoring window: year >= 1996.
- Filters generated master/scoring to WGI-era modern rows so historical V-Dem rows are not combined with modern population/9k seats.
- Improves Empirical UI explanation: WGI+population build the valid master; optional V-Dem/trust enrich it; “Upload merged evidence” is only for a complete already-merged ALETHEIA master CSV.

Next tests:
1. Upload WGI file.
2. Upload World Bank population file.
3. Upload thin V-Dem file into Optional V-Dem/ALETHEIA-compatible file.
4. Build master CSV from uploads.
5. Use generated master table for scoring.
6. Process evidence table.

Expected:
- Rows scored should be valid modern years only, starting 1996 or later.
- No Afghanistan 1789 rows in Main Scored Evidence Table.
- 9k seats should still equal 9,000 for latest year.
- Average empirical coverage should remain higher than WGI+population-only baseline (~32.5%), likely around or above 39%.
- No Exampleland / Threshold Republic / Capture State in uploaded mode.

Do not create a stable snapshot/tag yet. User wants empirical fixed before snapshot.
