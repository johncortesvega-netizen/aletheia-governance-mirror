# ALETHEIA Empirical Study Methodology Draft

## Research question
Can a V-Axis-inspired governance-risk model, calibrated with public demographic, governance, democracy, and trust data, classify systemic stability and capture risk in a way that corresponds to observed governance outcomes?

## Model posture
ALETHEIA should be presented as a hypothesis-generating research model, not as proof of any doctrine and not as a real-world decision authority.

## Data sources
1. UN World Population Prospects: country-year population and 9k proportional seat allocation.
2. World Bank Worldwide Governance Indicators: institutional governance measures.
3. V-Dem: democracy, executive constraint, public accountability, civil liberties, and autocratization measures.
4. World Values Survey / regional barometers: social trust and institutional confidence.

## Unit of analysis
Country-year.

## Core formula family
The simplified V-Axis thesis is:

Intelligence + Power - Ego = Stability

The empirical layer operationalizes this as:

Predicted Stability = capacity + rule alignment + trust - capture - power concentration

## Initial variable mapping
- Technical complexity / institutional capacity: WGI Government Effectiveness and Political Stability.
- Centralization: inverse of V-Dem executive constraints, WGI Voice and Accountability, and democracy score.
- Anonymity / opacity: inverse of Voice and Accountability, Control of Corruption, and social trust.
- Regulation: WGI Rule of Law and Regulatory Quality.
- Transparency: WGI Voice and Accountability, Control of Corruption, and democracy score.
- Trust prior: WVS generalized trust.

## Validation
1. Correlation tests against external stability, rule-of-law, corruption, democracy, and trust indicators.
2. Group comparisons across Sanctuary, Threshold, and Asylum classes.
3. Out-of-sample tests where older years calibrate weights and later years test predictive value.

## Limitations
- Public datasets have missingness, measurement error, and cultural bias.
- WVS coverage is not annual and does not cover every country.
- Model weights are provisional until calibrated.
- The 9k allocation is representation logic; it is not yet a 9,000-person behavioral simulation.
