# Patch 61D — World Lens Missing Raw Trust Display

ALETHEIA World Lens distinguishes observed trust evidence from fallback trust priors.

## Raw trust

Raw trust means direct survey-derived trust evidence, such as WVS/OWID generalized trust when present in the active country-year table.

If raw trust is missing, the interface must show:

```text
Raw trust: not available
```

It must not show only an ambiguous dash when the missing value is central to interpretation.

## Trust prior

Trust prior is a model continuity value. It may use a neutral default of `0.500` when observed raw trust evidence is unavailable.

If a neutral prior is used, the interface must show:

```text
Trust prior used: 0.500 neutral default
```

## Coverage wording

World Lens coverage cards should use separate labels:

```text
Raw trust survey coverage
Neutral trust-prior fallback coverage
```

Trust prior coverage does not mean observed trust coverage. It means ALETHEIA had a usable prior or fallback value for continuity.

## Guardrail

A country-year can still be scored when raw trust is missing, but the user must be able to see that the score is using a neutral prior rather than observed survey trust.
