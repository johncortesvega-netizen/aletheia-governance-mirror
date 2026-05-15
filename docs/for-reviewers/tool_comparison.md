# ALETHEIA compared to other AI governance tools

ALETHEIA is a free, open-source governance mirror for human review. It does not explain model internals like SHAP or LIME, enforce compliance like enterprise governance platforms, or block runtime outputs like guardrails. Instead, it reflects governance-risk patterns in proposals, policies, scenarios, AI artifacts, public-data evidence views, and ALETHEIA receipts.

Its niche is not automated control. Its niche is structured reflection: capture risk, weak appeal paths, evidence gaps, consent pressure, service misalignment, authority overreach, and repair questions.

Use ALETHEIA beside other tools, not instead of them.

| Aspect | ALETHEIA v1.0 | XAI tools such as SHAP / LIME | Enterprise governance platforms | Runtime guardrails |
|---|---|---|---|---|
| Core purpose | Governance-risk reflection for human review | Explain model decision internals | Compliance workflows, risk management, and oversight | Real-time safety and output control |
| Method | Rule/heuristic signal maps and structured review outputs | Statistical feature attribution | Dashboards, scoring, policy workflows, monitoring | Programmable validators and runtime rules |
| Output style | Risk signals, evidence context, repair questions, and receipts | Visual explanations and attribution scores | Risk scores, compliance reports, audit artifacts | Blocked, rewritten, flagged, or validated outputs |
| Live model use | None; this is an intentional design boundary | Usually none | Often includes monitoring or integrations | Often used directly in AI applications |
| Best used for | Reviewing proposals, policies, scenarios, static AI artifacts, evidence views, and receipts | Debugging predictive model decisions | Organizational compliance and governance operations | Production safety for AI applications |
| Transparency | Very high: open-source, inspectable rules, reviewer docs, and local receipts | High for explanation methods, depending on implementation | Varies; many are proprietary | High in open-source versions |
| Philosophy | Mirror, not throne: signals for human judgment | Technical explanation | Governance management and compliance | Preventive control |
| Relationship | Complementary reflection layer | Complementary technical layer | Complementary enterprise layer | Complementary safety layer |

## Positioning summary

ALETHEIA is strongest when a reviewer wants a structured second opinion on governance language, institutional safeguards, AI artifacts, evidence gaps, and subtle power dynamics in text.

SHAP and LIME-style tools help explain why a predictive model made a specific decision. Enterprise governance platforms help organizations manage compliance, monitoring, and policy workflows at scale. Guardrails help prevent harmful or off-policy outputs in real time.

ALETHEIA does not compete with these tools. It complements them by adding a dedicated complementary governance-risk reflection layer focused on human review, local receipts, transparency, and repair-oriented thinking.

**In one sentence:** ALETHEIA is not the tool that explains the model, enforces compliance, or blocks the output; it is the mirror that helps humans inspect the governance risk around what is being proposed, written, claimed, or relied on.

## Boundary note

This comparison does not make ALETHEIA a certification system, compliance platform, model-explainability method, runtime guardrail, legal authority, official authority, or final decision-maker. It only clarifies where ALETHEIA sits beside other tools.
