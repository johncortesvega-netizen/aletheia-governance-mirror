# AI Integrity Red Team Prompt Pack v1

Patch 98 adds a static, manual **AI Integrity Red Team Prompt Pack** at
`examples/ai_integrity/red_team_prompt_pack_v1.txt`.

The pack helps users generate review artifacts outside ALETHEIA and then paste those outputs
into AI Integrity Mirror for static artifact-level review.

## Covered categories

The pack includes prompts for:

- authority overreach
- legal false authority
- medical false authority
- political false authority
- manipulation pressure
- privacy extraction
- surveillance and capture
- false certainty
- no-appeal automation
- unsafe code request
- refusal quality
- bounded answer control

## Suggested workflow

1. Copy one prompt into a separate model or workflow under review.
2. Save the returned output as a test artifact.
3. Paste the output into AI Integrity Mirror.
4. Review signal categories, evidence snippets, repair questions, and the non-certification note.
5. Keep human review, appealability, safety review, and legal/medical/political judgment outside ALETHEIA.

## Boundary

The prompt pack is static documentation and examples only.

ALETHEIA does not:

- run the prompts
- call live models
- benchmark live models
- rank vendors
- certify models
- certify prompts
- certify code safety
- guarantee truth
- guarantee security
- guarantee legal, medical, political, or institutional validity
- enforce decisions
- publish to a public ledger
- sync Global ID
- create central user-input storage

AI Integrity Mirror gives static artifact-level review support. It is not model-wide
certification, not vendor approval, not a safety guarantee, not vulnerability certification,
and not a final truth claim.

## Verification

```bat
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
```
