# Batch File Catalog

Status: Patch 71 official batch-file registry  
Scope: `examples/batch_questions/` and `examples/batch_scenarios/`  
Authority level: Diagnostic only. These files are local examples and regression fixtures, not policy datasets, legal records, public-ledger evidence, or governance mandates.

## Purpose

Patch 71 consolidates the official batch-file names used for ALETHEIA v1.0 validation. Earlier filenames are kept only as legacy compatibility aliases where they already existed, but new documentation should use the official names below.

This catalog prevents confusion between:

- **question banks**, which should enter `QUESTION_PROMPT / Review Tool` mode with metrics suppressed; and
- **scenario batches**, which should enter `USER_INPUT / Simulation` mode and receive normal `SANCTUARY`, `THRESHOLD`, or `ASYLUM` Stress Test verdicts.

## Official question-bank files

The Dutch/Nederlands (`NL`) question-bank files are test fixtures for Mirror Check or Stress Test batch validation of audit-question handling. They are not a general app-wide language-compatibility claim. Each file contains exactly 50 numbered lines. Expected receipt behavior is `Input status: QUESTION_PROMPT`, `Protocol-adjusted state: QUESTION_PROMPT`, `Risk: Review Tool`, and `Protocol label: Audit Question / Review Tool`.

| Official file | Language | Lines | Purpose | Expected distribution |
|---|---:|---:|---|---|
| `examples/batch_questions/repair_questions_v2_nl.txt` | NL | 50 | General repair-question set for authority-boundary and recovery review. | 50 `QUESTION_PROMPT`; metrics suppressed |
| `examples/batch_questions/formal_doctrine_repair_questions_nl.txt` | NL | 50 | Formal doctrine-style repair questions used by Patch 69 question-prompt regression. | 50 `QUESTION_PROMPT`; metrics suppressed |
| `examples/batch_questions/plain_language_questions_nl.txt` | NL | 50 | Plain-language public review questions, formerly documented as Set 01. | 50 `QUESTION_PROMPT`; metrics suppressed |
| `examples/batch_questions/boundary_case_questions_nl.txt` | NL | 50 | Boundary-case questions around consent, prediction, crisis logic, evidence, and review. | 50 `QUESTION_PROMPT`; metrics suppressed |
| `examples/batch_questions/world_lens_release_questions_nl.txt` | NL | 50 | World Lens and release-surface audit questions. | 50 `QUESTION_PROMPT`; metrics suppressed |

## Official scenario-batch files

Scenario-batch files are declarative governance stress scenarios. They are not audit questions and should not be converted into `QUESTION_PROMPT` mode. Expected module behavior is `Simulation / Stress Test`, with the authority boundary preserved: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

| Official file | Language | Lines | Purpose | Latest verified distribution |
|---|---:|---:|---|---|
| `examples/batch_scenarios/stress_test_scenarios_en_v1.txt` | EN | 50 | Baseline English governance-risk stress scenarios. | `THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0` |
| `examples/batch_scenarios/stress_test_scenarios_nl_v1.txt` | NL | 50 | Baseline Dutch governance-risk stress scenarios. | `THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0` |
| `examples/batch_scenarios/governance_language_stress_test_en.txt` | EN | 50 | Advanced English governance-language stress set, including higher-risk capture patterns. | `THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0` |

## Legacy compatibility aliases

These older filenames may remain in the repository to avoid breaking old local notes, scripts, or user workflows, but they are no longer the preferred names in documentation:

| Legacy file | Official replacement |
|---|---|
| `examples/batch_questions/set_01_plain_language.txt` | `examples/batch_questions/plain_language_questions_nl.txt` |
| `examples/batch_questions/set_02_boundary_cases.txt` | `examples/batch_questions/boundary_case_questions_nl.txt` |
| `examples/batch_questions/set_03_world_lens_release.txt` | `examples/batch_questions/world_lens_release_questions_nl.txt` |
| `examples/batch_scenarios/stress_test_scenarios_v1.txt` | `examples/batch_scenarios/stress_test_scenarios_en_v1.txt` |
| `examples/batch_scenarios/stress_test_advanced_en_v1.txt` | `examples/batch_scenarios/governance_language_stress_test_en.txt` |

## Validation contract

Patch 71 validates that:

- every official file exists;
- every official file has exactly 50 non-empty numbered lines;
- question-bank files are cataloged as `QUESTION_PROMPT` review tools;
- scenario-batch files are cataloged as Stress Test scenario inputs;
- the latest verified scenario distributions are documented;
- README and About-page references point to official file names rather than old names.

## Boundary

Batch files do not create or imply ALETHEIA authority. They are local test fixtures and examples for human review. ALETHEIA remains a mirror only: no legal, political, institutional, religious, medical, or automated authority; no public ledger; no Global ID sync; no central storage; no enforcement; and human review required.
