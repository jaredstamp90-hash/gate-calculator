import streamlit as st


st.set_page_config(
    page_title="Instant Gate Quote Generator",
    page_icon="🚪",
    layout="centered",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f6f4;
        }
        .block-container {
            max-width: 760px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            color: #17231f;
        }
        div.stButton > button {
            width: 100%;
            min-height: 3rem;
            background: #e85d24;
            color: white;
            border: 0;
            border-radius: 5px;
            font-weight: 700;
        }
        div.stButton > button:hover {
            background: #c94b1b;
            color: white;
            border: 0;
        }
        .quote-box {
            background: white;
            padding: 1.25rem 1.5rem;
            border-radius: 6px;
            border-left: 5px solid #e85d24;
            box-shadow: 0 4px 14px rgba(23, 35, 31, 0.08);
        }
        .quote-total {
            color: #c94b1b;
            margin: 0.5rem 0;
        }
        .quote-note {
            color: #626b66;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_MATERIAL_COST_PER_SQM = 850
GALVANIZING_COST_PER_SQM = 300
POWDER_COATING_COST_PER_SQM = 250
LOCK_OPTIONS = {
    "Standard Deadlock (Basic)": 450,
    "Heavy-Duty Slam-Lock (Recommended)": 950,
    "Enclosed High-Security Lock Box": 1400,
}
ANTI_PRY_BAR_COST = 250
INSTALLATION_FIXED_COST = 850
MARKUP_PERCENTAGE = 0.35


st.title("🛡️ Instant Security Gate Quote")
st.write("Enter your door opening measurements for an immediate estimate.")

with st.form("gate_quote"):
    st.subheader("1. Dimensions")
    width_col, height_col = st.columns(2)
    with width_col:
        width_mm = st.number_input(
            "Width of opening (mm)", min_value=500, max_value=3000, value=900, step=10
        )
    with height_col:
        height_mm = st.number_input(
            "Height of opening (mm)", min_value=1000, max_value=3000, value=2100, step=10
        )

    st.subheader("2. Security upgrades")
    lock_type = st.selectbox("Select lock configuration", list(LOCK_OPTIONS))
    include_anti_pry = st.checkbox("Add anti-pry flat bar protection", value=True)
    include_installation = st.checkbox(
        "Include professional installation and fitment", value=True
    )
    generate_quote = st.form_submit_button("Generate my quote")

if generate_quote:
    square_meters = (width_mm / 1000) * (height_mm / 1000)
    material_cost = square_meters * BASE_MATERIAL_COST_PER_SQM
    finishing_cost = square_meters * (
        GALVANIZING_COST_PER_SQM + POWDER_COATING_COST_PER_SQM
    )
    upgrade_cost = ANTI_PRY_BAR_COST if include_anti_pry else 0
    production_cost = material_cost + finishing_cost + LOCK_OPTIONS[lock_type] + upgrade_cost
    final_quote = production_cost * (1 + MARKUP_PERCENTAGE)
    if include_installation:
        final_quote += INSTALLATION_FIXED_COST

    st.divider()
    st.subheader("Your custom estimate")
    st.markdown(
        f"""
        <div class="quote-box">
            <p><strong>Gate dimensions:</strong> {width_mm} mm × {height_mm} mm ({square_meters:.2f} m²)</p>
            <p><strong>Lock system:</strong> {lock_type}</p>
            <p><strong>Anti-pry protection:</strong> {"Included" if include_anti_pry else "Excluded"}</p>
            <p><strong>Installation:</strong> {"Included" if include_installation else "Excluded (supply only)"}</p>
            <hr style="border: 0; border-top: 1px solid #e7e9e7;">
            <h2 class="quote-total">Estimated total: R {final_quote:,.2f}</h2>
            <p class="quote-note">Indicative pricing based on material costs; subject to site verification.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.success("Capture these details to book your physical site measurement.")