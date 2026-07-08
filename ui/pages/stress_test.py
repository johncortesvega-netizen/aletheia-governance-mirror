from __future__ import annotations


def render_stress_test_page(runtime_namespace: dict[str, object]) -> None:
    """Render the Stress Test page using the current app runtime namespace.

    Stage 10 keeps behavior unchanged by using a temporary namespace bridge.
    Later stages can replace this bridge with explicit imports/dependencies.
    """
    globals().update(runtime_namespace)
    with st.container():
        st.subheader("Stress Test")
        render_shared_protocol_state_notice("Stress Test", expanded=False)

        # Patch 203: keep Stress Test as a compact working surface.
        # The full module header remains available, but it no longer renders as an always-open
        # wall of explanatory text above the primary input and result.
        with st.expander("Stress Test guide and safe-use notes", expanded=False):
            render_module_page_template_intro(
                st,
                ModulePageTemplateCopy(
                    module_name="Stress Test",
                    purpose=(
                        "Try a governance scenario under pressure and inspect stability, trust, friction, "
                        "safeguards, collapse risk, and repair needs. ALETHEIA is English-first; "
                        "Dutch/Nederlands examples may appear as batch-test fixtures, not as a general "
                        "app-wide language-compatibility claim."
                    ),
                    looks_for=(
                        "Power under pressure: who gains authority, how quickly, and under what constraints.",
                        "Safeguard gaps: whether term limits, independent review, appeal, exit, or correction paths are missing.",
                        "Governance stress: whether trust, friction, grievance, alignment, and ego pressure could destabilize the scenario.",
                        "Capture pressure: whether one leader, committee, platform, institution, token group, or emergency process can dominate.",
                        "Failure-mode pressure: authority drift, evidence inflation, flattery pressure, capture pressure, sanctification drift, false neutrality, or no-appeal automation.",
                        "Repair needs: what would make the scenario more reviewable, bounded, reversible, and accountable.",
                    ),
                    safe_first_path=(
                        "Write one scenario as a governance pattern, not as a personal accusation.",
                        "Use fictional roles or the Invisibility Filter when names and titles may bias the reading.",
                        "Use Scan my idea for text-derived features; use Manual test only when you deliberately want sliders to shape the run.",
                        "Read the result as a stress reading, not as proof that a person, group, or institution is safe, unsafe, trustworthy, or untrustworthy.",
                        "Inspect repair questions before relying on the internal taxonomy label or metrics.",
                    ),
                    input_guidance="Start with your own scenario, load a demo on purpose, or use Manual test. ALETHEIA does not read examples by default. You lead.",
                    result_guidance="Treat Stress Test output as a scenario-pressure reading, not as prediction, accusation, certification, or final judgment.",
                    observed_reasons_guidance="Check the visible stress signals, feature values, tree, and protocol notes before interpreting the reading.",
                    repair_questions_guidance="Use repair questions to add safeguards, appeal paths, review limits, transparency, and exit/correction options.",
                    receipt_guidance="Stress Test receipts are local review artifacts for a scenario run; they are not public-ledger records, official findings, or decisions.",
                ),
            )

        input_mode = st.radio(
            "How do you want to work?",
            ["Scan my idea", "Manual test"],
            horizontal=True,
            help="Scan my idea reads your text. Manual test uses the sliders.",
        )

        if input_mode == "Scan my idea":
            render_stress_test_scan_intro(st)
        else:
            st.warning("Manual test is for hands-on testing. The sliders shape the result. Any text is just a note.")

        if "simulation_scenario_text" not in st.session_state:
            st.session_state.simulation_scenario_text = ""
        if "simulation_input_source" not in st.session_state:
            st.session_state.simulation_input_source = "EMPTY_INPUT"

        col_a, col_b = st.columns([1.2, 1])
        with col_a:
            scenario_choice = st.selectbox("Stress Test demo examples", list(STRESS_TEST_DEMO_SCENARIOS.keys()), key="simulation_scenario_library")
            if st.button("Load Stress Test scenario demo", use_container_width=True, key="simulation_load_stress_demo_button"):
                resolved_demo_text = STRESS_TEST_DEMO_SCENARIOS[scenario_choice]
                st.session_state.simulation_scenario_text = resolved_demo_text
                st.session_state.simulation_demo_choice = scenario_choice
                st.session_state.simulation_demo_resolved_text = resolved_demo_text
                st.session_state.simulation_input_source = "DEMO_INPUT"
            query = st.text_area("Write or paste your idea", key="simulation_scenario_text", height=150)

            loaded_demo = STRESS_TEST_DEMO_SCENARIOS.get(st.session_state.get("simulation_demo_choice", ""), None)
            if not query.strip():
                input_status = "EMPTY_INPUT"
                st.session_state.simulation_input_source = "EMPTY_INPUT"
            elif st.session_state.get("simulation_input_source") == "DEMO_INPUT" and loaded_demo is not None and query == loaded_demo:
                input_status = "DEMO_INPUT"
            else:
                input_status = "USER_INPUT"
                st.session_state.simulation_input_source = "USER_INPUT"

            if input_status == "EMPTY_INPUT":
                st.caption("Add your own idea to begin. Demos are optional and never run by themselves.")
            elif input_status == "DEMO_INPUT":
                st.caption("Demo mode is on. This is only an example.")
            else:
                st.caption("Your idea is ready. You are the source; ALETHEIA is the mirror.")

            apply_invisibility = False
            if input_mode == "Scan my idea":
                apply_invisibility = st.checkbox(
                    "Invisibility Filter",
                    value=(input_status == "USER_INPUT"),
                    key=f"simulation_invisibility_filter_{input_status}",
                    disabled=(input_status == "EMPTY_INPUT"),
                    help="Remove names and titles before review. On by default for your own input.",
                )
                if apply_invisibility and input_status != "EMPTY_INPUT":
                    st.caption("Names and titles are removed before review. The pattern stays visible.")

            selected_context = "Waiting for your input" if input_status == "EMPTY_INPUT" else ((query[:120] + "…") if len(query) > 120 else query)
            update_protocol_state(selected_context=selected_context, last_update_source="Stress Test")
            if input_mode == "Manual test":
                st.caption("Manual test mode is active: sliders shape the result directly. Scenario text is optional context, not hidden default data.")
        with col_b:
            st.markdown("### Review lens / manual test")

            default_manual_features = {
                "technical_complexity": 0.55,
                "transparency": 0.55,
                "regulation": 0.55,
                "centralization": 0.35,
                "anonymity": 0.25,
                "capital_scale": 0.35,
            }

            scenario_slider_features = default_manual_features
            if (
                input_mode == "Scan my idea"
                and st.session_state.get("last_input_mode") == "Scan my idea"
                and isinstance(st.session_state.get("last_scan"), dict)
            ):
                scenario_slider_features = build_features_from_scan(st.session_state.last_scan)

            if input_mode == "Scan my idea":
                st.caption("These features are derived from the scenario text. In Scan my idea mode they stay read-only and refresh after each run so you can see what the parser picked up.")
                slider_key_suffix = "fresh"
                if isinstance(st.session_state.get("last_scan"), dict):
                    slider_key_suffix = "_".join([
                        f"{scenario_slider_features.get('technical_complexity', 0.55):.2f}",
                        f"{scenario_slider_features.get('transparency', 0.55):.2f}",
                        f"{scenario_slider_features.get('regulation', 0.55):.2f}",
                        f"{scenario_slider_features.get('centralization', 0.35):.2f}",
                        f"{scenario_slider_features.get('anonymity', 0.25):.2f}",
                        f"{scenario_slider_features.get('capital_scale', 0.35):.2f}",
                    ])

                manual_features = {
                    "technical_complexity": st.slider("Technical complexity", 0.0, 1.0, float(scenario_slider_features.get("technical_complexity", 0.55)), 0.01, key=f"scenario_technical_complexity_{slider_key_suffix}", disabled=True),
                    "transparency": st.slider("Transparency", 0.0, 1.0, float(scenario_slider_features.get("transparency", 0.55)), 0.01, key=f"scenario_transparency_{slider_key_suffix}", disabled=True),
                    "regulation": st.slider("Regulation / oversight", 0.0, 1.0, float(scenario_slider_features.get("regulation", 0.55)), 0.01, key=f"scenario_regulation_{slider_key_suffix}", disabled=True),
                    "centralization": st.slider("Power concentration", 0.0, 1.0, float(scenario_slider_features.get("centralization", 0.35)), 0.01, key=f"scenario_centralization_{slider_key_suffix}", disabled=True),
                    "anonymity": st.slider("Anonymity / opacity", 0.0, 1.0, float(scenario_slider_features.get("anonymity", 0.25)), 0.01, key=f"scenario_anonymity_{slider_key_suffix}", disabled=True),
                    "capital_scale": st.slider("Capital scale", 0.0, 1.0, float(scenario_slider_features.get("capital_scale", 0.35)), 0.01, key=f"scenario_capital_scale_{slider_key_suffix}", disabled=True),
                }
            else:
                st.caption("These sliders shape the test. They are inputs, not hidden truth.")
                manual_features = {
                    "technical_complexity": st.slider("Technical complexity", 0.0, 1.0, default_manual_features["technical_complexity"], 0.01, key="manual_technical_complexity"),
                    "transparency": st.slider("Transparency", 0.0, 1.0, default_manual_features["transparency"], 0.01, key="manual_transparency"),
                    "regulation": st.slider("Regulation / oversight", 0.0, 1.0, default_manual_features["regulation"], 0.01, key="manual_regulation"),
                    "centralization": st.slider("Power concentration", 0.0, 1.0, default_manual_features["centralization"], 0.01, key="manual_centralization"),
                    "anonymity": st.slider("Anonymity / opacity", 0.0, 1.0, default_manual_features["anonymity"], 0.01, key="manual_anonymity"),
                    "capital_scale": st.slider("Capital scale", 0.0, 1.0, default_manual_features["capital_scale"], 0.01, key="manual_capital_scale"),
                }

        with st.expander("How to write good Stress Test scenarios", expanded=False):
            st.markdown(
                """
    Stress Test works best when you write a **scenario as a governance pattern**, not as a personal accusation. ALETHEIA is English-first; Dutch/Nederlands examples may appear in batch-test fixtures, but that is not a general language-compatibility claim.

    Include: who gains power, how power is obtained, what can go wrong, what safeguards exist or are missing, and whether affected people can appeal, exit, or request correction.

    **Weak:** `Is this bad?`

    **Better:** `A temporary crisis leader gains emergency authority after a disaster, but no term limit, appeal path, or independent review is defined.`

    **Weak:** `John is evil.`

    **Better:** `A named leader gains centralized authority after a crisis. The system has weak review, unclear limits, and no visible exit path.`

    ALETHEIA reviews patterns, not personal worth. Use fictional names or roles when testing. The Invisibility Filter can reduce actor/name/title bias while keeping the governance pattern visible.
                """
            )

        run = st.button("Run review", type="primary", use_container_width=True, key="simulation_run_button")
        if run:
            if input_mode == "Scan my idea" and input_status == "EMPTY_INPUT":
                st.warning("Add your own scenario or load a demo before running Scan my idea. ALETHEIA does not run examples by itself.")
            else:
                analysis_query = query
                invisibility_report = None
                if input_mode == "Scan my idea" and apply_invisibility and input_status != "EMPTY_INPUT":
                    invisibility_report = decouple_actor(query)
                    analysis_query = invisibility_report.get("decoupled_text", query)
                with st.spinner("Reading your idea and checking the pattern..."):
                    scan, features, sim, report, scan_mode = run_audit(analysis_query, manual_features, weights, ego_tolerance, divine_floor, steps, n_agents, input_mode)
                    st.session_state.last_scan = scan
                    st.session_state.last_features = features
                    st.session_state.last_sim = sim
                    st.session_state.last_report = report
                    st.session_state.last_scan_mode = scan_mode
                    st.session_state.last_input_mode = input_mode
                    st.session_state.last_query = analysis_query
                    st.session_state.last_query_raw = query
                    st.session_state.last_input_status = input_status
                    st.session_state.last_invisibility_report = invisibility_report
                    # Patch 208: keep the resolved demo scenario text as an explicit
                    # semantic source. Demo labels are only UI labels; the semantic
                    # layer must scan the actual scenario body and the visible editor
                    # text, then keep the strongest pressure reading.
                    demo_source_text = ""
                    if input_status == "DEMO_INPUT":
                        demo_source_text = str(loaded_demo or st.session_state.get("simulation_demo_resolved_text", "") or "")
                    st.session_state.last_demo_scenario_text = demo_source_text
                    if input_mode == "Scan my idea" and (str(query or "").strip() or str(analysis_query or "").strip() or demo_source_text.strip()):
                        st.session_state.last_stress_semantic_scan = choose_strongest_semantic_scan(
                            choose_stress_semantic_scan(query, analysis_query),
                            choose_stress_semantic_scan(demo_source_text, analysis_query) if demo_source_text else None,
                            query,
                            analysis_query,
                            demo_source_text,
                        )
                    else:
                        st.session_state.last_stress_semantic_scan = None
                    selected_context = "Manual test" if input_mode == "Manual test" else ((analysis_query[:120] + "…") if len(analysis_query) > 120 else analysis_query)
                    update_protocol_state(selected_context=selected_context, last_update_source="Stress Test")
                    if input_mode == "Scan my idea":
                        st.rerun()

        with st.expander("Stress Test Batch Testing — up to 50 scenarios", expanded=False):
            st.caption("Upload or paste scenario-style inputs. Batch testing is explicit opt-in, local-only, and creates local witness receipts.")
            stress_batch_source = st.radio(
                "Stress batch input source",
                ["Upload .txt", "Paste list"],
                horizontal=True,
                key="stress_batch_source_mode",
            )
            stress_batch_text = ""
            if stress_batch_source == "Upload .txt":
                stress_upload = st.file_uploader(
                    "Upload Stress Test .txt list",
                    type=["txt"],
                    key="stress_batch_txt_upload",
                    help="Use one scenario per line, a numbered list, or --- between longer items.",
                )
                if stress_upload is not None:
                    stress_batch_text = stress_upload.getvalue().decode("utf-8", errors="replace")
                    st.caption(f"Staged {stress_upload.name}. Press Run Stress Batch to process it.")
            else:
                stress_batch_text = st.text_area(
                    "Paste Stress Test scenarios",
                    height=180,
                    key="stress_batch_manual_input",
                    placeholder="1. A temporary leader gains emergency power without a term limit.\n2. A public service requires biometric ID before food or housing support.",
                )

            stress_batch_items = parse_witness_batch_input(stress_batch_text, max_items=MAX_BATCH_RECEIPTS)
            stress_question_set_mode = is_witness_question_set(stress_batch_items)
            if stress_batch_text.strip():
                question_note = " Question-prompt mode will keep audit/repair questions as review tools, not scored scenarios." if stress_question_set_mode else ""
                st.caption(f"{len(stress_batch_items)} item(s) ready. Maximum: {MAX_BATCH_RECEIPTS}.{question_note}")
            stress_batch_apply_invisibility = st.checkbox(
                "Apply Invisibility Filter to Stress batch",
                value=bool(stress_batch_items),
                key="stress_batch_invisibility_filter",
                disabled=not bool(stress_batch_items),
            )
            stress_batch_signature = hashlib.sha256(
                (
                    stress_batch_source
                    + "\n"
                    + stress_batch_text.strip()
                    + "\n"
                    + str(bool(stress_batch_apply_invisibility))
                ).encode("utf-8")
            ).hexdigest()
            active_stress_batch_signature = st.session_state.get("stress_batch_active_signature")
            stress_batch_has_active_results = bool(
                st.session_state.get("stress_batch_summary")
                or st.session_state.get("stress_batch_archive_bytes")
            )
            stress_batch_matches_active = (
                bool(stress_batch_text.strip())
                and bool(active_stress_batch_signature)
                and active_stress_batch_signature == stress_batch_signature
            )
            stress_batch_is_stale = stress_batch_has_active_results and not stress_batch_matches_active
            if stress_batch_is_stale:
                st.info(
                    "The Stress batch input has changed. The previous batch result is closed for this draft. "
                    "Click Run Stress Batch to create a new batch and receipts."
                )
            run_stress_batch = st.button(
                "Run Stress Batch",
                type="primary",
                use_container_width=True,
                disabled=not bool(stress_batch_items),
                key="simulation_run_stress_batch_button",
            )
            if run_stress_batch:
                stress_receipts = []
                stress_rows = []
                with st.spinner(f"Running {len(stress_batch_items)} local Stress Test scenario(s)..."):
                    for idx, raw_item in enumerate(stress_batch_items, start=1):
                        processed_item = raw_item
                        invisibility_report = None
                        if stress_batch_apply_invisibility:
                            invisibility_report = decouple_actor(raw_item)
                            processed_item = invisibility_report.get("decoupled_text", raw_item)

                        # Patch 69: a Stress Test batch can also be a bank of audit/repair
                        # questions. In that case the questions are review tools, not
                        # governance scenarios to score as Sanctuary/Threshold/Asylum.
                        if stress_question_set_mode and is_witness_question_prompt(raw_item):
                            receipt = build_local_question_prompt_receipt(
                                module="Simulation",
                                input_text=raw_item,
                                processed_text=processed_item,
                                invisibility_applied=bool(stress_batch_apply_invisibility),
                                app_version=APP_VERSION,
                            )
                            stress_report = {"integrity": None, "repair_questions": receipt.get("repair_questions", [])}
                            verdict = "QUESTION_PROMPT"
                            risk = "Review Tool"
                            label = "Audit Question / Review Tool"
                        else:
                            scan, features, sim, stress_report, scan_mode = run_audit(
                                processed_item,
                                default_manual_features,
                                weights,
                                ego_tolerance,
                                divine_floor,
                                steps,
                                n_agents,
                                "Scan my idea",
                            )
                            label, needs_review, _reason = stress_label_for_phrase(processed_item)
                            base_verdict, _base_color = classify_verdict(stress_report["integrity"])
                            verdict, risk = apply_guardrail_verdict(base_verdict, label, needs_review)
                            sim, stress_report, verdict, label, needs_review, risk = enforce_missing_safeguard_threshold_route(
                                processed_item,
                                scan,
                                sim,
                                stress_report,
                                verdict,
                                label,
                                needs_review,
                                risk,
                            )
                            label = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
                            sim = enforce_asylum_metric_consistency(sim, verdict=verdict, risk=risk, protocol_label=label)
                            stress_report = ensure_asylum_repair_questions(
                                stress_report,
                                verdict=verdict,
                                risk=risk,
                                protocol_label=label,
                                scan=scan,
                            )
                            stress_report = ensure_threshold_repair_questions(
                                stress_report,
                                verdict=verdict,
                                risk=risk,
                                protocol_label=label,
                            )
                            ai_static_context = build_ai_static_scan_protocol_context(
                                processed_item,
                                source_module="Stress Test",
                                primary_state=verdict,
                                primary_risk=risk,
                                primary_protocol_label=label,
                            )
                            stress_report["ai_static_scan_context"] = ai_static_context
                            scan["ai_static_scan_context"] = ai_static_context
                            receipt = build_local_witness_receipt(
                                module="Simulation",
                                input_text=raw_item,
                                processed_text=processed_item,
                                input_status="USER_INPUT",
                                scan=scan,
                                sim=sim,
                                report=stress_report,
                                verdict=verdict,
                                risk=risk,
                                protocol_label=label,
                                invisibility_applied=isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied", False),
                                app_version=APP_VERSION,
                            )
                        stress_receipts.append(receipt)
                        integrity_value = stress_report.get("integrity") if isinstance(stress_report, dict) else None
                        stress_review_band = review_band_for_state(verdict, stress_report, sim)
                        stress_rows.append({
                            "#": idx,
                            "State": verdict,
                            "Review zone": stress_review_band.get("label"),
                            "Risk": risk,
                            "Label": label,
                            "Integrity": "—" if integrity_value is None else round(float(integrity_value), 3),
                            "Repair questions": len((stress_report or {}).get("repair_questions") or []),
                        })
                archive_bytes, batch_index = build_local_witness_batch_zip(stress_receipts, module="Simulation", app_version=APP_VERSION)
                st.session_state.stress_batch_archive_bytes = archive_bytes
                st.session_state.stress_batch_index = batch_index
                st.session_state.stress_batch_summary = stress_rows
                st.session_state.stress_batch_active_signature = stress_batch_signature
                # Patch 142.3: a Stress Test batch is a separate workflow. If the user
                # ran one scenario first and then runs a batch, close the single-scenario
                # tree/result state so the old tree does not remain below the batch.
                for stress_single_key in [
                    "last_scan",
                    "last_features",
                    "last_sim",
                    "last_report",
                    "last_scan_mode",
                    "last_input_mode",
                    "last_query",
                    "last_query_raw",
                    "last_input_status",
                    "last_invisibility_report",
                ]:
                    st.session_state.pop(stress_single_key, None)
                st.success(f"Stress batch complete. {len(stress_receipts)} local receipt(s) are ready to download.")

            if st.session_state.get("stress_batch_summary") and not stress_batch_is_stale:
                st.dataframe(pd.DataFrame(st.session_state.stress_batch_summary), use_container_width=True, hide_index=True, height=300)
            if st.session_state.get("stress_batch_archive_bytes") and not stress_batch_is_stale:
                st.download_button(
                    "⬇️ Download Stress Test batch receipts",
                    data=st.session_state.stress_batch_archive_bytes,
                    file_name="aletheia_stress_test_batch_witness_receipts.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="simulation_download_stress_batch_receipts",
                )
            if stress_batch_is_stale and st.session_state.get("stress_batch_summary"):
                with st.expander("Last closed Stress batch", expanded=False):
                    st.caption("Previous batch results are kept for review, but downloads are hidden until the current input is explicitly run.")
                    st.dataframe(_protocol_taxonomy_ui_table_df(pd.DataFrame(st.session_state.stress_batch_summary)), use_container_width=True, hide_index=True, height=220)

        if "last_report" not in st.session_state:
            st.info("No review has run yet. Add your input, load a demo, or use the Manual test.")
        else:
            scan = st.session_state.last_scan
            features = st.session_state.last_features
            sim = st.session_state.last_sim
            report = st.session_state.last_report
            scan_mode = st.session_state.last_scan_mode
            last_input_mode = st.session_state.get("last_input_mode", input_mode)

            base_verdict, base_color = classify_verdict(report["integrity"])
            display_query = st.session_state.get("last_query", query) if last_input_mode == "Scan my idea" else ""
            label, needs_review, stress_reason = stress_label_for_phrase(display_query) if display_query else ("Manual test", "NO", "Manual numeric tuner run.")
            verdict, risk = apply_guardrail_verdict(base_verdict, label, needs_review)
            sim, report, verdict, label, needs_review, risk = enforce_missing_safeguard_threshold_route(
                display_query,
                scan,
                sim,
                report,
                verdict,
                label,
                needs_review,
                risk,
            )
            label = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
            sim = enforce_asylum_metric_consistency(sim, verdict=verdict, risk=risk, protocol_label=label)
            st.session_state.last_sim = sim
            report = ensure_asylum_repair_questions(
                report,
                verdict=verdict,
                risk=risk,
                protocol_label=label,
                scan=scan,
            )
            report = ensure_threshold_repair_questions(
                report,
                verdict=verdict,
                risk=risk,
                protocol_label=label,
            )
            if last_input_mode == "Scan my idea":
                ai_static_context = build_ai_static_scan_protocol_context(
                    st.session_state.get("last_query", display_query),
                    source_module="Stress Test",
                    primary_state=verdict,
                    primary_risk=risk,
                    primary_protocol_label=label,
                )
                report["ai_static_scan_context"] = ai_static_context
                scan["ai_static_scan_context"] = ai_static_context
            st.session_state.last_report = report
            verdict_color = {"SANCTUARY": "#8fbc8f", "THRESHOLD": "#e5c36b", "ASYLUM": "#db7777"}.get(verdict, base_color)
            input_status_label = st.session_state.get("last_input_status", "MANUAL_INPUT" if last_input_mode == "Manual test" else "USER_INPUT")
            invisibility_report = st.session_state.get("last_invisibility_report")
            invisibility_note = " · Invisibility Filter: on" if isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied") else ""
            current_review_band = review_band_for_state(verdict, report, sim)
            st.caption(f"Feature source: {last_input_mode} · Input status: {input_status_label} · Scan mode: {scan_mode} · Protocol label: {label} · Review zone: {current_review_band.get('label')}{invisibility_note}")

            c1, c2, c3, c4 = st.columns(4)
            review_band = review_band_for_state(verdict, report, sim)
            review_band_label = review_band.get("label", verdict.title())
            review_band_summary = review_band.get("summary", "")
            result_display = f"<span style='color:{verdict_color}'>{_protocol_metric_display(verdict)}</span>"
            result_display += f"<br><span style='font-size:0.9rem;color:#c9c0b2;'>Internal review label: {html.escape(str(verdict))}</span>"
            if verdict == "THRESHOLD":
                result_display += f"<br><span style='font-size:1.05rem;color:#d4b88a;'>{review_band_label}</span>"

            result_helper = f"Risk signal: {risk}<br>{_protocol_humility_note(verdict)}"
            if verdict == "THRESHOLD":
                result_helper += f"<br>Review zone: {review_band_label}"

            with c1:
                metric_card("Protocol reading", result_display, result_helper, value_is_html=True, helper_is_html=True)
            with c2:
                metric_card("Integrity", f"{report['integrity']:.3f}", "Current reading. Raw values stay in the local receipt.")
            with c3:
                metric_card("Friction", f"{report['friction']:.3f}", "Control pressure")
            with c4:
                metric_card("Collapse pressure", f"{report['collapse_probability']:.3f}", scan_mode)

            # Patch S2.1: keep the human-readable reading and repair questions above the machinery.
            # The detailed Stress Test visuals are still available, but they no longer dominate
            # the first read of the result.
            with st.expander("Stress Test visuals and agent traces", expanded=False):
                st.caption(
                    "Diagnostic visuals only. These charts explain the scenario-pressure run; "
                    "they do not create a separate decision or authority claim."
                )
                c5, c6, c7, c8 = st.columns(4)
                c5.metric("Stability", f"{sim['stability']:.3f}")
                c6.metric("Trust", f"{sim['trust_index']:.3f}")
                c7.metric("Alignment", f"{sim['alignment']:.3f}")
                c8.metric("Ego", f"{sim['ego']:.3f}")

                render_pulse_tree(
                    display_score_from_judgment(report, {"verdict": verdict}),
                    sim["ego"],
                    sim["alignment"],
                    title="Stress Test Tree",
                    state_override=verdict,
                    mode="Stress Test",
                )

                st.plotly_chart(plot_trace(sim), use_container_width=True)

                chart_col, table_col = st.columns([1, 1.2])
                with chart_col:
                    st.plotly_chart(action_chart(sim), use_container_width=True)
                with table_col:
                    st.markdown("### Test voices")
                    st.dataframe(pd.DataFrame(sim.get("agent_profiles", [])), use_container_width=True, hide_index=True)

            st.markdown("### Why this result?")
            render_soft_card_grid(
                [
                    (
                        "What ALETHEIA saw",
                        f"Source: {last_input_mode}. Power concentration {scan['power_concentration']:.0%}, transparency {scan['decision_transparency']:.0%}, regulation {scan['regulatory_presence']:.0%}.",
                    ),
                    (
                        "Pattern over time",
                        f"Trust {sim['trust_index']:.0%}, alignment {sim['alignment']:.0%}, ego {sim['ego']:.0%}.",
                    ),
                    (
                        "Risk picture",
                        f"Review zone: {review_band_label}. {review_band_summary} Collapse risk: {'yes' if sim.get('collapse_risk') else 'no'}. Trust friction: {report['trust_friction']:.3f}. Grievance pressure: {sim.get('grievance_pressure', 0):.2f}. Safeguard gap: {sim.get('safeguard_gap', 0):.2f}.",
                    ),
                ],
                columns=3,
            )

            st.markdown("### Repair questions")
            st.caption("ALETHEIA asks questions here. It gives no orders and no final judgment.")
            repair_questions = report.get("repair_questions") or []
            if repair_questions:
                render_repair_question_cards(
                    repair_questions,
                    transform=silent_operator_question,
                    context="this repair path",
                    limit=5,
                )
            else:
                render_recommendation_cards(
                    report.get("recommendations") or [],
                    transform=silent_operator_question,
                    limit=5,
                )

            if last_input_mode == "Scan my idea":
                stored_stress_semantic_scan = st.session_state.get("last_stress_semantic_scan")
                current_raw_query = str(st.session_state.get("last_query_raw", "") or "").strip()
                current_processed_query = str(display_query or "").strip()
                visible_editor_query = str(query or "").strip()
                demo_source_query = str(st.session_state.get("last_demo_scenario_text", "") or "").strip()
                recomputed_stress_semantic_scan = choose_stress_semantic_scan(current_raw_query or visible_editor_query, current_processed_query)
                editor_stress_semantic_scan = choose_stress_semantic_scan(visible_editor_query, current_processed_query) if visible_editor_query else None
                demo_stress_semantic_scan = choose_stress_semantic_scan(demo_source_query, current_processed_query) if demo_source_query else None
                stress_semantic_scan = choose_strongest_semantic_scan(
                    stored_stress_semantic_scan,
                    recomputed_stress_semantic_scan,
                    editor_stress_semantic_scan,
                    demo_stress_semantic_scan,
                    current_raw_query,
                    visible_editor_query,
                    demo_source_query,
                    current_processed_query,
                )
                if stress_semantic_scan is not None:
                    st.session_state.last_stress_semantic_scan = stress_semantic_scan
                render_semantic_stress_triggers(stress_semantic_scan, expanded=False)

            ai_static_context = report.get("ai_static_scan_context") if isinstance(report, dict) else None
            # Patch 182: AI static scan expanders inherit sky/gold expander and table styling; context remains subordinate.
            if isinstance(ai_static_context, dict):
                with st.expander("AI static scan context — subordinate to Stress Test", expanded=False):
                    st.caption(ai_static_context.get("notice"))
                    st.markdown(
                        f"**Protocol context signal:** {ai_static_context.get('protocol_context_state', ai_static_context.get('ai_static_scan_state'))} · "
                        f"{ai_static_context.get('protocol_context_risk', ai_static_context.get('ai_static_scan_risk'))} · "
                        f"{ai_static_context.get('finding_count')} AI-specific finding(s)"
                    )
                    if ai_static_context.get("alignment_note"):
                        st.caption(ai_static_context.get("alignment_note"))
                    st.caption(
                        f"Raw AI static scan only: {ai_static_context.get('ai_static_scan_state')} · "
                        f"{ai_static_context.get('ai_static_scan_risk')}"
                    )
                    if ai_static_context.get("findings"):
                        st.dataframe(pd.DataFrame(ai_static_context.get("findings")), use_container_width=True, hide_index=True)

            # Patch 203: keep receipt download opt-in so Stress Test does not become one
            # long continuous result page. The receipt payload and schema are unchanged.
            with st.expander("Download local witness receipt", expanded=False):
                render_receipt_sky_panel(
                    kicker="User-held review artifact",
                    title="Local witness receipt",
                    body="Creates a receipt you hold. It is not published, synced, enforced, or treated as authority.",
                    pills=["Local only", "No public ledger", "No Global ID sync", "Human review required"],
                )
                st.caption("Download text only. This visual card does not change the receipt content, schema, or authority boundary.")
                raw_query_for_receipt = st.session_state.get("last_query_raw", display_query)
                processed_query_for_receipt = st.session_state.get("last_query", display_query)
                receipt = build_local_witness_receipt(
                    module="Simulation",
                    input_text=raw_query_for_receipt if last_input_mode == "Scan my idea" else "Manual test numeric input",
                    processed_text=processed_query_for_receipt if last_input_mode == "Scan my idea" else "Manual test numeric input",
                    input_status=input_status_label,
                    scan=scan,
                    sim=sim,
                    report=report,
                    verdict=verdict,
                    risk=risk,
                    protocol_label=label,
                    invisibility_applied=isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied", False),
                    app_version=APP_VERSION,
                )
                receipt_text = render_local_witness_receipt_text(receipt)
                st.download_button(
                    "⬇️ Download receipt",
                    data=receipt_text,
                    file_name="aletheia_local_witness_receipt.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
