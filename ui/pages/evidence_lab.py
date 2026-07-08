from __future__ import annotations


def render_evidence_lab_page(runtime_namespace: dict[str, object]) -> None:
    """Render the Evidence Lab page using the current app runtime namespace.

    Stage 11 keeps behavior unchanged by using a temporary namespace bridge.
    Later stages can replace this bridge with explicit imports/dependencies.
    """
    globals().update(runtime_namespace)
    with st.container():
        render_evidence_lab_intro(st)
        render_shared_protocol_state_notice("Evidence Lab", expanded=False)

        # Patch 169: Evidence Lab now uses compact opt-in panels from
        # pages_ui.evidence_lab_page.render_evidence_lab_intro. Keep the
        # interactive template and upload workflow below, but stop the top of the
        # tab from opening long guidance blocks by default.

        with st.expander("Semantic claim/mechanism evidence check", expanded=False):
            st.caption(
                "Optional S2 diagnostic: inspect whether a claim relies on soft value language, concrete mechanisms, "
                "access conditions, identity gates, or reversible safeguards. This does not score the country-year table."
            )
            semantic_evidence_text = st.text_area(
                "Claim, policy sentence, or evidence-summary text",
                value="This system protects dignity, safety, harmony, inclusion, and public trust.",
                height=120,
                key="evidence_lab_semantic_claim_text",
                help="Use this for claim/mechanism review before or alongside source scoring.",
            )
            render_semantic_evidence_check(semantic_evidence_text, expanded_details=False)

        with st.expander("Evidence status template", expanded=False):
            evidence_examples = {
                "Strong evidence": "Multiple public, relevant, reviewable sources support the claim.",
                "Partial evidence": "Some evidence exists, but coverage, independence, relevance, or completeness is limited.",
                "Weak evidence": "The claim is mostly asserted, anecdotal, internally sourced, or insufficiently documented.",
                "No evidence supplied": "No reviewable support is provided for the claim.",
                "Unverified extraordinary claim": "The claim may be personally meaningful, but it is not used as policy authority without public, testable, non-coercive evidence and human review.",
            }
            selected_evidence_level = st.selectbox(
                "Evidence status example",
                list(evidence_examples.keys()),
                key="evidence_status_example_selector",
                help="Template-level calibration only. Evidence status is a review signal, not a final truth claim.",
            )
            st.code(
                f"""Evidence Lab Review

        Plain-English receipt summary
        What is this document?
        This is an Evidence Lab review note. It records a claim, the visible evidence status, evidence gaps, and review questions. It is not proof, certification, or authority.

        The main results
        Claim reviewed: [insert claim]
        Evidence status: {selected_evidence_level}
        Reason: {evidence_examples[selected_evidence_level]}

        How power and control are distributed
        Evidence Lab asks whether a claim is supported by public, relevant, reviewable evidence or whether power is being moved through unsupported certainty, stale sources, hidden assumptions, or extraordinary claims without evidence.

        Next steps and questions
        Evidence gaps: identify unsupported assertions, missing sources, stale data, self-referential sources, or unreviewable claims.
        Extraordinary claim handling: treat as unverified unless supported by public, testable, non-coercive evidence.
        Policy consequence audit: review effects on basic rights, free agency, coercion, transparency, appeal, accountability, and repair.
        Human review disclaimer: Evidence Lab is a mirror for human review. It is not a proof engine, oracle, legal judgment, religious authority, or enforcement authority.""",
                language="text",
            )


        with st.expander("Data sources → ALETHEIA fields → Protocol view", expanded=False):
            st.markdown(
                "**Flow:** public evidence → variable mapping → scoring → protocol overlay → review."
            )
            st.markdown("#### Data source map")
            source_df = evidence_source_frame()
            visible_source_cols = ["Evidence source", "What it contributes", "ALETHEIA use"]
            st.dataframe(source_df[visible_source_cols], use_container_width=True, hide_index=True, height=300)
            with st.expander("Protocol details by source", expanded=False):
                st.dataframe(
                    source_df[["Evidence source", "Protocol overlay"]],
                    use_container_width=True,
                    hide_index=True,
                    height=300,
                )
            st.markdown("#### Field mapping")
            st.dataframe(variable_mapping_frame(), use_container_width=True, hide_index=True, height=300)
            st.caption(
                "External outcome columns do not change the score. They are for later checks against real-world outcomes."
            )

        with st.expander("Needed and helpful columns", expanded=False):
            st.markdown("**Required identity columns**")
            st.code("country, iso3, year", language="text")
            st.markdown("**Needed for real 9k allocation**")
            st.code("population", language="text")
            st.markdown("**Helpful empirical columns**")
            helpful_empirical_columns = [c for c in EMPIRICAL_COLUMNS if c != "population"]
            st.code("\n".join(helpful_empirical_columns), language="text")
            st.caption("Scale expectations: WGI fields can use their normal -2.5 to +2.5 scale. V-Dem and trust fields should already be 0–1.")


        with st.expander("Advanced: build/upload country-year evidence table", expanded=False):
            st.caption("Open this only when you want to upload WGI/population/V-Dem/trust files or rebuild the country-year table. The semantic evidence check above stays separate from empirical scoring.")
            render_evidence_lab_public_data_build_intro(st)

            with st.expander("How to get and prepare the first real dataset", expanded=False):
                st.markdown(ingestion_notes_markdown())
                st.info(
                    "This uploader does not hard-code a live web download. That makes the workflow reliable on Streamlit Cloud: "
                    "download the public data from the official source, then upload the file here."
                )

            ingest_cols = st.columns(2)
            with ingest_cols[0]:
                wgi_upload = st.file_uploader(
                    "Upload World Bank WGI CSV/XLS/XLSX",
                    type=["csv", "xls", "xlsx"],
                    key="wgi_ingest_upload",
                    help="Accepts common WGI long or wide layouts. Required fields: country, iso3/country code, year, and indicator/value or WGI columns.",
                )
            with ingest_cols[1]:
                pop_upload = st.file_uploader(
                    "Optional population CSV/XLS/XLSX",
                    type=["csv", "xls", "xlsx"],
                    key="population_ingest_upload",
                    help="Required for real 9k seat allocation. Needs country, iso3/country code, year, and population/value columns.",
                )

            optional_cols = st.columns(2)
            with optional_cols[0]:
                vdem_upload = st.file_uploader(
                    "Optional V-Dem/ALETHEIA-compatible file",
                    type=["csv", "xls", "xlsx"],
                    key="vdem_ingest_upload",
                    help="Use country, iso3, year plus columns such as vdem_executive_constraints and vdem_democracy.",
                )
            with optional_cols[1]:
                trust_upload = st.file_uploader(
                    "Optional trust/ALETHEIA-compatible file",
                    type=["csv", "xls", "xlsx"],
                    key="trust_ingest_upload",
                    help="Use country, iso3, year plus wvs_generalized_trust, or upload OWID self-reported trust attitudes CSV directly (Entity/Code/Year plus most-people-can-be-trusted indicator).",
                )

            build_master = st.button("Build master CSV from uploads", use_container_width=True)
            if build_master:
                try:
                    with st.spinner("Reading uploads and building country-year master table..."):
                        wgi_df = read_public_data_upload(wgi_upload) if wgi_upload is not None else None
                        pop_df = read_public_data_upload(pop_upload) if pop_upload is not None else None
                        vdem_df = read_public_data_upload(vdem_upload) if vdem_upload is not None else None
                        trust_df = read_public_data_upload(trust_upload) if trust_upload is not None else None
                        if all(x is None for x in [wgi_df, pop_df, vdem_df, trust_df]):
                            warn_no_public_data_upload(st)
                        else:
                            diagnostics_df = public_upload_diagnostics(
                                wgi_df=wgi_df,
                                population_df=pop_df,
                                vdem_df=vdem_df,
                                trust_df=trust_df,
                            )
                            st.session_state["empirical_ingest_diagnostics"] = diagnostics_df.copy()
                            master_df = build_master_from_public_uploads(wgi_df=wgi_df, population_df=pop_df, vdem_df=vdem_df, trust_df=trust_df)
                            demo_names = {"Exampleland", "Threshold Republic", "Capture State"}
                            if "country" in master_df.columns and set(master_df["country"].astype(str).head(10)) & demo_names:
                                raise ValueError(
                                    "Builder produced synthetic demo rows after a real upload. This is blocked so uploaded data is not mistaken for evidence."
                                )
                            st.session_state["empirical_master_df"] = master_df.copy()
                            st.session_state["use_generated_master_for_scoring"] = True
                            valid_rows = int(master_df.get("empirical_identity_valid", pd.Series([True] * len(master_df))).fillna(False).astype(bool).sum()) if not master_df.empty else 0
                    if not all(x is None for x in [wgi_df, pop_df, vdem_df, trust_df]):
                        st.success(f"Upload processed: built a country-year table with {len(master_df):,} row(s); {valid_rows:,} valid identity row(s).")
                except Exception as exc:
                    st.session_state.pop("empirical_master_df", None)
                    render_upload_processing_failed(st, exc)
                    if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                        st.markdown("#### Upload check details")
                        st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)

            if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                with st.expander("Upload check details", expanded=build_master):
                    st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
                    st.caption(
                        "raw_rows_read = rows actually read from the uploaded file; "
                        "standardized_country_year_rows = rows ALETHEIA could map to country/iso3/year; "
                        "rows_with_signal = rows carrying WGI, population, V-Dem, or trust values. "
                        "Individual source files may show 0 valid country-year rows before merge if they do not contain "
                        "the full identity/population basis. The merged master is the source of truth for scoring. "
                        "The generated/scored master uses the default modern empirical window, year >= 1996."
                    )

        def _empirical_source_status_frame(df: pd.DataFrame | None) -> pd.DataFrame:
            wgi_cols = [
                "wgi_voice_accountability",
                "wgi_political_stability",
                "wgi_government_effectiveness",
                "wgi_regulatory_quality",
                "wgi_rule_of_law",
                "wgi_control_corruption",
            ]
            vdem_cols = ["vdem_executive_constraints", "vdem_democracy", "v2x_polyarchy", "v2x_libdem"]
            trust_raw_cols = ["wvs_generalized_trust"]
            trust_prior_cols = ["empirical_trust_prior"]

            def _count_present(cols: list[str]) -> tuple[int, int, str, str]:
                if not isinstance(df, pd.DataFrame) or df.empty:
                    return 0, 0, "No active table", "missing"
                existing = [c for c in cols if c in df.columns]
                if not existing:
                    return 0, len(df), "Columns absent", "missing"
                mask = pd.Series(False, index=df.index)
                for col in existing:
                    mask = mask | pd.to_numeric(df[col], errors="coerce").notna()
                present = int(mask.sum())
                missing = int((~mask).sum())
                if present > 0:
                    status = "active"
                elif existing:
                    status = "columns present; no usable values"
                else:
                    status = "missing"
                return present, missing, ", ".join(existing), status

            rows = []
            for label, cols in [
                ("WGI", wgi_cols),
                ("V-Dem", vdem_cols),
                ("Trust raw survey", trust_raw_cols),
            ]:
                present, missing, detail, status = _count_present(cols)
                rows.append({
                    "Source": label,
                    "Rows with usable values": present,
                    "Rows missing / neutral fallback": missing,
                    "Status": status,
                    "Detected columns": detail,
                })

            # Patch 72.13: `empirical_trust_prior` is a derived/scoring field, not a
            # required upload source. Direct merged-upload diagnostics should not
            # report it as a missing source error when raw trust is active.
            prior_present, prior_missing, prior_detail, prior_status = _count_present(trust_prior_cols)
            if prior_detail == "Columns absent":
                prior_status = "computed after scoring"
                prior_detail = "Not an upload requirement; derived during scoring from raw trust or neutral fallback."
                prior_missing = 0
            else:
                prior_status = "derived field active" if prior_present > 0 else "derived field present; no usable values yet"
            rows.append({
                "Source": "Trust prior (derived)",
                "Rows with usable values": prior_present,
                "Rows missing / neutral fallback": prior_missing,
                "Status": prior_status,
                "Detected columns": prior_detail,
            })
            return pd.DataFrame(rows)

        def _is_aletheia_scored_master(df: pd.DataFrame | None) -> bool:
            if not isinstance(df, pd.DataFrame) or df.empty:
                return False
            required = {
                "country", "iso3", "year", "population",
                "aletheia_empirical_integrity",
                "aletheia_empirical_friction",
                "aletheia_empirical_collapse_probability",
                "aletheia_verdict",
            }
            cols = {str(c).strip().lower().replace(" ", "_") for c in df.columns}
            return required.issubset(cols)

        uploaded_empirical_override = None
        if isinstance(st.session_state.get("empirical_master_df"), pd.DataFrame):
            master_df = st.session_state["empirical_master_df"]
            with st.expander("Data carry-through check", expanded=False):
                st.dataframe(_empirical_source_status_frame(master_df), use_container_width=True, hide_index=True)
                st.caption("This checks the table before scoring. If WGI is missing here, World Lens cannot report WGI coverage. Rebuild with the WGI file in the WGI slot.")
            st.markdown("#### Generated country-year table")
            st.caption("This table merges WGI, population, and optional V-Dem/trust data. V-Dem rows before 1996 are filtered out by default.")
            st.dataframe(master_df.head(250), use_container_width=True, hide_index=True, height=260)
            st.download_button(
                "⬇️ Download generated country-year master CSV",
                data=master_df.to_csv(index=False),
                file_name="aletheia_country_year_master.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_generated_country_year_master_csv",
            )
            st.caption("Downloading this master CSV does not rebuild the four source uploads; it exports the active generated table held in session state.")
            if "use_generated_master_for_scoring" not in st.session_state:
                st.session_state["use_generated_master_for_scoring"] = True

            if st.checkbox("Use this table for scoring", key="use_generated_master_for_scoring"):
                uploaded_empirical_override = master_df.copy()

        st.markdown("### Score evidence table")
        template_df = empirical_template()
        st.download_button(
            "⬇️ Download empirical CSV template",
            data=template_df.to_csv(index=False),
            file_name="aletheia_empirical_country_year_template.csv",
            mime="text/csv",
            use_container_width=True,
        )

        uploaded_empirical = st.file_uploader(
            "Upload merged evidence / country-year CSV",
            type=["csv"],
            key="empirical_merged_upload",
            help="Use this for a complete already-merged ALETHEIA master CSV or a previously exported ALETHEIA scored master. Do not upload V-Dem-only or trust-only enrichment files here; use their optional slots above.",
        )

        direct_upload_df = None
        direct_upload_is_scored_master = False
        if uploaded_empirical is not None:
            try:
                direct_upload_df = pd.read_csv(uploaded_empirical)
                st.session_state["direct_empirical_upload_df"] = direct_upload_df.copy()
                direct_upload_is_scored_master = _is_aletheia_scored_master(direct_upload_df)
                with st.expander("Direct merged-upload diagnostics", expanded=True):
                    st.dataframe(_empirical_source_status_frame(direct_upload_df), use_container_width=True, hide_index=True)
                    if direct_upload_is_scored_master:
                        st.success(
                            "This file looks like an ALETHEIA scored master/export. Existing ALETHEIA scores, verdicts, "
                            "trust priors, and source columns will be preserved for the active empirical table."
                        )
                    else:
                        st.info(
                            "This file looks like an unscored merged evidence table. ALETHEIA will score it after variable mapping. "
                            "Raw trust is read from `wvs_generalized_trust` when available. Trust prior is derived during scoring, "
                            "so it is not a required upload column. If a true source column is present but has no usable values, "
                            "Grid coverage for that source will correctly remain 0%."
                        )
            except Exception as exc:
                render_direct_csv_read_failed(st, exc)
                direct_upload_df = None

        use_template = st.checkbox(
            "Use built-in synthetic demo template instead of uploaded/generated data",
            value=(uploaded_empirical is None and uploaded_empirical_override is None),
            help="The demo rows are not real countries. They only demonstrate the schema and output flow.",
        )

        st.session_state["empirical_use_template"] = bool(use_template)
        update_protocol_state(last_update_source="Evidence Lab", synthetic_demo_active=bool(use_template))

        if use_template:
            st.warning(
                "Synthetic demo mode is active. Exampleland, Threshold Republic, and Capture State are interface-test rows only; "
                "do not interpret their correlations, scores, or 9k allocation as real-world findings."
            )

        empirical_raw = None
        active_direct_scored_master = False
        if uploaded_empirical_override is not None and not use_template:
            empirical_raw = uploaded_empirical_override.copy()
        elif direct_upload_df is not None and not use_template:
            empirical_raw = direct_upload_df.copy()
            active_direct_scored_master = bool(direct_upload_is_scored_master)
        else:
            empirical_raw = template_df.copy()

        def _empirical_active_input_signature(
            df: pd.DataFrame | None,
            *,
            source_label: str,
            use_template_flag: bool,
            active_direct_scored_master_flag: bool,
        ) -> str:
            """Stable Evidence Lab signature for active input tables.

            Patch 72.9: widgets and downloads rerun Streamlit, but they should not
            re-score the same active master. This signature changes when the active
            source table, source type, or scored-master mode changes.
            """
            hasher = hashlib.sha256()
            hasher.update(str(source_label).encode("utf-8"))
            hasher.update(str(bool(use_template_flag)).encode("utf-8"))
            hasher.update(str(bool(active_direct_scored_master_flag)).encode("utf-8"))
            if not isinstance(df, pd.DataFrame):
                hasher.update(b"<none>")
                return hasher.hexdigest()
            hasher.update(str(df.shape).encode("utf-8"))
            hasher.update("|".join(map(str, df.columns)).encode("utf-8"))
            try:
                content_hash = pd.util.hash_pandas_object(df.reset_index(drop=True), index=True).values
                hasher.update(content_hash.tobytes())
            except Exception:
                hasher.update(df.to_csv(index=False).encode("utf-8", errors="replace"))
            return hasher.hexdigest()

        if empirical_raw is not None:
            if use_template:
                source_label = "synthetic demo template"
            elif uploaded_empirical_override is not None:
                source_label = "generated master table"
            elif active_direct_scored_master:
                source_label = "uploaded ALETHEIA scored master"
            else:
                source_label = "uploaded merged evidence CSV"

            empirical_active_signature = _empirical_active_input_signature(
                empirical_raw,
                source_label=source_label,
                use_template_flag=bool(use_template),
                active_direct_scored_master_flag=bool(active_direct_scored_master),
            )
            cached_signature = st.session_state.get("empirical_active_scoring_signature")
            cached_prepared = st.session_state.get("empirical_active_prepared_df")
            cached_scored_all = st.session_state.get("empirical_active_scored_all_df")
            if (
                cached_signature == empirical_active_signature
                and isinstance(cached_prepared, pd.DataFrame)
                and isinstance(cached_scored_all, pd.DataFrame)
            ):
                prepared = cached_prepared.copy().reset_index(drop=True)
                scored_all = cached_scored_all.copy().reset_index(drop=True)
                st.caption(
                    "Using the active Evidence Lab scored table from session state. "
                    "Country/year selection and downloads do not rebuild or rescore the uploaded master."
                )
            else:
                with st.spinner(f"Processing {source_label} through ALETHEIA variable mapping and Sydney Protocol overlay..."):
                    prepared = prepare_empirical_frame(empirical_raw).reset_index(drop=True)
                    if active_direct_scored_master:
                        # A previously exported ALETHEIA master should be accepted as an
                        # already-scored protocol state rather than neutralized by a second
                        # scoring pass when raw source columns are sparse. Identity and
                        # modern-year guards still apply below.
                        scored_all = prepared.copy().reset_index(drop=True)
                        for _score_col in [
                            "aletheia_empirical_integrity",
                            "aletheia_empirical_friction",
                            "aletheia_empirical_collapse_probability",
                            "empirical_completeness",
                            "empirical_trust_prior",
                        ]:
                            if _score_col in scored_all.columns:
                                scored_all[_score_col] = pd.to_numeric(scored_all[_score_col], errors="coerce")
                        if "evidence_variables_used" not in scored_all.columns and "evidence_used" in scored_all.columns:
                            scored_all["evidence_variables_used"] = scored_all["evidence_used"]
                        if "evidence_used" not in scored_all.columns and "evidence_variables_used" in scored_all.columns:
                            scored_all["evidence_used"] = scored_all["evidence_variables_used"]
                        if "protocol_overlay_status" not in scored_all.columns:
                            scored_all["protocol_overlay_status"] = "preserved uploaded scored master"
                        if "final_audit_interpretation" not in scored_all.columns:
                            scored_all["final_audit_interpretation"] = scored_all.get("aletheia_verdict", pd.Series([""] * len(scored_all))).astype(str)
                    else:
                        scored_all = score_empirical_frame(prepared).reset_index(drop=True)
                st.session_state["empirical_active_scoring_signature"] = empirical_active_signature
                st.session_state["empirical_active_prepared_df"] = prepared.copy()
                st.session_state["empirical_active_scored_all_df"] = scored_all.copy()

            if active_direct_scored_master and not scored_all.empty:
                _direct_identity = scored_all.get("empirical_identity_valid", pd.Series([False] * len(scored_all)))
                _direct_identity = _direct_identity.fillna(False).astype(bool) if hasattr(_direct_identity, "fillna") else pd.Series([False] * len(scored_all))
                _direct_year = pd.to_numeric(scored_all.get("year"), errors="coerce")
                _direct_modern = _direct_year.ge(1996)
                _before_direct_filter = len(scored_all)
                scored_all = scored_all.loc[_direct_identity & _direct_modern].copy().reset_index(drop=True)
                _removed_direct = _before_direct_filter - len(scored_all)
                if _removed_direct > 0:
                    st.info(f"Direct scored table guard removed {_removed_direct:,} row(s) outside valid identity or modern-year scope.")

            # Fail closed for real uploads/generated masters. Diagnostic rows are useful
            # for ingestion debugging, but they must never be reported as scored
            # empirical evidence. A valid empirical row requires country, iso3, year,
            # and positive population.
            if not use_template:
                if scored_all.empty:
                    st.error("No valid country-year rows are available for scoring.")
                    st.warning(
                        "The upload/generated master produced only diagnostic rows or no rows at all. "
                        "ALETHEIA blocked scoring instead of reporting diagnostic rows as evidence. "
                        "Check WGI pivoting, country/iso3/year fields, and population merge."
                    )
                    if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                        st.markdown("#### Upload check details")
                        st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
                    st.stop()

                _identity_series = scored_all.get("empirical_identity_valid", pd.Series([False] * len(scored_all)))
                _identity_series = _identity_series.fillna(False).astype(bool) if hasattr(_identity_series, "fillna") else pd.Series([False] * len(scored_all))
                _valid_rows = int(_identity_series.sum())
                _diagnostic_rows = int((~_identity_series).sum())
                if _valid_rows == 0:
                    st.error("No valid country-year rows are available for scoring.")
                    st.warning(
                        f"{_diagnostic_rows:,} diagnostic row(s) were produced, but all are missing country, iso3, year, "
                        "or positive population. Scoring and 9k allocation are blocked until at least one valid "
                        "country-year row exists."
                    )
                    if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                        st.markdown("#### Upload check details")
                        st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
                    st.stop()

            st.success(f"Evidence scoring complete: {len(scored_all):,} valid row(s) mapped and scored from {source_label}.")

            # Keep the active empirical input columns attached to the scored output.
            # The scoring helper intentionally returns a compact audit table, but the
            # UI, validation checks, downloads, and technical detail sections need the
            # original public evidence columns too.  Attaching them here prevents lower
            # sections from falling back to the synthetic demo view or losing WGI data.
            if len(scored_all) == len(prepared):
                passthrough_cols = [
                    "wgi_voice_accountability",
                    "wgi_political_stability",
                    "wgi_government_effectiveness",
                    "wgi_regulatory_quality",
                    "wgi_rule_of_law",
                    "wgi_control_corruption",
                    "vdem_executive_constraints",
                    "vdem_democracy",
                    "wvs_generalized_trust",
                    "conflict_events",
                    "political_violence_events",
                    "coup_attempt",
                    "regime_breakdown",
                    "civil_unrest_index",
                    "forced_displacement_rate",
                    "future_stability_decline",
                ]
                for _col in passthrough_cols:
                    if _col in prepared.columns and _col not in scored_all.columns:
                        scored_all[_col] = prepared[_col].values

            # Recompute 9k seats from the full valid country population base, not
            # from the WGI-filtered evidence subset and not from World Bank regional
            # aggregates.  The scored table keeps diagnostic rows, but only valid
            # country rows receive seats.
            allocation_base_all = _country_allocation_base(scored_all, include_demo=use_template)
            if not use_template:
                scored_all = _replace_allocation_columns(scored_all, allocation_base_all)
            else:
                allocation_base_all = scored_all.copy()

            identity_valid_series = scored_all.get("empirical_identity_valid", pd.Series([True] * len(scored_all)))
            identity_valid_series = identity_valid_series.fillna(False).astype(bool) if hasattr(identity_valid_series, "fillna") else pd.Series([True] * len(scored_all))
            invalid_count = int((~identity_valid_series).sum()) if not scored_all.empty else 0
            valid_identity_count = int(identity_valid_series.sum()) if not scored_all.empty else 0

            if invalid_count and not use_template:
                st.warning(
                    f"{valid_identity_count:,} valid country-year row(s) and {invalid_count:,} diagnostic row(s). "
                    "Diagnostic rows are retained because they are missing country, iso3, year, or positive population; "
                    "they are excluded from valid 9k allocation."
                )
            elif not use_template and not scored_all.empty:
                st.success(f"{valid_identity_count:,} valid country-year row(s) are ready for scoring and 9k allocation.")

            scored = scored_all.copy()
            if not use_template and not scored.empty:
                _wgi_cols_check = [
                    "wgi_voice_accountability",
                    "wgi_political_stability",
                    "wgi_government_effectiveness",
                    "wgi_regulatory_quality",
                    "wgi_rule_of_law",
                    "wgi_control_corruption",
                ]
                _wgi_present_cols = [c for c in _wgi_cols_check if c in scored.columns]
                _wgi_rows_present = 0
                if _wgi_present_cols:
                    _wgi_mask = pd.Series(False, index=scored.index)
                    for _col in _wgi_present_cols:
                        _wgi_mask = _wgi_mask | pd.to_numeric(scored[_col], errors="coerce").notna()
                    _wgi_rows_present = int(_wgi_mask.sum())
                if _wgi_rows_present == 0:
                    st.warning(
                        "WGI source signal is not present in the active scored evidence table. "
                        "The Global Grid will correctly show WGI coverage as 0.0% until the master is rebuilt with a WGI file in the WGI upload slot or a merged CSV containing WGI columns."
                    )

            if not use_template and not scored.empty:
                wgi_signal_cols = [
                    "wgi_voice_accountability",
                    "wgi_political_stability",
                    "wgi_government_effectiveness",
                    "wgi_regulatory_quality",
                    "wgi_rule_of_law",
                    "wgi_control_corruption",
                ]
                available_signal_cols = [c for c in wgi_signal_cols if c in scored.columns]
                if available_signal_cols:
                    evidence_mask = pd.Series(False, index=scored.index)
                    for col in available_signal_cols:
                        evidence_mask = evidence_mask | pd.to_numeric(scored[col], errors="coerce").notna()
                    if int(evidence_mask.sum()) > 0 and int(evidence_mask.sum()) < len(scored):
                        show_evidence_years_only = st.checkbox(
                            "Show WGI-supported evidence years only",
                            value=True,
                            help="Recommended for first real runs. Population-only historical rows are useful for allocation context but should not drive governance scoring summaries.",
                        )
                        if show_evidence_years_only:
                            scored = scored.loc[evidence_mask].copy()
                        st.caption(
                            f"Evidence-year filter: showing {len(scored):,} of {len(scored_all):,} rows. "
                            f"{int(evidence_mask.sum()):,} row(s) contain at least one WGI governance indicator."
                        )

            st.session_state["empirical_scored_df"] = scored.copy()
            st.session_state["empirical_allocation_df"] = allocation_base_all.copy()
            update_protocol_state(last_update_source="Evidence Lab", synthetic_demo_active=bool(use_template))

            if not use_template and not scored.empty:
                demo_names = {"Exampleland", "Threshold Republic", "Capture State"}
                visible_names = set(scored.get("country", pd.Series(dtype=str)).astype(str).head(25).tolist())
                if visible_names & demo_names:
                    st.warning("Uploaded-evidence mode is active, but demo country names are still present in the active scored data. Clear the uploaded file or reload the app if this was not intended.")

            # Validation should use the exact active dataframe visible on the page,
            # including uploaded/generated evidence columns.  This keeps N and group
            # means aligned with the real uploaded evidence instead of the demo rows.
            scored_for_validation = scored.reset_index(drop=True).copy()

            st.markdown("### Topline Evidence Results" + (" · Synthetic demo" if use_template else " · Uploaded evidence"))
            if use_template:
                st.caption("Synthetic rows are for app testing only. Do not read them as real-world findings.")
            else:
                st.caption("Uploaded/generated data was mapped, scored, and shown through the protocol view.")

            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Rows scored", f"{len(scored):,}")

            seat_year_label = "Synthetic 9k seats" if use_template else "Latest-year 9k seats"
            seat_year_value = "—"
            seat_caption = ""
            seat_df = allocation_base_all.copy()
            if not seat_df.empty and "year" in seat_df.columns and "seats_9k" in seat_df.columns:
                year_values = pd.to_numeric(seat_df["year"], errors="coerce")
                if year_values.notna().any():
                    latest_year = int(year_values.dropna().max())
                    seat_year_label = "Synthetic 9k seats" if use_template else f"9k seats · {latest_year}"
                    latest_year_mask = year_values == latest_year
                    latest_year_seats = int(pd.to_numeric(seat_df.loc[latest_year_mask, "seats_9k"], errors="coerce").sum(skipna=True))
                    seat_year_value = f"{latest_year_seats:,}"
                    if not use_template:
                        all_year_seats = int(pd.to_numeric(seat_df["seats_9k"], errors="coerce").sum(skipna=True))
                        seat_caption = f"All row-year seat total: {all_year_seats:,}; 9k allocation is interpreted per year."
            e2.metric(seat_year_label, seat_year_value)
            e3.metric("Mean integrity", f"{pd.to_numeric(scored['aletheia_empirical_integrity'], errors='coerce').mean():.3f}")
            e4.metric("Average schema coverage" if use_template else "Average empirical coverage", f"{pd.to_numeric(scored['empirical_completeness'], errors='coerce').mean():.1%}")
            if seat_caption:
                st.caption(seat_caption)
            if use_template:
                st.caption("Demo schema coverage is below 100% because capital_scale is intentionally blank; optional proxies should not be treated as empirically supplied.")

            with st.expander("Main scored data table", expanded=False):
                st.markdown("### Main scored data table")
                st.caption("capital_scale is neutral/default unless supplied through an empirical proxy column; schema coverage is not proof of empirical validity." if use_template else "capital_scale is neutral/default unless supplied through an empirical proxy column.")
                curated_cols = [
                    "country", "iso3", "year", "population", "seats_9k",
                    "aletheia_verdict", "aletheia_empirical_integrity", "aletheia_empirical_friction",
                    "aletheia_empirical_collapse_probability",
                    "empirical_completeness", "empirical_identity_valid",
                ]
                curated_cols = [c for c in curated_cols if c in scored.columns]
                display_names = {
                    "aletheia_verdict": "verdict",
                    "aletheia_empirical_integrity": "integrity",
                    "aletheia_empirical_friction": "friction",
                    "aletheia_empirical_collapse_probability": "collapse_probability",
                    "empirical_completeness": "schema_coverage" if use_template else "empirical_coverage",
                    "empirical_identity_valid": "identity_valid",
                }
                curated_display = scored[curated_cols].rename(columns=display_names)
                st.dataframe(curated_display, use_container_width=True, hide_index=True, height=260)

                csv_out = scored.to_csv(index=False)
                st.download_button(
                    "⬇️ Download scored empirical ALETHEIA table",
                    data=csv_out,
                    file_name="aletheia_evidence_audit_scores.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            st.markdown("### Country-Year Explorer")
            valid_rows = scored.reset_index(drop=True).copy()

            def _truthy_series(series: pd.Series) -> pd.Series:
                if series is None:
                    return pd.Series(True, index=valid_rows.index)
                if series.dtype == bool:
                    return series.fillna(False)
                text = series.astype(str).str.strip().str.lower()
                return text.isin(["true", "1", "yes", "y", "valid"])

            if "empirical_identity_valid" in valid_rows.columns:
                identity_mask = _truthy_series(valid_rows["empirical_identity_valid"])
            elif "identity_valid" in valid_rows.columns:
                identity_mask = _truthy_series(valid_rows["identity_valid"])
            else:
                identity_mask = pd.Series(True, index=valid_rows.index)

            required_explorer_cols = ["country", "iso3", "year"]
            missing_explorer_cols = [c for c in required_explorer_cols if c not in valid_rows.columns]
            if missing_explorer_cols:
                st.warning(
                    "Country-Year Explorer is inactive because the active scored table is missing required column(s): "
                    + ", ".join(missing_explorer_cols)
                    + ". Upload or rebuild a country-year master with country, iso3, and year."
                )
            else:
                valid_rows = valid_rows.loc[identity_mask].copy()
                valid_rows["_country_label"] = valid_rows["country"].astype(str).str.strip()
                valid_rows["_iso3_label"] = valid_rows["iso3"].astype(str).str.strip().str.upper()
                valid_rows["_year_num"] = pd.to_numeric(valid_rows["year"], errors="coerce")
                valid_rows = valid_rows[
                    valid_rows["_country_label"].ne("")
                    & valid_rows["_iso3_label"].ne("")
                    & valid_rows["_year_num"].notna()
                ].copy()

                if valid_rows.empty:
                    st.info("No valid country-year rows yet. Add country, ISO3, year, and population so you can inspect one row at a time." )
                else:
                    valid_rows["_year_int"] = valid_rows["_year_num"].astype(int)

                    def _friendly_country_name(iso3_value: str, country_value: str = "") -> str:
                        iso3_text = str(iso3_value or "").strip().upper()
                        country_text = str(country_value or "").strip()
                        if country_text and country_text.upper() != iso3_text and len(country_text) > 3:
                            return country_text
                        manual_names = {
                            "AFG": "Afghanistan", "ALB": "Albania", "DZA": "Algeria", "AGO": "Angola", "ARG": "Argentina",
                            "ARM": "Armenia", "AUS": "Australia", "AUT": "Austria", "AZE": "Azerbaijan", "BHR": "Bahrain",
                            "BGD": "Bangladesh", "BLR": "Belarus", "BEL": "Belgium", "BEN": "Benin", "BOL": "Bolivia",
                            "BIH": "Bosnia and Herzegovina", "BWA": "Botswana", "BRA": "Brazil", "BGR": "Bulgaria",
                            "BFA": "Burkina Faso", "BDI": "Burundi", "KHM": "Cambodia", "CMR": "Cameroon", "CAN": "Canada",
                            "CAF": "Central African Republic", "TCD": "Chad", "CHL": "Chile", "CHN": "China", "COL": "Colombia",
                            "COD": "Democratic Republic of the Congo", "COG": "Republic of the Congo", "CRI": "Costa Rica",
                            "CIV": "Côte d’Ivoire", "HRV": "Croatia", "CUB": "Cuba", "CYP": "Cyprus", "CZE": "Czechia",
                            "DNK": "Denmark", "DOM": "Dominican Republic", "ECU": "Ecuador", "EGY": "Egypt", "SLV": "El Salvador",
                            "ERI": "Eritrea", "EST": "Estonia", "ETH": "Ethiopia", "FIN": "Finland", "FRA": "France",
                            "GAB": "Gabon", "GEO": "Georgia", "DEU": "Germany", "GHA": "Ghana", "GRC": "Greece",
                            "GTM": "Guatemala", "GIN": "Guinea", "HTI": "Haiti", "HND": "Honduras", "HUN": "Hungary",
                            "IND": "India", "IDN": "Indonesia", "IRN": "Iran", "IRQ": "Iraq", "IRL": "Ireland",
                            "ISR": "Israel", "ITA": "Italy", "JPN": "Japan", "JOR": "Jordan", "KAZ": "Kazakhstan",
                            "KEN": "Kenya", "KWT": "Kuwait", "KGZ": "Kyrgyzstan", "LAO": "Laos", "LVA": "Latvia",
                            "LBN": "Lebanon", "LBR": "Liberia", "LBY": "Libya", "LTU": "Lithuania", "MDG": "Madagascar",
                            "MWI": "Malawi", "MYS": "Malaysia", "MLI": "Mali", "MEX": "Mexico", "MDA": "Moldova",
                            "MAR": "Morocco", "MOZ": "Mozambique", "MMR": "Myanmar", "NAM": "Namibia", "NPL": "Nepal",
                            "NLD": "Netherlands", "NZL": "New Zealand", "NIC": "Nicaragua", "NER": "Niger", "NGA": "Nigeria",
                            "PRK": "North Korea", "MKD": "North Macedonia", "NOR": "Norway", "OMN": "Oman", "PAK": "Pakistan",
                            "PAN": "Panama", "PRY": "Paraguay", "PER": "Peru", "PHL": "Philippines", "POL": "Poland",
                            "PRT": "Portugal", "QAT": "Qatar", "ROU": "Romania", "RUS": "Russia", "RWA": "Rwanda",
                            "SAU": "Saudi Arabia", "SEN": "Senegal", "SRB": "Serbia", "SLE": "Sierra Leone", "SGP": "Singapore",
                            "SVK": "Slovakia", "SVN": "Slovenia", "SOM": "Somalia", "ZAF": "South Africa", "KOR": "South Korea",
                            "SSD": "South Sudan", "ESP": "Spain", "LKA": "Sri Lanka", "SDN": "Sudan", "SWE": "Sweden",
                            "CHE": "Switzerland", "SYR": "Syria", "TWN": "Taiwan", "TJK": "Tajikistan", "TZA": "Tanzania",
                            "THA": "Thailand", "TUN": "Tunisia", "TUR": "Türkiye", "TKM": "Turkmenistan", "UGA": "Uganda",
                            "UKR": "Ukraine", "ARE": "United Arab Emirates", "GBR": "United Kingdom", "USA": "United States",
                            "URY": "Uruguay", "UZB": "Uzbekistan", "VEN": "Venezuela", "VNM": "Vietnam", "YEM": "Yemen",
                            "ZMB": "Zambia", "ZWE": "Zimbabwe",
                        }
                        return manual_names.get(iso3_text, country_text or iso3_text)

                    valid_rows["_country_name"] = [
                        _friendly_country_name(iso3, country)
                        for iso3, country in zip(valid_rows["_iso3_label"], valid_rows["_country_label"])
                    ]
                    valid_rows = valid_rows.sort_values(["_year_int", "_country_name"], ascending=[False, True]).reset_index(drop=True)

                    years_available = sorted(valid_rows["_year_int"].dropna().astype(int).unique().tolist(), reverse=True)
                    if years_available:
                        max_explorer_year = max(years_available)
                        min_explorer_year = min(years_available)
                        if max_explorer_year < 2020:
                            st.warning(
                                f"The active scored table currently only goes up to {max_explorer_year}. "
                                "The explorer can only show years that exist in this Empirical run. "
                                "If you expected newer years, reload or rebuild the full country-year master before using this explorer."
                            )

                        # Country-first selection keeps the list readable and gives native
                        # type-ahead suggestions from the available countries.
                        country_lookup = (
                            valid_rows[["_country_name", "_iso3_label"]]
                            .drop_duplicates()
                            .sort_values(["_country_name", "_iso3_label"])
                            .reset_index(drop=True)
                        )
                        country_lookup["_country_option"] = country_lookup["_country_name"] + " · " + country_lookup["_iso3_label"]
                        country_options = country_lookup["_country_option"].tolist()

                        synced_iso3 = st.session_state.get("aletheia_synced_iso3")
                        synced_country_option = None
                        if synced_iso3:
                            _synced_options = country_lookup.loc[
                                country_lookup["_iso3_label"].astype(str).str.upper() == str(synced_iso3).upper(),
                                "_country_option",
                            ].tolist()
                            synced_country_option = _synced_options[0] if _synced_options else None

                        country_widget_key = "empirical_country_year_explorer_country_search"
                        # Only seed the country selector before the widget exists.
                        # Do not overwrite an existing widget value from a user click,
                        # otherwise a stale focus country can force the selector back
                        # to the previous/default country such as Afghanistan.
                        if country_widget_key not in st.session_state and synced_country_option in country_options:
                            st.session_state[country_widget_key] = synced_country_option

                        country_col, year_col = st.columns([2, 1])
                        with country_col:
                            selected_country_option = st.selectbox(
                                "Search country",
                                options=country_options,
                                index=country_options.index(st.session_state.get(country_widget_key, country_options[0])) if st.session_state.get(country_widget_key, country_options[0]) in country_options else 0,
                                key=country_widget_key,
                                help="Start typing a country name or ISO code. The list only includes countries available in the active scored table.",
                            )
                        selected_iso = country_lookup.loc[
                            country_lookup["_country_option"] == selected_country_option, "_iso3_label"
                        ].iloc[0]
                        selected_country_name = country_lookup.loc[
                            country_lookup["_country_option"] == selected_country_option, "_country_name"
                        ].iloc[0]
                        st.session_state["aletheia_synced_iso3"] = str(selected_iso).upper()
                        st.session_state["aletheia_synced_country_name"] = str(selected_country_name)
                        st.caption(f"Focus country set for Grid/report context: {selected_country_name} · {str(selected_iso).upper()}")

                        country_rows_all_years = valid_rows[valid_rows["_iso3_label"] == selected_iso].copy()
                        country_years = country_available_years(valid_rows, selected_iso)

                        st.caption(
                            country_year_status_message(selected_country_name, selected_iso, country_years)
                            + " The year dropdown is scoped to this selected country only; ALETHEIA does not silently fall back to a global/default year."
                        )
                        if not country_years:
                            st.warning(
                                f"No available country-year data for {selected_country_name} · {str(selected_iso).upper()}. "
                                "Choose another country or rebuild the country-year master."
                            )
                            st.stop()

                        synced_evidence_year = st.session_state.get("aletheia_synced_evidence_year")
                        country_year_widget_key = f"empirical_country_year_explorer_year_{selected_iso}"
                        # Patch 72.13: a synced Grid/World Lens year may seed the widget
                        # once, but must not overwrite a user's manual year choice on
                        # every Streamlit rerun. This keeps the dropdown from snapping
                        # back to 2024 after the user selects another available year.
                        if country_year_widget_key not in st.session_state and synced_evidence_year in country_years:
                            st.session_state[country_year_widget_key] = int(synced_evidence_year)
                        country_year_index = safe_country_year_index(st.session_state.get(country_year_widget_key), country_years)
                        with year_col:
                            selected_explorer_year = st.selectbox(
                                "Year for country",
                                options=country_years,
                                index=country_year_index,
                                key=country_year_widget_key,
                                help="Only years present for the selected country are shown. No global/default fallback is used.",
                            )
                        st.session_state["aletheia_synced_evidence_year"] = int(selected_explorer_year)
                        st.session_state["aletheia_empirical_country_year"] = int(selected_explorer_year)

                        explorer_rows = country_rows_all_years[country_rows_all_years["_year_int"] == int(selected_explorer_year)].copy()

                        if explorer_rows.empty:
                            st.info("No country-year row matches that country and year. Try another country or year.")
                            st.stop()

                        explorer_rows["_label"] = explorer_rows["_country_name"] + " · " + explorer_rows["_iso3_label"] + " · " + explorer_rows["_year_int"].astype(str)
                        if "seats_9k" in explorer_rows.columns:
                            _seat_nums = pd.to_numeric(explorer_rows["seats_9k"], errors="coerce")
                            explorer_rows.loc[_seat_nums.notna(), "_label"] = (
                                explorer_rows.loc[_seat_nums.notna(), "_label"]
                                + " · "
                                + _seat_nums[_seat_nums.notna()].astype(int).astype(str)
                                + " seats"
                            )

                        st.caption(
                            "Explorer source: active scored table. Search country first, then choose one of that country’s available years. "
                            "This avoids stale global-year fallback and shares the confirmed year with allocation and Grid outputs when available."
                        )

                        if len(explorer_rows) == 1:
                            selected = explorer_rows.iloc[0]
                        else:
                            options = explorer_rows.index.tolist()
                            selected_idx = st.selectbox(
                                "Country-year row",
                                options=options,
                                format_func=lambda idx: explorer_rows.loc[idx, "_label"],
                                key="empirical_country_year_explorer_country_year_row",
                            )
                            selected = explorer_rows.loc[selected_idx]

                        selected_explorer_signature = (
                            f"{str(selected.get('iso3', selected_iso)).upper()}::"
                            f"{int(selected_explorer_year)}::"
                            f"{str(selected.get('country', selected_country_name))}"
                        )
                        pending_label = f"{selected_country_name} · {str(selected_iso).upper()} · {int(selected_explorer_year)}"
                        active_signature = st.session_state.get("empirical_country_year_explorer_active_signature")
                        active_selected = active_signature == selected_explorer_signature

                        run_cols = st.columns([1, 2])
                        with run_cols[0]:
                            run_country_diagnostic = st.button(
                                "Run country-year review",
                                key="empirical_country_year_explorer_run_button",
                                type="primary",
                                use_container_width=True,
                            )
                        with run_cols[1]:
                            if active_selected:
                                st.success(f"Diagnostic is active for: {pending_label}")
                            else:
                                st.info(
                                    f"Selected: {pending_label}. Press **Run country-year review** to update the cards and raw-row detail."
                                )

                        if run_country_diagnostic:
                            st.session_state["empirical_country_year_explorer_active_signature"] = selected_explorer_signature
                            st.session_state["empirical_country_year_explorer_active_payload"] = selected.to_dict()
                            active_selected = True

                        if active_selected:
                            active_payload = st.session_state.get("empirical_country_year_explorer_active_payload")
                            if isinstance(active_payload, dict):
                                selected = pd.Series(active_payload)
                        else:
                            selected = None
                    else:
                        st.info("No valid years are available in the active scored table.")
                        st.stop()

                    if selected is not None:
                        def _first_value(row, names, default="—"):
                            for name in names:
                                if name in row.index:
                                    value = row.get(name)
                                    if pd.notna(value):
                                        return value
                            return default

                        def _fmt_num(value, digits=3):
                            num = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
                            return "—" if pd.isna(num) else f"{float(num):.{digits}f}"

                        verdict_value = _first_value(selected, ["aletheia_verdict", "verdict"], "—")
                        verdict_text = str(verdict_value or "—").strip().upper()
                        if verdict_text == "SANCTUARY":
                            display_verdict_value = "Low-risk internal reading"
                            display_verdict_caption = (
                                "Internal taxonomy label: SANCTUARY. This means the country-year evidence pattern is low-risk within ALETHEIA's review model; "
                                "it is not a final safety, final Sanctuary, or authority claim."
                            )
                        else:
                            display_verdict_value = verdict_value
                            display_verdict_caption = ""
                        integrity_value = _first_value(selected, ["aletheia_empirical_integrity", "integrity"], None)
                        collapse_value = _first_value(selected, ["aletheia_empirical_collapse_probability", "collapse_probability"], None)
                        coverage_value = _first_value(selected, ["empirical_completeness", "empirical_coverage", "schema_coverage"], None)
                        seats_value = pd.to_numeric(pd.Series([_first_value(selected, ["seats_9k"], None)]), errors="coerce").iloc[0]

                        col_a, col_b, col_c, col_d = st.columns(4)
                        col_a.metric("Empirical pattern", display_verdict_value)
                        if display_verdict_caption:
                            col_a.caption(display_verdict_caption)
                        col_b.metric("Integrity", _fmt_num(integrity_value))
                        col_c.metric("Collapse pressure", _fmt_num(collapse_value))
                        col_d.metric("Allocated seats", "—" if pd.isna(seats_value) else f"{int(seats_value):,}")

                        col_e, col_f, col_g, col_h = st.columns(4)
                        col_e.metric("Empirical coverage", _fmt_num(coverage_value, digits=1) if pd.to_numeric(pd.Series([coverage_value]), errors="coerce").iloc[0] > 1 else ("—" if pd.isna(pd.to_numeric(pd.Series([coverage_value]), errors="coerce").iloc[0]) else f"{pd.to_numeric(pd.Series([coverage_value]), errors='coerce').iloc[0]:.1%}"))
                        raw_trust_value = _first_value(selected, ["wvs_generalized_trust"], None)
                        trust_prior_value = _first_value(selected, ["empirical_trust_prior"], None)
                        col_f.metric("Raw trust", format_raw_trust_label(raw_trust_value))
                        col_g.metric("Trust prior used", format_trust_prior_label(trust_prior_value))
                        if format_raw_trust_label(raw_trust_value) == "not available" and format_trust_prior_label(trust_prior_value).startswith("0.500"):
                            st.caption("Raw trust is not available for this country-year; ALETHEIA is showing a neutral trust-prior fallback, not observed survey trust.")
                        col_h.metric("Identity valid", str(_first_value(selected, ["empirical_identity_valid", "identity_valid"], True)))

                        st.markdown("#### Sydney Protocol overlay")
                        overlay_status_value = str(_first_value(selected, ["protocol_overlay_status", "sydney_overlay_status"], "No overlay status available."))
                        if overlay_status_value.startswith("SANCTUARY evidence pattern"):
                            overlay_status_value = (
                                "Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails. "
                                "Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority."
                            )
                        st.write(overlay_status_value)
                        st.caption("Evidence used: " + str(_first_value(selected, ["evidence_variables_used", "evidence_used"], "—")))
                        st.caption("Country-Year Explorer uses the active scored table. Search a country, then choose one of its years. Seats are read inside that year only.")

                        feature_cols = [
                            "technical_complexity", "centralization", "anonymity", "regulation", "transparency", "capital_scale",
                            "empirical_trust_prior", "wvs_generalized_trust",
                            "wgi_voice_accountability", "wgi_political_stability", "wgi_government_effectiveness",
                            "wgi_regulatory_quality", "wgi_rule_of_law", "wgi_control_corruption",
                            "vdem_executive_constraints", "vdem_democracy",
                        ]
                        feature_rows = []
                        for col in feature_cols:
                            if col in selected.index:
                                value = pd.to_numeric(pd.Series([selected.get(col)]), errors="coerce").iloc[0]
                                feature_rows.append({"feature": col, "value": "—" if pd.isna(value) else f"{value:.3f}"})
                        feature_table = pd.DataFrame(feature_rows)
                        if not feature_table.empty:
                            st.dataframe(feature_table, use_container_width=True, hide_index=True, height=300)

                        detail_cols = [
                            "country", "iso3", "year", "population", "population_share", "seats_9k", "_allocation_role",
                            "aletheia_verdict", "verdict", "aletheia_empirical_integrity", "integrity",
                            "aletheia_empirical_friction", "friction",
                            "aletheia_empirical_collapse_probability", "collapse_probability",
                            "empirical_completeness", "empirical_coverage",
                            "evidence_variables_used", "evidence_used",
                        ]
                        detail_cols = [c for c in detail_cols if c in valid_rows.columns]
                        with st.expander("Selected country-year raw row", expanded=False):
                            st.dataframe(pd.DataFrame([selected[detail_cols].to_dict()]), use_container_width=True, hide_index=True)
            active_explorer_payload = st.session_state.get("empirical_country_year_explorer_active_payload")
            active_explorer_signature = st.session_state.get("empirical_country_year_explorer_active_signature")
            if active_explorer_signature is None or not isinstance(active_explorer_payload, dict):
                st.caption("Country-Year cards unlock after you choose a country/year and press **Run country-year review**.")

            with st.expander("Advanced evidence views — allocation, validation, and technical tables", expanded=False):
                st.markdown("### Seat allocation view")
                st.caption("Synthetic 9k allocation across demo rows." if use_template else "Country seats by selected year. Regional, income, and diagnostic rows are excluded.")

                allocation_df = allocation_base_all.dropna(subset=["seats_9k"]).copy()
                allocation_locked = active_explorer_signature is None or not isinstance(active_explorer_payload, dict)

                if allocation_locked:
                    st.info(
                        "Seat allocation view is locked to avoid stale or mismatched output. "
                        "Choose a country/year above and press **Run country-year review**. "
                        "The allocation chart will then use that confirmed diagnostic year."
                    )
                elif not allocation_df.empty:
                    selected_years = sorted(pd.to_numeric(allocation_df["year"], errors="coerce").dropna().astype(int).unique().tolist())
                    if selected_years:
                        active_allocation_year = pd.to_numeric(pd.Series([active_explorer_payload.get("year")]), errors="coerce").iloc[0]
                        if pd.isna(active_allocation_year):
                            st.warning("The active country-year diagnostic does not contain a valid year. Rerun the diagnostic.")
                        else:
                            active_allocation_year = int(active_allocation_year)
                            if active_allocation_year not in selected_years:
                                st.warning(
                                    f"Seat allocation view is locked because the confirmed diagnostic year {active_allocation_year} "
                                    "is not available in the allocation table. Rebuild the master or choose another country/year."
                                )
                            else:
                                st.session_state["empirical_allocation_year"] = active_allocation_year
                                st.session_state["aletheia_synced_evidence_year"] = active_allocation_year
                                st.session_state["aletheia_empirical_allocation_year"] = active_allocation_year

                                alloc_year = allocation_df[
                                    pd.to_numeric(allocation_df["year"], errors="coerce") == active_allocation_year
                                ].sort_values("seats_9k", ascending=False)

                                country_name = str(active_explorer_payload.get("country", st.session_state.get("aletheia_synced_country_name", ""))).strip()
                                iso3_name = str(active_explorer_payload.get("iso3", st.session_state.get("aletheia_synced_iso3", ""))).strip().upper()
                                st.success(
                                    f"Seat allocation view confirmed for diagnostic selection: "
                                    f"{country_name or iso3_name} · {iso3_name} · {active_allocation_year}"
                                )
                                st.caption(
                                    "The allocation chart is now static and tied to the confirmed Country-Year Explorer diagnostic. "
                                    "Change the country/year above, then press the run button again to update this chart."
                                )
                                fig = go.Figure(go.Bar(x=alloc_year["country"], y=alloc_year["seats_9k"]))
                                fig.update_layout(template="plotly_white", title=f"9k allocation · {active_allocation_year}", height=420, margin=dict(l=10, r=10, t=55, b=10))
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No valid years are available for seat display.")
                else:
                    st.info("No valid population/year rows are available for 9k allocation.")

                st.markdown("### Evidence checks")
                st.caption(
                    "Internal checks compare ALETHEIA outputs to variables that may also be score inputs. External validation checks use optional outcome columns that are not score inputs. "
                    "Pearson correlations are withheld until N ≥ 30. For true validation, add external outcomes such as conflict events, coups, regime breakdown, political violence, or future-year decline."
                )
                corr_df, group_df = validation_summary(scored_for_validation)
                vc1, vc2 = st.columns(2)
                with vc1:
                    st.markdown("#### Correlation checks")
                    st.dataframe(corr_df, use_container_width=True, hide_index=True, height=260)
                with vc2:
                    st.markdown("#### Group averages by internal taxonomy")
                    st.caption(
                        "These are internal taxonomy groupings for model diagnostics, not final Sanctuary or authority claims. "
                        + ("Interface/schema inspection only when groups are small; do not infer real effects from N=1 demo classes." if use_template else "Read group averages only after checking group size and outside validation targets.")
                    )
                    display_group_df = _empirical_humility_display_df(group_df)
                    st.dataframe(display_group_df, use_container_width=True, hide_index=True, height=260)

                st.markdown("### Technical details")
                st.caption("Technical tables preserve raw/internal taxonomy fields for traceability and add display labels so SANCTUARY is read as a low-risk internal pattern, not a final claim.")
                overlay_cols = [c for c in ["country", "iso3", "year", "aletheia_verdict", "protocol_overlay_status", "final_audit_interpretation", "evidence_variables_used"] if c in scored.columns]
                if overlay_cols:
                    with st.expander("Protocol detail by country-year", expanded=False):
                        st.dataframe(_empirical_humility_display_df(scored[overlay_cols]), use_container_width=True, hide_index=True, height=300)
                with st.expander("Full empirical output table", expanded=False):
                    st.dataframe(_empirical_humility_display_df(scored), use_container_width=True, hide_index=True, height=420)
                with st.expander("Method note", expanded=False):
                    st.markdown(methodology_markdown())

