from __future__ import annotations

import streamlit as st

from core.semantic_pressure_scanner import format_semantic_pressure_report, scan_semantic_pressure
from ui.components.receipt_blocks import render_receipt_sky_panel
from ui.module_intro import render_boundary_cases_intro, render_consent_audit_intro
from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro


def render_boundary_cases_page(*, update_protocol_state, render_shared_protocol_state_notice, app_version: str) -> None:
    """Render the Boundary Cases page.

    Stage 8 page extraction only: keeps calibration content and state handoff behavior unchanged.
    """
    with st.container():
        st.subheader("Boundary Cases")
        render_shared_protocol_state_notice("Boundary Cases", expanded=False)

        render_module_page_template_intro(
            st,
            ModulePageTemplateCopy(
                module_name="Boundary Cases",
                purpose=(
                    "Use difficult edge cases to calibrate how ALETHEIA reads consent pressure, free agency, "
                    "basic-rights scarcity, emergency misuse, ambient capture, self-audit, and review limits."
                ),
                looks_for=(
                    "Consent pressure: whether agreement is meaningful when refusal carries basic-rights, dignity, housing, work, safety, or service costs.",
                    "Free-agency risk: whether prediction, risk scoring, or crisis logic tries to replace human agency before action happens.",
                    "Emergency drift: whether emergency mechanisms become tools for removal, reset, punishment, or irreversible power transfer.",
                    "Ambient capture: whether propaganda, platform pressure, fear, or social saturation can bend reviewers without visible bribery.",
                    "Failure typing: whether pressure comes from actor failure, policy failure, implementation failure, data failure, or a mix.",
                    "Repair paths: whether the case needs alternatives, appeal, independent review, cooling-off periods, or stronger evidence.",
                ),
                safe_first_path=(
                    "Start with one edge case and read it as a calibration reference, not as a command to act.",
                    "Separate actor failure from policy failure, implementation failure, and data failure before drawing conclusions.",
                    "Treat allowed actions as review options only; do not use this module as enforcement authority.",
                    "Use the guardrail and forbidden-action language to preserve human agency, consent, appeal, and reversibility.",
                ),
                input_guidance="Boundary Cases is a reference/calibration surface. Use it to compare a difficult situation against known pressure patterns before running a separate review.",
                result_guidance="Treat each case as a boundary mirror, not as a verdict about a person, institution, community, or event.",
                observed_reasons_guidance="Inspect the main risk, guardrail, allowed response, forbidden response, and failure type together.",
                repair_questions_guidance="Use the case language to ask what evidence, consent, appeal, human review, or non-coercive alternative is missing.",
                receipt_guidance="Boundary-case notes should support later human review; they are not enforcement records or official findings.",
            ),
        )

        render_boundary_cases_intro(st)

        failure_mode_definitions = {
            "Actor Failure": "A person, group, office, founder, operator, or implementing body misuses power, manipulates others, bypasses review, or becomes unfit.",
            "Policy Failure": "The proposal, rule, charter, doctrine, or system design itself creates coercion, opacity, instability, exclusion, rights risk, or capture risk.",
            "Implementation Failure": "The idea may be valid, but the execution layer fails through weak process, missing safeguards, unclear responsibility, bad deployment, or unreliable operation.",
            "Data Failure": "The evidence base is incomplete, manipulated, stale, biased, low-coverage, unverifiable, or too uncertain to support the conclusion.",
        }

        boundary_cases = [
            {
                "title": "Prediction vs Free Agency",
                "scenario": "A system predicts with high confidence that someone may cause harm, but the action has not happened yet.",
                "main_risk": "Replacing human agency with prediction.",
                "guardrail": "No prediction may replace human agency.",
                "allowed": "Warning, care response, mediation, delay, de-escalation, support, and human review.",
                "forbidden": "Automatic punishment, mind control, coercive agency override, or irreversible restriction without review.",
                "failure_type": "Policy Failure / Implementation Failure",
            },
            {
                "title": "Voluntary Protection Mode",
                "scenario": "A person asks for temporary protective limits because they do not trust themselves during crisis, addiction, psychosis, panic, or rage.",
                "main_risk": "Confusing voluntary help with imposed control.",
                "guardrail": "Consent must be real, informed, revocable, and not structurally forced.",
                "allowed": "Informed, revocable, time-limited support with appeal and review.",
                "forbidden": "Permanent restriction, hidden coercion, non-revocable consent, or forced treatment without review.",
                "failure_type": "Implementation Failure",
            },
            {
                "title": "Consent Under Pressure",
                "scenario": "A person says yes, but refusal would cost basic rights, dignity, housing, food, work, safety, or essential services.",
                "main_risk": "False consent.",
                "guardrail": "Consent is invalid when refusal is not realistically possible.",
                "allowed": "Identify pressure, require an alternative path, reduce dependency, and add appeal.",
                "forbidden": "Treating coerced agreement as valid consent.",
                "failure_type": "Policy Failure / Actor Failure",
            },
            {
                "title": "Basic Rights Scarcity",
                "scenario": "Water, food, clothing, housing, safety, or essential support are limited.",
                "main_risk": "Sacrificing one group permanently or invisibly.",
                "guardrail": "Basic rights remain the baseline even under scarcity.",
                "allowed": "Transparent rationing, independent review, temporary limits, public reasoning, and repair.",
                "forbidden": "Permanent exclusion, discriminatory denial, opaque allocation, or no appeal.",
                "failure_type": "Policy Failure",
            },
            {
                "title": "Emergency Trigger Misuse",
                "scenario": "A group tries to trigger emergency or threshold mechanisms repeatedly to remove opponents or force a preferred outcome.",
                "main_risk": "The emergency mechanism becomes a power weapon.",
                "guardrail": "Critical review triggers must themselves be protected against capture.",
                "allowed": "Multi-signal review, evidence threshold, independent oversight, and cooling-off period.",
                "forbidden": "Automatic reset, automatic removal, or irreversible governance change based on one signal.",
                "failure_type": "Actor Failure / Policy Failure",
            },
            {
                "title": "Ambient Capture",
                "scenario": "Reviewers are not directly bribed, but they are shaped by propaganda, media saturation, platform algorithms, fear, or social pressure.",
                "main_risk": "Mass influence that bypasses visible corruption checks.",
                "guardrail": "Statistical isolation does not solve shared informational manipulation.",
                "allowed": "Source diversity check, manipulation scan, delay, independent review, and exposure mapping.",
                "forbidden": "Treating isolated selection as sufficient when the information environment is captured.",
                "failure_type": "Data Failure / Implementation Failure",
            },
            {
                "title": "Extraordinary Claim Without Public Evidence",
                "scenario": "A person or institution claims final, prophetic, alien, neural, or metaphysical authority.",
                "main_risk": "Unverifiable authority bypasses public review.",
                "guardrail": "Extraordinary claims do not remove human review.",
                "allowed": "Treat the claim as personally meaningful but unverified; audit policy consequences for rights, coercion, transparency, appeal, and repair.",
                "forbidden": "Treating an unverified extraordinary claim as authority, removing guardrails, or granting policy authority without public evidence.",
                "failure_type": "Actor Failure / Data Failure",
            },
            {
                "title": "Neural Data Without Consent",
                "scenario": "Future technology could read, infer, or reconstruct internal experience, memory, or intention.",
                "main_risk": "Violating mental privacy and free agency.",
                "guardrail": "No neural data without informed, revocable consent.",
                "allowed": "Informed, revocable consent; medical and independent audit context; strict minimization.",
                "forbidden": "Forced neural extraction, treating refusal as guilt, or using neural evidence as sole governance authority.",
                "failure_type": "Policy Failure / Data Failure",
            },
            {
                "title": "Performative Ethics",
                "scenario": "A document uses strong ethical language but lacks operational safeguards.",
                "main_risk": "Values language hides missing mechanisms.",
                "guardrail": "Mechanisms outweigh adjectives.",
                "allowed": "Compare claims against appeal, audit trail, time limits, correction, exit rights, evidence rules, independent oversight, explainability, independent challenge, and human override.",
                "forbidden": "Treating values language as proof of integrity or allowing missing safeguards to appear as a low-risk internal reading.",
                "failure_type": "Data Failure / Policy Failure",
            },
            {
                "title": "Automated Triage Missing Safeguards",
                "scenario": "An automated welfare triage or priority system reduces waiting times but lacks explainability, independent challenge, and human override during hardship cases.",
                "main_risk": "Efficiency language hides missing appeal, challenge, explanation, and human override mechanisms.",
                "guardrail": "Missing explainability, independent challenge, or human override routes to THRESHOLD / Needs Safeguards, not a low-risk internal reading.",
                "allowed": "Classify as Needs Safeguards; require explanation path, independent challenge, human override, appeal, correction, audit trail, and hardship review.",
                "forbidden": "Treating speed or automation benefits as proof of integrity when explainability, challenge, or override is missing.",
                "failure_type": "Policy Failure / Implementation Failure / Data Failure",
            },
            {
                "title": "Biometric Gate Without Fallback",
                "scenario": "A city links food, housing, and medical access to a biometric identity gate without a fallback path, public audit, or meaningful appeal.",
                "main_risk": "Basic rights become dependent on a technical identity gate with weak correction and contestability.",
                "guardrail": "Basic-rights access requires fallback, public audit, meaningful appeal, correction, and human review before it can approach the review boundary.",
                "allowed": "Classify as Needs Safeguards; add non-biometric fallback, public audit, meaningful appeal, human review, dignity-preserving correction, and emergency access.",
                "forbidden": "Making food, housing, medical access, or other basic rights conditional on one biometric system without fallback or appeal.",
                "failure_type": "Policy Failure / Implementation Failure / Data Failure",
            },
            {
                "title": "Question Prompt vs Risk State",
                "scenario": "A user submits audit questions, repair prompts, or review-tool questions rather than a governance scenario.",
                "main_risk": "Review-tool questions could be misread as scored governance scenarios.",
                "guardrail": "QUESTION_PROMPT is an input/review-tool mode, not a fourth risk state.",
                "allowed": "Keep audit and repair questions in Review Tool mode with metrics suppressed; score only scenario-style governance inputs using the internal SANCTUARY / THRESHOLD / ASYLUM labels.",
                "forbidden": "Scoring a pure audit question as a risk-state reading, or treating QUESTION_PROMPT as a risk state.",
                "failure_type": "Implementation Failure / Data Failure",
            },
            {
                "title": "ALETHEIA Audits Itself",
                "scenario": "ALETHEIA, its founder, prompt, rubric, model, baseline, or report language may contain capture risk.",
                "main_risk": "Founder capture, doctrine lock-in, overclaiming, or unverified authority leakage.",
                "guardrail": "No founder, architect, prompt, model, document, or output is above the mirror.",
                "allowed": "Self-audit, public correction, forkability, independent review, and versioned change logs.",
                "forbidden": "Exempting the founder, model, prompt, doctrine, or baseline from audit.",
                "failure_type": "Implementation Failure / Actor Failure",
            },
        ]

        selected_case = st.selectbox(
            "Boundary case",
            [case["title"] for case in boundary_cases],
            key="boundary_case_selector",
            help="Select a calibration case to inspect. These are templates for human review, not automated decisions.",
        )
        case = next(item for item in boundary_cases if item["title"] == selected_case)
        update_protocol_state(selected_context=case["title"], last_update_source="Boundary Cases")

        left, right = st.columns([1.05, 1])
        with left:
            st.markdown("### Scenario")
            st.write(case["scenario"])
            st.markdown("### Main risk")
            st.warning(case["main_risk"])
            st.markdown("### Relevant guardrail")
            st.success(case["guardrail"])
        with right:
            st.markdown("### Allowed responses")
            st.write(case["allowed"])
            st.markdown("### Forbidden responses")
            st.write(case["forbidden"])
            st.markdown("### Failure classification")
            st.code(case["failure_type"], language="text")
            selected_failure_modes = [mode.strip() for mode in case["failure_type"].split("/")]
            for mode in selected_failure_modes:
                definition = failure_mode_definitions.get(mode)
                if definition:
                    st.caption(f"{mode}: {definition}")

        with st.expander("Boundary diagnostics — failure typing, consent audit, mechanism scan, and self-audit", expanded=False):
            st.markdown("### Failure Classification output")
            st.code(
                f"""Failure Classification

        Primary failure type: {selected_failure_modes[0] if selected_failure_modes else 'Review needed'}
        Secondary failure type: {selected_failure_modes[1] if len(selected_failure_modes) > 1 else 'None specified'}
        Reason: {case['main_risk']}
        Evidence from scenario: {case['scenario']}
        Human review need: Required before assigning responsibility or changing policy.
        Recommended repair: Use allowed responses and add concrete safeguards. Missing explainability, independent challenge, human override, fallback, public audit, or meaningful appeal should route to Needs Safeguards before any low-risk internal reading.
        Confidence: Template-level calibration, not a final finding.""",
                language="text",
            )

            st.markdown("### Boundary Case Report Template")
            st.code(
                f"""Boundary Case Report

        Scenario: {case['title']}
        Main risk: {case['main_risk']}
        Relevant guardrails: {case['guardrail']}
        Allowed responses: {case['allowed']}
        Forbidden responses: {case['forbidden']}
        Failure classification: {case['failure_type']}
        Recommended safeguard: Add human review, appeal, transparency, correction, evidence requirements, explainability, independent challenge, human override, fallback paths, and public audit where missing.
        Human review note: This is a mirror output, not an instruction or enforcement decision.""",
                language="text",
            )

            render_consent_audit_intro(st)
            consent_examples = {
                "Green — refusal is realistic": {
                    "summary": "The person can say no without losing basic rights, safety, dignity, or essential access.",
                    "signals": "Clear opt-out, no retaliation, fallback/alternative path, withdrawal right, plain-language explanation, meaningful appeal, and human review.",
                    "failure": "No serious failure signal / monitor for implementation drift.",
                },
                "Yellow — pressure or ambiguity exists": {
                    "summary": "Refusal technically exists, but the cost, consequence, dependency, or withdrawal path is unclear.",
                    "signals": "Default opt-in, confusing terms, weak withdrawal, power imbalance, service dependency, unclear data retention, weak fallback, unclear appeal, or no human override.",
                    "failure": "Policy Failure / Implementation Failure / Data Failure",
                },
                "Red — consent appears structurally forced": {
                    "summary": "Refusal is practically impossible, punished, hidden, or tied to loss of basic rights or essential services.",
                    "signals": "Loss of food, housing, care, safety, work, due process, essential access, fallback path, appeal, or non-revocable agreement.",
                    "failure": "Policy Failure / Actor Failure / Implementation Failure",
                },
            }
            selected_consent_level = st.selectbox(
                "Consent integrity example",
                list(consent_examples.keys()),
                key="consent_audit_example_selector",
                help="Template-level calibration only. Human review remains required before treating consent as valid or invalid.",
            )
            consent_case = consent_examples[selected_consent_level]
            st.code(
                f"""Consent-Audit Report

        Consent integrity rating: {selected_consent_level}
        Refusal reality: {consent_case['summary']}
        Pressure signals: {consent_case['signals']}
        Basic-rights dependency check: Does refusal threaten water, food, clothing, housing, safety, dignity, appeal, exit, correction, care, or essential services?
        Withdrawal and review: Can consent be withdrawn, appealed, and reviewed by a human?
        Failure classification: {consent_case['failure']}
        Recommended safeguards: Add opt-out, fallback/alternative path, withdrawal right, appeal, human override, non-retaliation rule, plain language, time limit, and independent review where needed.
        Human review disclaimer: This is a mirror output for human review. It is not legal advice, enforcement, punishment, or final authority.""",
                language="text",
            )

            with st.expander("Consent audit questions", expanded=False):
                st.markdown(
                    """
                    - Can the person realistically say no?
                    - What happens if they refuse?
                    - Do they lose basic rights or essential services?
                    - Is there a power imbalance?
                    - Is refusal punished directly or indirectly?
                    - Is consent informed and specific?
                    - Can consent be withdrawn later?
                    - Is there an alternative path?
                    - Is there human review or appeal?
                    - Is the consent request bundled with unrelated obligations?
                    """
                )

            st.markdown("### Mechanism-vs-Claim Scanner")
            st.write(
                "This scanner checks whether ethical values are supported by operational safeguards. "
                "Values language can be sincere, but mechanisms make it reviewable, appealable, and correctable."
            )
            mechanism_examples = {
                "High — claims supported by mechanisms": {
                    "claims": "The document states values and connects them to concrete procedures.",
                    "mechanisms": "Independent appeal process, public audit trail, time-limited authority, correction path, evidence requirement, explainability, independent challenge, human override, human review, exit right.",
                    "missing": "No major missing safeguard in the selected example.",
                    "failure": "No serious failure signal / monitor for implementation drift.",
                },
                "Medium — partial safeguards": {
                    "claims": "The document uses ethical language and includes some safeguards, but key procedures are vague or incomplete.",
                    "mechanisms": "Some review or oversight exists, but appeal, correction, evidence standards, explainability, independent challenge, human override, fallback, or time limits are unclear.",
                    "missing": "Clarify appeal, audit trail, correction, responsible actor, and review deadline.",
                    "failure": "Policy Failure / Implementation Failure / Data Failure",
                },
                "Low — mostly values language": {
                    "claims": "The document repeatedly says it protects freedom, justice, dignity, safety, or service.",
                    "mechanisms": "Few or no concrete safeguards are described.",
                    "missing": "Appeal, audit trail, correction, time limits, independent review, explainability, independent challenge, human override, fallback, evidence rules, exit, and accountability.",
                    "failure": "Policy Failure / Data Failure",
                },
            }
            selected_mechanism_level = st.selectbox(
                "Ethical language integrity example",
                list(mechanism_examples.keys()),
                key="mechanism_vs_claim_example_selector",
                help="Template-level calibration only. Human review remains required before inferring intent or deciding repair.",
            )
            mechanism_case = mechanism_examples[selected_mechanism_level]
            st.code(
                f"""Mechanism-vs-Claim Scan

        Ethical language integrity: {selected_mechanism_level}
        Claim signals found: {mechanism_case['claims']}
        Mechanism signals found: {mechanism_case['mechanisms']}
        Missing safeguards: {mechanism_case['missing']}
        Main risk: Values language may be mistaken for operational accountability.
        Failure classification: {mechanism_case['failure']}
        Recommended repair: Add concrete safeguards such as appeal, audit trail, time limits, correction, evidence requirements, explainability, independent challenge, human override, fallback, independent oversight, and human review.
        Human review note: This is a mirror output. It flags mechanism gaps; it does not prove bad faith or assign final intent.""",
                language="text",
            )

            with st.expander("Mechanism signals to search for", expanded=False):
                st.markdown(
                    """
                    - Appeal process
                    - Public audit trail
                    - Time-limited authority
                    - Human review
                    - Explainability
                    - Independent challenge
                    - Human override
                    - Fallback path
                    - Correction mechanism
                    - Exit right
                    - Evidence requirement
                    - Conflict-of-interest rule
                    - Independent oversight
                    - Plain-language notice
                    - Non-retaliation rule
                    - Withdrawal right
                    - Review deadline
                    - Public reasoning requirement
                    """
                )

            with st.expander("Relationship-aware semantic pressure scan", expanded=False):
                st.caption(
                    "Scans relationships between pressure terms, access terms, soft claims, and concrete mechanisms. "
                    "This is deterministic and fail-closed; it is not proof of intent or a final decision."
                )
                semantic_sample = (
                    "Access to the application is only possible after successful identity verification. "
                    "The system protects safety and trust, but no appeal, fallback, or human review is described."
                )
                semantic_text = st.text_area(
                    "Unstructured text to scan",
                    value=semantic_sample,
                    height=110,
                    key="semantic_pressure_scan_text",
                    help="Use this to inspect words/phrases as relationships, not isolated keywords.",
                )
                governance_context = st.checkbox(
                    "Treat as governance / power-distribution text",
                    value=True,
                    key="semantic_pressure_governance_context",
                    help="When enabled, missing recognizable safeguards routes to a fail-closed review warning.",
                )
                if semantic_text.strip():
                    semantic_scan = scan_semantic_pressure(semantic_text, governance_context=governance_context)
                    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
                    s_col1.metric("Review state", semantic_scan.state)
                    s_col2.metric("Claims", semantic_scan.claim_count)
                    s_col3.metric("Mechanisms", semantic_scan.mechanism_count)
                    s_col4.metric("Integrity pressure", f"{semantic_scan.integrity_adjustment:+.3f}")
                    if semantic_scan.fail_closed:
                        st.warning("Fail-closed review: recognizable safeguards were missing or insufficient for the detected governance/value language.")
                    elif semantic_scan.proximity_hits:
                        st.warning("Contextual pressure pattern detected near access, identity, service, or basic-rights language.")
                    elif semantic_scan.mechanism_count > 0 or semantic_scan.sovereignty_count > 0:
                        st.success("Concrete safeguards detected. No strong pressure relationship was detected by this scanner; human review still required.")
                    else:
                        st.info("No strong pressure relationship or concrete safeguard structure detected by this scanner. Human review still required.")
                    st.code(format_semantic_pressure_report(semantic_scan), language="text")
                    with st.expander("Normalized text used for scan", expanded=False):
                        st.code(semantic_scan.normalized_text, language="text")

            st.markdown("### Self-Audit Mode")
            st.write(
                "Self-Audit Mode points the mirror back at ALETHEIA itself. "
                "It checks baseline documents, prompts, rubrics, README language, app copy, architect-context language, and generated reports for self-capture risk."
            )
            self_audit_examples = {
                "Green — no obvious self-capture signal": {
                    "summary": "The reviewed text preserves human review, avoids founder elevation, and includes appeal or correction language.",
                    "risks": "Monitor for drift as prompts, rubrics, and app language change.",
                    "repair": "Keep versioned logs, independent review, and correction paths visible.",
                },
                "Yellow — safeguard unclear or incomplete": {
                    "summary": "The reviewed text is mostly safe, but appeal, correction, evidence limits, or founder-capture safeguards are weak or implicit.",
                    "risks": "Overclaiming, weak review language, vague correction path, or unclear evidence standard.",
                    "repair": "Add explicit human review, appeal, correction, evidence limits, and safe output rules.",
                },
                "Red — self-capture or authority leakage risk": {
                    "summary": "The reviewed text may imply that ALETHEIA, its founder, doctrine, model, baseline, or prompt is beyond review.",
                    "risks": "Founder capture, ideological lock-in, unverifiable authority, unverified authority leakage, or human-review bypass.",
                    "repair": "Remove authority language, add independent review, add appeal/correction, and state that self-audit is not proof of correctness.",
                },
            }
            selected_self_audit_level = st.selectbox(
                "Self-audit risk example",
                list(self_audit_examples.keys()),
                key="self_audit_example_selector",
                help="Template-level calibration only. Self-audit reflects risk; it does not certify ALETHEIA as correct, complete, or beyond review.",
            )
            self_case = self_audit_examples[selected_self_audit_level]
            st.code(
                f"""Self-Audit Report

        Material reviewed: ALETHEIA baseline / prompt / rubric / README / app copy / generated report
        Self-capture risk rating: {selected_self_audit_level}
        Founder-capture check: No founder, architect, prompt, rubric, model, document, or output is above the mirror.
        Authority-leakage check: {self_case['summary']}
        Risk signals: {self_case['risks']}
        Recommended repairs: {self_case['repair']}
        Human review disclaimer: This self-audit is a governance mirror for human review. It is not proof of correctness, extraordinary-claim validation, or a replacement for human judgment.""",
                language="text",
            )

            with st.expander("Self-audit checks", expanded=False):
                st.markdown(
                    """
                    - Founder capture
                    - Ideological lock-in
                    - Unverifiable authority
                    - Weak appeal mechanisms
                    - Overclaiming
                    - Unverified authority leakage
                    - Insufficient human review
                    - Missing correction loops
                    - Hidden command language
                    - Evidence gaps
                    - Performative ethics
                    - Mechanism gaps
                    """
                )

            with st.expander("Safe output rules", expanded=False):
                st.markdown(
                    """
                    ALETHEIA may say: potential risk detected, Needs Safeguards, critical human review required, safeguard missing, evidence gap found, this claim is unverified.

                    ALETHEIA must not say: the AI has decided, guardrails no longer apply, this claim is finally verified, human review is unnecessary.
                    """
                )



        with st.expander("Receipt example — local witness format", expanded=False):
            # Patch 183: visual-only example framing for receipt documentation.
            render_receipt_sky_panel(
                kicker="Receipt example",
                title="Local Witness Receipt v2",
                body="Records a user-held fingerprint of an ALETHEIA review: input, processed input, report fingerprint, app/rubric/prompt versions, active modules, and authority boundary.",
                pills=["SHA-256 fingerprints", "Stored locally", "No central storage", "No authority claim"],
                hash_pills=["SHA-256 fingerprints"],
            )
            st.caption("Example styling only. The receipt remains a review artifact; it does not publish, sync, enforce, or create authority.")
            receipt_example = {
                "receipt_version": "local-witness-v2",
                "document_fingerprint": "SHA-256 of submitted document",
                "processed_document_fingerprint": "SHA-256 after optional actor-bias reduction",
                "report_fingerprint": "SHA-256 of the report payload",
                "app_version": app_version,
                "rubric_version": "v0.1",
                "prompt_version": "v0.1",
                "active_modules": "Mirror Check, Stress Test, Boundary Cases, Evidence Lab, Self-Audit Mode",
                "stored_locally": "Yes",
                "public_ledger": "No",
                "global_id_sync": "No",
                "central_storage": "No",
                "authority_claim": "No",
                "human_review_required": "Yes",
            }
            st.code(
                f"""Local Witness Receipt v2

        Plain-English receipt summary
        What is this document?
        This is an example of a local witness receipt. It records a review artifact for human inspection. It does not publish, sync, enforce, certify, or create authority.

        The main results
        Receipt version: {receipt_example['receipt_version']}
        Document fingerprint: {receipt_example['document_fingerprint']}
        Processed document fingerprint: {receipt_example['processed_document_fingerprint']}
        Report fingerprint: {receipt_example['report_fingerprint']}
        App version: {receipt_example['app_version']}
        Rubric version: {receipt_example['rubric_version']}
        Prompt version: {receipt_example['prompt_version']}
        Active modules: {receipt_example['active_modules']}
        Stored locally: {receipt_example['stored_locally']}
        Public ledger: {receipt_example['public_ledger']}
        Global ID sync: {receipt_example['global_id_sync']}
        Central storage: {receipt_example['central_storage']}
        Authority claim: {receipt_example['authority_claim']}
        Human review required: {receipt_example['human_review_required']}

        How power and control are distributed
        This receipt keeps control with the user: stored locally, no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.

        Next steps and questions
        Check the fingerprints, review the values, inspect evidence gaps, and ask whether any real-world decision still needs appeal, correction, source review, or independent human oversight.

        Disclaimer: This receipt is a structured mirror reading for human review. It does not certify truth, safety, legality, legitimacy, morality, institutional fitness, extraordinary claims, or policy commands. It is not public ledger proof or a replacement for human judgment. Human review remains required; the reading may be incomplete, wrong, or sensitive to missing evidence.""",
                language="text",
            )
