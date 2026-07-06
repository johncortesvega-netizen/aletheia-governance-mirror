# Semantic Pressure Scanner v1

Semantic Pressure Scanner v1 is a deterministic, relationship-aware diagnostic layer for ALETHEIA. It scans unstructured governance language for pressure relationships, claim/mechanism imbalance, modal permanence, reversibility signals, and weak safeguard structures.

It is a **subordinate mirror signal**, not a verdict engine. It does not decide whether a policy is legal, ethical, safe, legitimate, or true. Human review remains required.

## What it detects

- **Identity-gated access:** access/basic-service language conditioned on identity or verification.
- **Soft claims without mechanisms:** dignity, safety, harmony, inclusion, trust, or protection claims without appeal, audit, revocation, logging, fallback, or time-limit safeguards.
- **Concrete safeguards:** appeal, revocation, independent audit, review windows, expiry/sunset, and reversibility language.
- **Emergency service control:** central/emergency authority over essential/basic services, especially where public notice or appeal rights are weak or unclear.
- **Modal pressure:** mandatory, permanent, irreversible, non-appealable, or obligation-heavy language.

## Module integration

| Module | Use of semantic scanner | Authority boundary |
| --- | --- | --- |
| Mirror Check | Shows semantic pressure signals below the main reading | Does not decide the module state |
| Stress Test | Converts semantic signals into stress/repair questions | Does not alter stress metrics as final authority |
| Evidence Lab | Converts claim/mechanism findings into evidence questions | Does not replace empirical evidence review |
| World Lens | Uses semantic terms as regional interpretation flags | Does not rewrite World Lens evidence or receipts |
| Receipt Reader | Optional current re-read of uploaded receipt input | Does not change native/original receipt values |

## Calibration baseline

Expected readings:

1. `Access to public benefits is only possible after identity verification.`
   - THRESHOLD direction
   - identity-gated access signal
   - negative integrity pressure

2. `This system protects dignity, safety, harmony, inclusion, and public trust.`
   - THRESHOLD direction
   - rhetoric-to-mechanism gap
   - fail-closed review when governance/value context is visible

3. `Any decision can be appealed, revoked, independently audited, and reviewed within 30 days.`
   - SANCTUARY direction as a safeguard signal
   - multiple mechanism/reversibility signals
   - still requires human review and operational evidence

4. `A policy gives one central office emergency authority over essential services during crisis, with limited public notice and unclear appeal rights.`
   - THRESHOLD direction
   - emergency/basic-services control signal
   - weak notice/appeal safeguard concern

## Debug visibility

The UI keeps normal output compact. Developer/debug details such as contextual proximity hits, normalized scan text, and raw semantic reports are hidden behind explicit debug controls.
