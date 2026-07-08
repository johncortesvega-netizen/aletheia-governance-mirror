from __future__ import annotations

# Patch 239: Mirror Check page extraction.
# This module receives the current app runtime namespace from app.py so the first
# page split can stay behavior-preserving. Later stages may replace this shim
# with explicit imports after the remaining app globals are consolidated.


def render_mirror_check_page(runtime: dict) -> None:
    """Render the Mirror Check page using the existing app runtime dependencies.

    Stage 9 intentionally moves the page body out of app.py without changing
    scoring, scanner behavior, session-state keys, receipt behavior, or UI copy.
    """
    globals().update(runtime)
    with st.container():
        st.subheader("Mirror Check")
        st.caption(
            "Review one bounded idea, policy, proposal, or AI output. "
            "The result is a mirror reading for human review, not a decision."
        )
        st.info(
            "Boundary: SANCTUARY / THRESHOLD / ASYLUM are internal review labels. "
            "Metrics are directional pressure readings, not approval, rejection, certification, or final truth."
        )

        with st.expander("Module guidance and protocol context", expanded=False):
            render_shared_protocol_state_notice("Mirror Check")
            render_audit_module_integrity_panel()
            render_module_page_template_intro(
                st,
                ModulePageTemplateCopy(
                    module_name="Mirror Check",
                    purpose=(
                        "Review one document, idea, proposal, policy text, or AI output for pressure signals, "
                        "missing safeguards, review needs, and repair questions. ALETHEIA is English-first; "
                        "Dutch/Nederlands examples may be used for batch testing, not as a general app-wide "
                        "language-compatibility claim."
                    ),
                    looks_for=(
                        "Care alignment: whether the idea protects people, dignity, consent, and non-harm.",
                        "Power language: whether soft wording hides control, coercion, ranking, punishment, or authority drift.",
                        "Evidence and reviewability: whether reasons, sources, and assumptions can be inspected by another human reviewer.",
                        "Appeal and repair: whether affected people have explanation, contestation, correction, and human-review paths.",
                        "Failure-mode pressure: authority drift, evidence inflation, flattery pressure, capture pressure, sanctification drift, false neutrality, or no-appeal automation.",
                        "Witness receipt: whether a local review record is useful for later human inspection.",
                    ),
                    safe_first_path=(
                        "Paste one short item, not a whole archive of mixed cases.",
                        "Use optional demos only for orientation; they never run by themselves.",
                        "Read the protocol-adjusted label as a bounded signal, not a decision.",
                        "Inspect observed reasons, values, and repair questions before relying on the reading.",
                        "Download a receipt only when you want a local review record.",
                    ),
                    input_guidance="Use this module for one bounded text item. Use the batch-testing panel only for deliberate local test batches.",
                    result_guidance="Treat the result as a mirror reading of pressure and review needs, not as approval, rejection, certification, or final truth.",
                    observed_reasons_guidance="Check which signals drove the reading before trusting any label, metric, or repair suggestion.",
                    repair_questions_guidance="Use repair questions to strengthen evidence, safeguards, appeal paths, and human review.",
                    receipt_guidance="Mirror Check receipts are local review artifacts held by the user; they are not public-ledger records, official determinations, or authorization.",
                ),
            )

        if "chat_audit_history" not in st.session_state:
            st.session_state.chat_audit_history = []

        if "audit_chat_query" not in st.session_state:
            st.session_state.audit_chat_query = ""
        if "audit_chat_input_source" not in st.session_state:
            st.session_state.audit_chat_input_source = "EMPTY_INPUT"

        def mirror_active_input_signature(text_value: str) -> str:
            """Stable signature for the currently typed Mirror Check input.

            Patch 72.2: prevents an old assessment/receipt from staying active after
            the user edits the input box. History may remain, but a changed input
            requires an explicit new Review idea click.
            """
            return hashlib.sha256((text_value or "").strip().encode("utf-8")).hexdigest()

        def run_chat_audit_from_text(text_value: str, raw_text_value=None, input_source: str = "USER_INPUT", invisibility_report=None, store_history: bool = True, force_local: bool = False):
            raw_text_value = text_value if raw_text_value is None else raw_text_value
            scan = governance_scan(text_value, force_local=force_local)
            scan = apply_capture_feature_override(text_value, scan)
            semantic_pressure_scan = scan_semantic_pressure(text_value, governance_context=True)
            semantic_pressure_payload = semantic_pressure_scan.to_dict()
            scan["semantic_pressure_scan"] = semantic_pressure_payload
            scan["semantic_pressure_report"] = format_semantic_pressure_report(semantic_pressure_scan)
            features = build_features_from_scan(scan)
            np.random.seed(deterministic_seed_from_payload(text_value, features, weights, ego_tolerance, divine_floor, steps, n_agents, "chat"))
            sim = simulate(
                features,
                weights,
                ego_tolerance=ego_tolerance,
                divine_floor=divine_floor,
                steps=steps,
                n_agents=n_agents,
            )
            if scan.get("capture_override"):
                sim["stability"] = min(float(sim.get("stability", 1.0)), 0.39)
                sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.62)
                sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.58)
                sim["ego"] = max(float(sim.get("ego", 0.0)), 0.28)
                sim["collapse_risk"] = True
                sim["structural_capture_risk"] = max(float(sim.get("structural_capture_risk", 0.0)), 0.88)
                sim["structural_risk"] = max(float(sim.get("structural_risk", 0.0)), 0.88)
                sim["grievance_pressure"] = max(float(sim.get("grievance_pressure", 0.0)), 0.35)
                sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.72)
                sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.35)
            report = full_report(sim)
            report["cognitive_resilience_diagnostics"] = evaluate_cognitive_resilience(
                text_value, governance_result=scan, features=features
            )
            report = apply_cognitive_resilience_to_metrics(
                report, report.get("cognitive_resilience_diagnostics")
            )
            ethics_diagnostics = evaluate_ethics(text_value, governance_result=scan, features=features)
            # Patch 22: make visible Mirror Check metrics reflect contextual ethics pressure.
            # Protocol hard overrides still take precedence; this only calibrates the numeric layer.
            sim, report = apply_ethics_to_metrics(sim, report, ethics_diagnostics)
            report["ethics_diagnostics"] = ethics_diagnostics
            report["semantic_pressure_scan"] = semantic_pressure_payload
            report["semantic_pressure_report"] = scan["semantic_pressure_report"]
            if force_local:
                judgment, source = local_governance_judgment(text_value, scan, sim, report), "Local batch scan"
            else:
                judgment, source = llm_governance_judgment(text_value, scan, sim, report)
            judgment = positive_cr_baseline_stabilizer(judgment, report)

            # Patch 75: Mirror Check must not display or receipt ASYLUM / High
            # readings with THRESHOLD-style trust/alignment/ego metrics. The cap is
            # display/receipt calibration only; it does not create authority or
            # enforcement. Raw pre-ethics values remain in the receipt when present.
            mirror_verdict = str(judgment.get("verdict", "THRESHOLD")).upper()
            mirror_risk = str(judgment.get("corruption_risk", judgment.get("guardrail_risk", "Medium")))
            mirror_label = normalize_asylum_protocol_label(
                judgment.get("stress_label", mirror_verdict),
                verdict=mirror_verdict,
                risk=mirror_risk,
            )
            judgment["stress_label"] = mirror_label
            sim = enforce_asylum_metric_consistency(
                sim,
                verdict=mirror_verdict,
                risk=mirror_risk,
                protocol_label=mirror_label,
            )
            report = ensure_asylum_repair_questions(
                report,
                verdict=mirror_verdict,
                risk=mirror_risk,
                protocol_label=mirror_label,
                scan=scan,
            )

            ai_static_context = build_ai_static_scan_protocol_context(
                text_value,
                source_module="Mirror Check",
                primary_state=mirror_verdict,
                primary_risk=mirror_risk,
                primary_protocol_label=mirror_label,
            )
            report["ai_static_scan_context"] = ai_static_context
            scan["ai_static_scan_context"] = ai_static_context

            entry = {
                "query": text_value,
                "raw_query": raw_text_value,
                "input_source": input_source,
                "invisibility_report": invisibility_report,
                "scan": scan,
                "sim": sim,
                "report": report,
                "ethics_diagnostics": ethics_diagnostics,
                "semantic_pressure_scan": semantic_pressure_payload,
                "judgment": judgment,
                "source": source,
                "source_hits": source_conformance_hits(text_value),
            }
            if store_history:
                st.session_state.chat_audit_history.insert(0, entry)
            return entry

        def build_mirror_receipt_for_entry(latest):
            invisibility_note = latest.get("invisibility_report")
            mirror_invisibility_applied = isinstance(invisibility_note, dict) and invisibility_note.get("invisibility_filter_applied", False)
            mirror_receipt_report = dict(latest["report"] or {})
            mirror_receipt_report["repair_questions"] = (
                latest["judgment"].get("questions")
                or mirror_receipt_report.get("repair_questions")
                or []
            )
            if latest.get("ethics_diagnostics"):
                mirror_receipt_report["ethics_diagnostics"] = latest["ethics_diagnostics"]
                mirror_receipt_report["ethics_adjusted_integrity"] = min(
                    float(mirror_receipt_report.get("integrity", 1.0) or 1.0),
                    float(latest["ethics_diagnostics"].get("ethics_score", 1.0) or 1.0),
                )
            mirror_receipt = build_local_witness_receipt(
                module="Mirror Check",
                input_text=latest.get("raw_query", latest["query"]),
                processed_text=latest["query"],
                input_status=latest.get("input_source", "USER_INPUT"),
                scan=latest["scan"],
                sim=latest["sim"],
                report=mirror_receipt_report,
                verdict=latest["judgment"].get("verdict", "THRESHOLD"),
                risk=latest["judgment"].get("corruption_risk", "Medium"),
                protocol_label=latest["judgment"].get("stress_label", latest["judgment"].get("verdict", "THRESHOLD")),
                invisibility_applied=mirror_invisibility_applied,
                app_version=APP_VERSION,
            )
            return mirror_receipt

        def run_mirror_batch_review(batch_items, *, apply_invisibility: bool, batch_label: str = "ideas"):
            """Review a bounded Mirror Check batch and prepare one local zip archive."""
            receipts = []
            summaries = []
            question_set_mode = is_witness_question_set(batch_items)
            with st.spinner(f"Reviewing {len(batch_items)} {batch_label} and preparing local receipts..."):
                for idx, raw_item in enumerate(batch_items, start=1):
                    processed_item = raw_item
                    invisibility_report = None
                    if apply_invisibility:
                        invisibility_report = decouple_actor(raw_item)
                        processed_item = invisibility_report.get("decoupled_text", raw_item)

                    # A batch of audit questions is a review tool, not one or more policy proposals.
                    # Keep risky terms visible for later human review without escalating the question itself.
                    if question_set_mode and is_witness_question_prompt(raw_item):
                        receipt = build_local_question_prompt_receipt(
                            module="Mirror Check",
                            input_text=raw_item,
                            processed_text=processed_item,
                            invisibility_applied=bool(apply_invisibility),
                            app_version=APP_VERSION,
                        )
                    else:
                        entry = run_chat_audit_from_text(
                            processed_item,
                            raw_text_value=raw_item,
                            input_source="USER_INPUT",
                            invisibility_report=invisibility_report,
                            store_history=False,
                            force_local=True,
                        )
                        receipt = build_mirror_receipt_for_entry(entry)
                    receipts.append(receipt)
                    verdict = receipt.get("verdict", {}) or {}
                    summaries.append({
                        "#": idx,
                        "State": verdict.get("protocol_adjusted_state"),
                        "Risk": verdict.get("risk"),
                        "Label": verdict.get("protocol_label"),
                    })
            archive_bytes, batch_index = build_local_witness_batch_zip(
                receipts, module="Mirror Check", app_version=APP_VERSION
            )
            st.session_state.audit_batch_archive_bytes = archive_bytes
            st.session_state.audit_batch_index = batch_index
            st.session_state.audit_batch_summary = summaries
            st.session_state.audit_batch_count = len(receipts)
            return receipts

        # Mirror Check keeps the primary path visually dominant. Batch testing remains
        # available on the side, but the first visible action is one bounded review.
        normal_review_col, batch_testing_col = st.columns([0.68, 0.32], gap="large")

        with normal_review_col:
            st.markdown("### Review one bounded idea")
            st.caption("Paste one bounded item. The tree scanner runs only after you press Review idea.")

            with st.expander("Optional demo inputs", expanded=False):
                st.caption("Demo inputs are fictional and opt-in. They load only when you click; they never run by themselves.")
                demo_input_choice = st.selectbox(
                    "Demo input library",
                    [name for name, _ in DEMO_INPUT_FILES],
                    key="mirror_demo_input_library",
                )
                demo_input_map = dict(DEMO_INPUT_FILES)
                if st.button("Load demo input", use_container_width=True, key="mirror_load_demo_input_button"):
                    demo_text = load_demo_input(demo_input_map[demo_input_choice])
                    st.session_state.audit_chat_query = demo_text
                    st.session_state.audit_demo_choice = demo_input_choice
                    st.session_state.audit_demo_loaded_text = demo_text
                    st.session_state.audit_chat_input_source = "DEMO_INPUT"
                    st.info("Demo input loaded. Click Review idea if you want ALETHEIA to analyze it.")

                audit_demo_choice = st.selectbox("Mirror Check scenario examples", list(MIRROR_CHECK_DEMO_SCENARIOS.keys()), key="audit_demo_library")
                if st.button("Load scenario demo", use_container_width=True, key="audit_load_demo_button"):
                    demo_text = MIRROR_CHECK_DEMO_SCENARIOS[audit_demo_choice]
                    st.session_state.audit_chat_query = demo_text
                    st.session_state.audit_demo_choice = audit_demo_choice
                    st.session_state.audit_demo_loaded_text = demo_text
                    st.session_state.audit_chat_input_source = "DEMO_INPUT"

            chat_query = st.text_area(
                "Write or paste the idea you want reviewed",
                height=170,
                key="audit_chat_query",
            )
            if "chat_audit_query" in st.session_state and "audit_chat_query" not in st.session_state:
                st.session_state.audit_chat_query = st.session_state.chat_audit_query

            loaded_audit_demo = st.session_state.get("audit_demo_loaded_text") or MIRROR_CHECK_DEMO_SCENARIOS.get(st.session_state.get("audit_demo_choice", ""), None)
            if not chat_query.strip():
                audit_input_status = "EMPTY_INPUT"
                st.session_state.audit_chat_input_source = "EMPTY_INPUT"
            elif st.session_state.get("audit_chat_input_source") == "DEMO_INPUT" and loaded_audit_demo is not None and chat_query == loaded_audit_demo:
                audit_input_status = "DEMO_INPUT"
            else:
                audit_input_status = "USER_INPUT"
                st.session_state.audit_chat_input_source = "USER_INPUT"

            if audit_input_status == "EMPTY_INPUT":
                st.caption("Add your own idea to begin. Demos are optional and never run by themselves.")
            elif audit_input_status == "DEMO_INPUT":
                st.caption("Demo mode is on. This reading is only an example.")
            else:
                st.caption("Your idea is ready. You are the source; ALETHEIA is the mirror.")

            audit_apply_invisibility = st.checkbox(
                "Invisibility Filter",
                value=(audit_input_status == "USER_INPUT"),
                key=f"audit_invisibility_filter_{audit_input_status}",
                disabled=(audit_input_status == "EMPTY_INPUT"),
                help="Remove names and titles before review. On by default for your own input.",
            )
            if audit_apply_invisibility and audit_input_status != "EMPTY_INPUT":
                st.caption("Names and titles are removed before review. The pattern stays visible.")

            c_run, c_clear = st.columns([1, 0.35])
            with c_run:
                run_chat = st.button("Review idea", type="primary", use_container_width=True)
            with c_clear:
                clear_chat = st.button("Clear results", use_container_width=True)

        with batch_testing_col:
            st.markdown("### Batch testing")
            st.caption("Optional local test bench for lists. Keep closed unless you need batch receipts.")

            # Batch testing is intentionally separate from the single Mirror Check / tree scanner flow.
            # It opens on the right side after a user click, runs local-only batch scans, and writes a ZIP of receipts.
            if "audit_batch_testing_open" not in st.session_state:
                st.session_state.audit_batch_testing_open = False

            if st.button("Batch Testing — up to 50 lines", use_container_width=True, key="audit_open_batch_testing_button"):
                st.session_state.audit_batch_testing_open = not st.session_state.audit_batch_testing_open

            if not st.session_state.audit_batch_testing_open:
                st.info("Open Batch Testing when you want to upload or paste a list.")

            if st.session_state.audit_batch_testing_open:
                with st.container(border=True):
                    st.caption("Upload a .txt file or paste up to 50 lines. This bench stays separate from the tree scanner.")

                    if "audit_batch_upload_signature" not in st.session_state:
                        st.session_state.audit_batch_upload_signature = ""
                    if "audit_batch_last_source" not in st.session_state:
                        st.session_state.audit_batch_last_source = "EMPTY"

                    batch_source = st.radio(
                        "Batch input source",
                        ["Upload .txt", "Paste list"],
                        horizontal=True,
                        key="audit_batch_source_mode",
                        help="Like Evidence Lab, uploaded files are staged first and only processed when you press Run Batch Testing.",
                    )

                    batch_upload_text = ""
                    batch_manual_text = ""
                    batch_upload = None

                    if batch_source == "Upload .txt":
                        batch_upload = st.file_uploader(
                            "Upload .txt list for batch only",
                            type=["txt"],
                            key="audit_batch_txt_upload",
                            help="Use one phrase per line, a numbered list, or --- between longer items.",
                        )
                        if batch_upload is not None:
                            uploaded_batch_bytes = batch_upload.getvalue()
                            batch_upload_text = uploaded_batch_bytes.decode("utf-8", errors="replace")
                            upload_signature = hashlib.sha256(uploaded_batch_bytes + batch_upload.name.encode("utf-8", errors="replace")).hexdigest()
                            if upload_signature != st.session_state.audit_batch_upload_signature:
                                st.session_state.audit_batch_upload_signature = upload_signature
                                st.session_state.audit_batch_last_source = f"UPLOAD:{batch_upload.name}"
                                st.session_state.audit_batch_summary = []
                                st.session_state.audit_batch_archive_bytes = None
                                st.session_state.audit_batch_index = None
                                st.session_state.audit_batch_count = 0
                            st.caption(f"Staged {batch_upload.name}. Press Run Batch Testing to process it.")
                            with st.expander("Preview uploaded batch text", expanded=False):
                                st.text_area(
                                    "Uploaded text preview",
                                    value=batch_upload_text[:12000],
                                    height=180,
                                    disabled=True,
                                    key="audit_batch_upload_preview",
                                )
                        else:
                            st.caption("Choose a .txt file, then press Run Batch Testing.")
                    else:
                        batch_manual_text = st.text_area(
                            "Paste batch phrases or questions",
                            height=220,
                            key="audit_batch_manual_input",
                            placeholder="1. Who can appeal this decision?\n2. Where is the human override?\n---\nA system cannot be questioned and has no appeal path.",
                        )

                    batch_text = batch_upload_text if batch_source == "Upload .txt" else batch_manual_text
                    batch_items = parse_witness_batch_input(batch_text, max_items=MAX_BATCH_RECEIPTS)
                    batch_ready = bool(batch_items)
                    if batch_text.strip():
                        question_set_ready = is_witness_question_set(batch_items)
                        mode_note = " Question set mode will keep audit prompts as review tools." if question_set_ready else ""
                        st.caption(f"{len(batch_items)} line(s) ready. Maximum: {MAX_BATCH_RECEIPTS}.{mode_note}")
                    else:
                        st.caption("Batch Testing waits until you upload or paste a list.")

                    batch_apply_invisibility = st.checkbox(
                        "Apply Invisibility Filter to batch",
                        value=batch_ready,
                        key="audit_batch_invisibility_filter",
                        disabled=not batch_ready,
                        help="Removes names and titles from each item before local review. Raw input hashes stay in each receipt.",
                    )
                    run_batch = st.button(
                        "Run Batch Testing",
                        type="primary",
                        use_container_width=True,
                        disabled=not batch_ready,
                        key="audit_run_batch_button",
                    )
                    if run_batch:
                        receipts = run_mirror_batch_review(
                            batch_items,
                            apply_invisibility=batch_apply_invisibility,
                            batch_label="batch item(s)",
                        )
                        st.success(f"Batch complete. {len(receipts)} local receipt(s) are ready to download.")

                    if st.session_state.get("audit_batch_summary"):
                        batch_summary_df = pd.DataFrame(st.session_state.audit_batch_summary)
                        batch_display_df = batch_summary_df.rename(columns={
                            "State": "Type",
                            "Risk": "Role",
                            "Label": "Reading",
                        })
                        batch_display_df["Type"] = batch_display_df["Type"].replace({
                            "QUESTION_PROMPT": "Question",
                            "OUT_OF_SCOPE": "Needs context",
                            "SANCTUARY": "Sanctuary",
                            "THRESHOLD": "Threshold",
                            "ASYLUM": "Asylum",
                        })
                        batch_display_df["Role"] = batch_display_df["Role"].replace({
                            "Review Tool": "Review",
                            "None": "Context",
                        })
                        batch_display_df["Reading"] = batch_display_df["Reading"].replace({
                            "Audit Question / Review Tool": "Audit question",
                            "Out-of-Scope / Needs Context": "Needs more context",
                        })
                        # Keep the narrow side panel readable: fold Role into Reading instead of hiding a third column.
                        batch_display_df["Reading"] = batch_display_df.apply(
                            lambda row: f"{row['Reading']} · {row['Role']}" if row.get("Role") else row["Reading"],
                            axis=1,
                        )
                        batch_display_df = batch_display_df[["#", "Type", "Reading"]]
                        st.dataframe(
                            batch_display_df,
                            use_container_width=True,
                            hide_index=True,
                            height=360,
                            column_config={
                                "#": st.column_config.NumberColumn("#", width="small"),
                                "Type": st.column_config.TextColumn("Type", width="small"),
                                "Reading": st.column_config.TextColumn("Reading", width="large"),
                            },
                        )
                    if st.session_state.get("audit_batch_archive_bytes"):
                        st.download_button(
                            "⬇️ Download full batch archive (.zip)",
                            data=st.session_state.audit_batch_archive_bytes,
                            file_name="aletheia_mirror_check_batch_witness_receipts.zip",
                            mime="application/zip",
                            use_container_width=True,
                        )

        selected_chat_context = "Waiting for your input" if audit_input_status == "EMPTY_INPUT" else ((chat_query[:120] + "…") if len(chat_query) > 120 else chat_query)
        update_protocol_state(selected_context=selected_chat_context, last_update_source="Mirror Check")

        if clear_chat:
            st.session_state.chat_audit_history = []
            st.rerun()

        if run_chat:
            if not st.session_state.audit_chat_query.strip():
                st.warning("Add your own idea or load a demo before review. ALETHEIA does not run examples by itself.")
            else:
                audit_analysis_query = st.session_state.audit_chat_query
                audit_invisibility_report = None
                if audit_apply_invisibility and audit_input_status != "EMPTY_INPUT":
                    audit_invisibility_report = decouple_actor(st.session_state.audit_chat_query)
                    audit_analysis_query = audit_invisibility_report.get("decoupled_text", st.session_state.audit_chat_query)
                with st.spinner("Reading the idea and preparing the review..."):
                    run_chat_audit_from_text(
                        audit_analysis_query,
                        raw_text_value=st.session_state.audit_chat_query,
                        input_source=audit_input_status,
                        invisibility_report=audit_invisibility_report,
                    )
                    st.session_state.audit_active_input_signature = mirror_active_input_signature(st.session_state.audit_chat_query)
                    update_protocol_state(selected_context=(audit_analysis_query[:120] + "…") if len(audit_analysis_query) > 120 else audit_analysis_query, last_update_source="Mirror Check")
                st.rerun()

        st.markdown("---")

        # Latest result appears immediately after the question box, but only when
        # it still belongs to the currently visible input.
        if st.session_state.chat_audit_history:
            latest = st.session_state.chat_audit_history[0]
            latest_raw_query = str(latest.get("raw_query", latest.get("query", "")) or "")
            current_input_signature = mirror_active_input_signature(chat_query)
            latest_input_signature = mirror_active_input_signature(latest_raw_query)
            active_input_signature = st.session_state.get("audit_active_input_signature", latest_input_signature)
            latest_matches_current_input = (
                bool(chat_query.strip())
                and current_input_signature == latest_input_signature
                and active_input_signature == latest_input_signature
            )

            if latest_matches_current_input:
                st.markdown("### Latest reading")
                if latest.get("input_source") == "DEMO_INPUT":
                    st.caption("Demo mode was used. This reading is only an example.")
                invisibility_note = latest.get("invisibility_report")
                if isinstance(invisibility_note, dict) and invisibility_note.get("invisibility_filter_applied"):
                    st.caption("Names and titles were removed before this review.")
                render_pulse_tree(
                    display_score_from_judgment(latest["report"], latest["judgment"]),
                    latest["sim"]["ego"],
                    latest["sim"]["alignment"],
                    title="Mirror Reading Tree",
                    state_override=str(latest.get("judgment", {}).get("verdict", "THRESHOLD")).upper(),
                    mode="Mirror Check",
                )
                render_chat_judgment(latest["judgment"], latest["source"], latest["report"], latest.get("sim"), latest.get("scan"))

                semantic_payload = latest.get("semantic_pressure_scan")
                if not semantic_payload and isinstance(latest.get("report"), dict):
                    semantic_payload = latest["report"].get("semantic_pressure_scan")
                if not semantic_payload and isinstance(latest.get("scan"), dict):
                    semantic_payload = latest["scan"].get("semantic_pressure_scan")
                if not semantic_payload:
                    semantic_payload = latest.get("query", "")
                render_semantic_pressure_panel(semantic_payload, source_label="Mirror Check", expanded=False, panel_key="mirror_check_latest_semantic_pressure")

                st.markdown("### Mirror Check support context")
                support_columns = st.columns(2, gap="large")
                source_hits = latest.get("source_hits", source_conformance_hits(latest["query"]))
                with support_columns[0]:
                    with st.expander("Source match hits", expanded=False):
                        if source_hits:
                            st.dataframe(pd.DataFrame(source_hits), use_container_width=True, hide_index=True)
                        else:
                            st.caption("No named source concept matched this idea in the current detector set.")

                ai_static_context = latest.get("report", {}).get("ai_static_scan_context") if isinstance(latest.get("report"), dict) else None
                # Patch 182: AI static scan context uses the same sky/gold expander treatment as other aligned review panels.
                with support_columns[1]:
                    with st.expander("AI static scan context — subordinate to Mirror Check", expanded=False):
                        if isinstance(ai_static_context, dict):
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
                        else:
                            st.caption("No subordinate AI static scan context was attached to this Mirror Check reading.")

                # Patch 183: visual-only Mirror Check receipt framing; receipt payload and schema remain unchanged.
                st.markdown(
                    """
                    <div class="receipt-sky-panel">
                      <div class="receipt-kicker">Mirror Check artifact</div>
                      <div class="receipt-title">Local witness receipt</div>
                      <div class="receipt-body">Creates a receipt you hold. It is not published, synced, enforced, or treated as authority.</div>
                      <div class="receipt-boundary-strip">
                        <span class="receipt-boundary-pill">User-held text file</span>
                        <span class="receipt-boundary-pill">No central storage</span>
                        <span class="receipt-boundary-pill">No public ledger</span>
                        <span class="receipt-boundary-pill">Human review required</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption("Download text only. This visual card does not change the receipt content, schema, or authority boundary.")
                mirror_receipt = build_mirror_receipt_for_entry(latest)
                mirror_receipt_text = render_local_witness_receipt_text(mirror_receipt)
                st.download_button(
                    "⬇️ Download receipt",
                    data=mirror_receipt_text,
                    file_name="aletheia_mirror_check_local_witness_receipt.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

                with st.expander("Scanner features used for this reading"):
                    st.json(latest["scan"])
            else:
                st.info("The input has changed. The previous assessment is closed for this draft. Click Review idea to create a new reading and receipt.")
                with st.expander("Last closed reading", expanded=False):
                    verdict = latest["judgment"].get("verdict", "THRESHOLD")
                    risk = latest["judgment"].get("corruption_risk", "Medium")
                    st.markdown(f"**{verdict} · {risk} risk**")
                    st.caption(latest_raw_query[:240] + ("..." if len(latest_raw_query) > 240 else ""))

            previous_items = st.session_state.chat_audit_history[1:] if latest_matches_current_input else st.session_state.chat_audit_history
            if previous_items:
                with st.expander("Previous readings"):
                    for idx, item in enumerate(previous_items, start=1):
                        verdict = item["judgment"].get("verdict", "THRESHOLD")
                        risk = item["judgment"].get("corruption_risk", "Medium")
                        st.markdown(f"**{idx}. {verdict} · {risk} risk**")
                        st.caption(item["query"][:240] + ("..." if len(item["query"]) > 240 else ""))
        else:
            st.caption("No reading yet. Share one idea above to create a Mirror Reading Tree.")




