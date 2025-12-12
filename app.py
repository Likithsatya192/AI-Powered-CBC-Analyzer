import streamlit as st
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

from app.run_pipeline import run_full_pipeline

# Streamlit Config
st.set_page_config(
    page_title="CBC Analyzer",
    page_icon="🩸",
    layout="wide"
)

st.title("🩸 AI-Powered CBC Analyzer")
st.caption("Upload a CBC report (PDF or image) to extract, validate, interpret, and visualize parameters.")

uploaded = st.file_uploader(
    "Upload CBC Report",
    type=["pdf", "jpg", "jpeg", "png"],
    help="Supports PDF or common image formats."
)

if uploaded:
    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded.read())
        file_path = tmp.name

    with st.status("Processing report… please wait", expanded=False) as status:
        result = run_full_pipeline(file_path)
        status.update(label="Processing complete", state="complete")

    # ==========================
    # 1) Extracted Parameters
    # ==========================
    st.subheader("📌 Extracted CBC Parameters (raw OCR)")
    expected_params = 13  # number of entries in reference_ranges.json
    extracted_count = len(result.extracted_params or {})
    coverage = (extracted_count / expected_params * 100) if expected_params else 0
    st.caption(f"Captured {extracted_count} / {expected_params} parameters ({coverage:.0f}%).")
    if coverage < 50:
        st.warning("Low extraction coverage (<50%). Try a higher-resolution scan or brighter image.")
    if result.extracted_params:
        extracted_df = pd.DataFrame([
            {
                "Parameter": k,
                "Raw Value": v.get("raw_value"),
                "Final Value": v.get("value"),
                "Unit": v.get("unit"),
                "Scale Adjustment": v.get("scale_note"),
            }
            for k, v in result.extracted_params.items()
        ]).sort_values("Parameter")

        st.dataframe(
            extracted_df,
            use_container_width=True,
            height=min(600, 70 + 32 * len(extracted_df)),
        )

        csv_buf = StringIO()
        extracted_df.to_csv(csv_buf, index=False)
        st.download_button(
            "Download extracted parameters as CSV",
            data=csv_buf.getvalue(),
            file_name="cbc_extracted.csv",
            mime="text/csv",
        )
    else:
        st.warning("No CBC parameters were extracted. OCR or parsing may have failed.")

    # ==========================
    # 2) Validated Parameters
    # ==========================
    st.subheader("✅ Validated Parameters (with reference ranges)")
    if result.validated_params:
        validated_df = pd.DataFrame([
            {
                "Parameter": param,
                "Value": info["value"],
                "Unit": info["unit"],
                "Ref Low": info["reference"]["low"],
                "Ref High": info["reference"]["high"],
            }
            for param, info in result.validated_params.items()
        ]).sort_values("Parameter")
        st.dataframe(
            validated_df,
            use_container_width=True,
            height=min(600, 70 + 32 * len(validated_df)),
        )
    else:
        st.warning("No parameters passed validation. Check OCR quality or reference configs.")

    # ==========================
    # 3) Model Interpretation
    # ==========================
    st.subheader("🧭 Interpretation (Normal / High / Low)")
    if result.param_interpretation:
        interp_df = pd.DataFrame([
            {
                "Parameter": param,
                "Value": info["value"],
                "Unit": info.get("unit"),
                "Status": info["status"],
                "Ref Low": info["reference"]["low"],
                "Ref High": info["reference"]["high"],
            }
            for param, info in result.param_interpretation.items()
        ]).sort_values("Parameter")
        st.dataframe(
            interp_df,
            use_container_width=True,
            height=min(600, 70 + 32 * len(interp_df)),
        )
    else:
        st.info("No interpreted results available yet.")

    # ==========================
    # 4) Visualization
    # ==========================
    st.subheader("📊 CBC Parameter Graph")
    if result.extracted_params:
        df_plot = pd.DataFrame([
            {"Parameter": k, "Value": v["value"]}
            for k, v in result.extracted_params.items()
            if v.get("value") is not None
        ])

        if len(df_plot) > 0:
            plt.figure(figsize=(10, 5))
            plt.bar(df_plot["Parameter"], df_plot["Value"], color="#4c82fb")
            plt.xticks(rotation=45, ha="right")
            plt.ylabel("Value")
            plt.title("CBC Parameter Values")
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.warning("No numerical CBC values available for visualization.")
    else:
        st.warning("Visualization not available. No parameters extracted.")

    # ==========================
    # 5) Errors & Warnings
    # ==========================
    if result.errors:
        st.subheader("⚠️ Warnings / Errors")
        for err in result.errors:
            st.error(err)