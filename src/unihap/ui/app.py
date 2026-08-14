"""
==============================================================================
FILE: src/unihap/ui/app.py
MODULE: Streamlit Human-in-the-Loop (HITL) Review Dashboard
PURPOSE:
    Provides a feature-rich, interactive web dashboard for catalog curators and reviewers:
      - Uploading raw catalog spreadsheets (XLSX / CSV) or running on bundled datasets
      - Automatically loads and runs on the 1,000-row catalog on first launch
      - High-level KPIs (Total Processed, Auto-Approved %, Needs-Review %, Rejected %)
      - Interactive filterable Data Table with configurable display size (All 1,000, 500, 250, 100)
      - Detail Record Inspector: Side-by-side view of raw input, canonical master data,
        5 description formats, and attribute table with exact `evidence_span` & source URL
      - One-click Curator Approval / Correction editor updating the feedback queue
      - One-click "Export 252-Column Delivery CSV" button with live download
==============================================================================
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from unihap.core.delivery_format import DeliveryFormatExporter
from unihap.pipeline import UniHAPPipeline

st.set_page_config(page_title="UniHAP — Catalog Review Dashboard", page_icon="⚡", layout="wide")

# Custom CSS for clean, high-contrast dashboard aesthetics
st.markdown(
    """
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px 16px;
        border: 1px solid #e9ecef;
    }
    .badge-approved {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-review {
        background-color: #fff3cd;
        color: #856404;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-rejected {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ UniHAP — Product Intelligence & Enrichment Engine")
st.caption("12-Layer Evidence-Grounded Catalog Enrichment & Human-in-the-Loop Review Queue")

# Sidebar Controls
st.sidebar.header("📁 Data Input & Execution")

sample_input_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "raw" / "unihack_sample_input.csv"
input_mode = st.sidebar.radio(
    "Select Catalog Source:", ["Use Bundled 1,000-Row Sample Dataset", "Upload Custom Catalog File (.csv / .xlsx)"]
)

uploaded_file = None
active_input_path = None

if input_mode == "Upload Custom Catalog File (.csv / .xlsx)":
    uploaded_file = st.sidebar.file_uploader("Upload Catalog Sheet", type=["csv", "xlsx"])
    if uploaded_file:
        temp_dir = Path("/tmp/unihap_uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        active_input_path = temp_dir / uploaded_file.name
        with open(active_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    if sample_input_path.exists():
        active_input_path = sample_input_path
        st.sidebar.info("Using bundled dataset: `unihack_sample_input.csv` (1,000 rows)")

# Auto-run on startup if not already run
if "pipeline_result" not in st.session_state and active_input_path and active_input_path.exists():
    pipeline = UniHAPPipeline()
    result = pipeline.run(active_input_path)
    st.session_state["pipeline_result"] = result
    st.session_state["pipeline_instance"] = pipeline

# Manual Re-Run Button
if st.sidebar.button("🔄 Re-Run 12-Layer Pipeline", type="primary"):
    if active_input_path and active_input_path.exists():
        with st.spinner("Executing 12-layer pipeline on all catalog records..."):
            pipeline = UniHAPPipeline()
            result = pipeline.run(active_input_path)
            st.session_state["pipeline_result"] = result
            st.session_state["pipeline_instance"] = pipeline
            st.sidebar.success(f"Processed {result.total_processed} records in {result.execution_time_seconds}s!")
    else:
        st.sidebar.error("Please provide a valid input catalog file.")

# Main Dashboard View
if "pipeline_result" in st.session_state:
    res = st.session_state["pipeline_result"]
    records = res.records

    # Summary KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Processed", res.total_processed)
    col2.metric(
        "Auto-Approved (≥85%)",
        f"{res.auto_approved_count} ({round(res.auto_approved_count / res.total_processed * 100, 1)}%)",
    )
    col3.metric(
        "Needs Review (55-84%)",
        f"{res.needs_review_count} ({round(res.needs_review_count / res.total_processed * 100, 1)}%)",
    )
    col4.metric(
        "Rejected (<55%)", f"{res.rejected_count} ({round(res.rejected_count / res.total_processed * 100, 1)}%)"
    )
    col5.metric("Execution Latency", f"{res.execution_time_seconds}s")

    st.divider()

    # Filter Controls
    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 2])
    status_filter = fcol1.selectbox("Filter by Status Tier:", ["All", "auto-approved", "needs-review", "rejected"])
    search_query = fcol2.text_input("Search by MPN or Manufacturer:", "")
    page_size_option = fcol3.selectbox("Display Rows:", ["All (1,000)", 500, 250, 100], index=0)

    # Export Delivery CSV Button
    delivery_csv_path = Path("/tmp/unihap_delivery_export.csv")
    DeliveryFormatExporter.export_to_csv(records, delivery_csv_path)
    with open(delivery_csv_path, "rb") as f:
        fcol4.download_button(
            label="📥 Download 252-Col CSV",
            data=f,
            file_name="unihap_252_column_delivery.csv",
            mime="text/csv",
            type="secondary",
        )

    # Filter records
    filtered_records = records
    if status_filter != "All":
        filtered_records = [r for r in filtered_records if r.overall_status.value == status_filter]
    if search_query:
        q = search_query.lower()
        filtered_records = [
            r
            for r in filtered_records
            if q in r.mpn.lower()
            or q in r.canonical_manufacturer.lower()
            or q in (r.descriptions.short_title or "").lower()
        ]

    # Slice for display
    if page_size_option == "All (1,000)":
        display_records = filtered_records
    else:
        display_records = filtered_records[: int(page_size_option)]

    st.subheader(
        f"Enriched Catalog Items ({len(filtered_records)} total matching filter, displaying {len(display_records)})"
    )

    # Construct Display Table
    table_rows = []
    for r in display_records:
        table_rows.append(
            {
                "Row ID": r.row_id,
                "MPN": r.mpn,
                "Manufacturer": r.canonical_manufacturer,
                "Classification": r.classification.full_path if r.classification else "",
                "Invoice Desc (≤40 CAPS)": r.descriptions.invoice_caps,
                "Confidence": f"{round(r.overall_confidence * 100, 1)}%",
                "Status": r.overall_status.value,
            }
        )

    df_display = pd.DataFrame(table_rows)
    st.dataframe(df_display, use_container_width=True, height=380)

    # Detail Record Inspector
    st.divider()
    st.subheader("🔍 Record Inspector & Evidence Citations")

    if filtered_records:
        selected_row_id = st.selectbox(
            "Select Record to Inspect Detail & Provenance:",
            [r.row_id for r in filtered_records],
            format_func=lambda rid: (
                f"Row {rid} — {[r.mpn for r in filtered_records if r.row_id == rid][0]} ({[r.canonical_manufacturer for r in filtered_records if r.row_id == rid][0]})"
            ),
        )

        if selected_row_id:
            target_rec = next(r for r in filtered_records if r.row_id == selected_row_id)

            icol1, icol2 = st.columns(2)

            with icol1:
                st.markdown("#### Master Data & Descriptions")
                st.markdown(f"**Canonical Manufacturer**: `{target_rec.canonical_manufacturer}`")
                st.markdown(f"**Canonical Brand**: `{target_rec.canonical_brand}`")
                st.markdown(
                    f"**Classpath**: `{target_rec.classification.full_path if target_rec.classification else 'N/A'}`"
                )
                st.markdown(f"**Official Spec URL**: [{target_rec.spec_source_url}]({target_rec.spec_source_url})")

                st.markdown("##### Synthesized 5 Formats:")
                st.code(
                    f"INVOICE_DESC (<=40 CAPS) : {target_rec.descriptions.invoice_caps}\n"
                    f"MOBILE_DESC (60-80 chars): {target_rec.descriptions.mobile}\n"
                    f"SHORT_DESC               : {target_rec.descriptions.short_title}\n\n"
                    f"LONG_DESC:\n{target_rec.descriptions.long_desc}"
                )

            with icol2:
                st.markdown("#### Extracted Attributes & Evidence Spans")
                attr_table = []
                for aname, aval in target_rec.attributes.items():
                    if aval.normalized_value:
                        span_text = aval.provenance.exact_text_span if aval.provenance else "Direct Match"
                        attr_table.append(
                            {
                                "Attribute": aname,
                                "Normalized Value": aval.normalized_value,
                                "In LOV": "✅" if aval.in_lov else "❌",
                                "Evidence Span Quote": span_text,
                                "Status": aval.status.value,
                            }
                        )

                if attr_table:
                    st.dataframe(pd.DataFrame(attr_table), use_container_width=True)
                else:
                    st.info("No attributes extracted for this item.")

            # Human Correction / Curation Tool
            st.markdown("##### ✍️ Human-in-the-Loop Curation Tool")
            with st.expander("Apply Human Override / Correction"):
                corr_attr = st.selectbox(
                    "Attribute to Correct:", list(target_rec.attributes.keys()) if target_rec.attributes else ["Finish"]
                )
                corr_val = st.text_input("New Corrected LOV Value:", "")
                if st.button("Apply Correction & Approve Record"):
                    if corr_val and "pipeline_instance" in st.session_state:
                        pl = st.session_state["pipeline_instance"]
                        pl.hitl_queue.add_to_queue(target_rec)
                        updated = pl.hitl_queue.apply_human_correction(target_rec.row_id, {corr_attr: corr_val})
                        st.success(
                            f"Applied correction for Row {target_rec.row_id}: {corr_attr} -> {corr_val}. Status promoted to AUTO_APPROVED!"
                        )
                        st.rerun()

else:
    st.info("👈 Click **Run 12-Layer Pipeline** in the sidebar to start batch catalog processing!")
