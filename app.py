import joblib
import pandas as pd
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MindPulse — Student Mental Health Prediction",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM MODERN STYLING
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    
    .score-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.15));
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .score-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 4rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
        margin: 10px 0;
    }
    
    .pill-optimal {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    
    .pill-balanced {
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    
    .pill-strain {
        background: rgba(239, 68, 68, 0.2);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    
    .metric-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MODEL LOADING (CACHED)
# =========================================================
@st.cache_resource
def load_model():
    return joblib.load("Mental_Health_Model.pkl")


model = load_model()
top_countries = [
    "Other",
    "Pakistan",
    "USA",
    "Canada",
    "Australia",
    "UK",
    "Germany",
    "Mexico",
    "Turkey",
    "France",
]

# =========================================================
# HEADER & ARCHETYPE PRESETS
# =========================================================
st.markdown(
    '<div class="main-title">MindPulse <span class="gradient-text">Student Wellness AI</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Predictive psychological health analytics powered by a trained Random Forest Regressor.</div>',
    unsafe_allow_html=True,
)

# Preset session state initialization
if "preset" not in st.session_state:
    st.session_state.preset = "balanced"

c1, c2, c3 = st.columns([1, 1, 3])
with c1:
    if st.button("🧘 Load: Balanced Student", use_container_width=True):
        st.session_state.age = 21
        st.session_state.gender = "Male"
        st.session_state.country = "Pakistan"
        st.session_state.academic = "Undergraduate"
        st.session_state.platform = "YouTube"
        st.session_state.purpose = "Education"
        st.session_state.screen_time = 3.0
        st.session_state.unlocks = 35
        st.session_state.study = 4.5
        st.session_state.activity = 1.5
        st.session_state.sleep = 8.0
        st.session_state.stress = "Low"
        st.rerun()

with c2:
    if st.button("📱 Load: Heavy Screen Strain", use_container_width=True):
        st.session_state.age = 22
        st.session_state.gender = "Female"
        st.session_state.country = "Pakistan"
        st.session_state.academic = "Graduate"
        st.session_state.platform = "TikTok"
        st.session_state.purpose = "Entertainment"
        st.session_state.screen_time = 9.5
        st.session_state.unlocks = 140
        st.session_state.study = 1.5
        st.session_state.activity = 0.2
        st.session_state.sleep = 4.5
        st.session_state.stress = "Very High"
        st.rerun()

st.divider()

# =========================================================
# WORKSPACE (2 COLUMNS)
# =========================================================
col_inputs, col_results = st.columns([1.2, 0.9], gap="large")

with col_inputs:
    st.subheader("1. Profile & Demographics")
    p_col1, p_col2, p_col3 = st.columns(3)

    with p_col1:
        age = st.number_input(
            "Age", min_value=10, max_value=100, value=st.session_state.get("age", 21)
        )
    with p_col2:
        gender_options = ["Male", "Female"]
        default_gender_idx = gender_options.index(
            st.session_state.get("gender", "Male")
        )
        gender = st.selectbox("Gender", gender_options, index=default_gender_idx)
    with p_col3:
        country_options = [
            "Pakistan",
            "USA",
            "Canada",
            "Australia",
            "UK",
            "Germany",
            "Mexico",
            "Turkey",
            "France",
            "Other",
        ]
        default_country_idx = country_options.index(
            st.session_state.get("country", "Pakistan")
        )
        country = st.selectbox(
            "Country", country_options, index=default_country_idx
        )

    a_col1, a_col2 = st.columns(2)
    with a_col1:
        acad_options = ["High School", "Undergraduate", "Graduate"]
        default_acad_idx = acad_options.index(
            st.session_state.get("academic", "Undergraduate")
        )
        academic_level = st.selectbox(
            "Academic Standing", acad_options, index=default_acad_idx
        )
    with a_col2:
        purp_options = ["Education", "Entertainment", "Networking", "News"]
        default_purp_idx = purp_options.index(
            st.session_state.get("purpose", "Education")
        )
        purpose_of_use = st.selectbox(
            "Primary Media Purpose", purp_options, index=default_purp_idx
        )

    st.subheader("2. Digital Habits (67.5% Model Weight)")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        plat_options = [
            "YouTube",
            "Instagram",
            "TikTok",
            "WhatsApp",
            "LinkedIn",
            "Twitter",
            "Facebook",
            "Snapchat",
            "WeChat",
            "LINE",
            "KakaoTalk",
            "VKontakte",
        ]
        default_plat_idx = plat_options.index(
            st.session_state.get("platform", "YouTube")
        )
        most_used_platform = st.selectbox(
            "Most-Used Platform", plat_options, index=default_plat_idx
        )
    with d_col2:
        daily_unlocks = st.slider(
            "Daily Phone Unlocks",
            min_value=0,
            max_value=300,
            value=st.session_state.get("unlocks", 35),
            step=5,
        )

    avg_daily_usage_hours = st.slider(
        "Average Daily Screen Time (Hours/Day)",
        min_value=0.0,
        max_value=16.0,
        value=st.session_state.get("screen_time", 3.0),
        step=0.5,
        help="Primary model driver: Higher social screen hours strongly lower resilience.",
    )

    st.subheader("3. Lifestyle, Recovery & Stress")
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        sleep_hours_per_night = st.slider(
            "Nightly Sleep (hrs)",
            min_value=0.0,
            max_value=14.0,
            value=st.session_state.get("sleep", 8.0),
            step=0.5,
        )
    with l_col2:
        study_hours = st.slider(
            "Study Hours/Day",
            min_value=0.0,
            max_value=14.0,
            value=st.session_state.get("study", 4.5),
            step=0.5,
        )
    with l_col3:
        physical_activity_hours = st.slider(
            "Exercise (hrs/day)",
            min_value=0.0,
            max_value=6.0,
            value=st.session_state.get("activity", 1.5),
            step=0.5,
        )

    stress_options = ["Low", "Medium", "High", "Very High"]
    default_stress_idx = stress_options.index(
        st.session_state.get("stress", "Low")
    )
    stress_level = st.select_slider(
        "Perceived Stress Level",
        options=stress_options,
        value=stress_options[default_stress_idx],
    )

# =========================================================
# MODEL INFERENCE CALCULATION
# =========================================================
country_group = country if country in top_countries else "Other"

input_row = pd.DataFrame(
    [
        {
            "Age": age,
            "Gender": gender,
            "Country": country,
            "Academic_Level": academic_level,
            "Most_Used_Platform": most_used_platform,
            "Purpose_Of_Use": purpose_of_use,
            "Avg_Daily_Usage_Hours": float(avg_daily_usage_hours),
            "Daily_Unlocks": int(daily_unlocks),
            "Study_Hours": float(study_hours),
            "Physical_Activity_Hours": float(physical_activity_hours),
            "Sleep_Hours_Per_Night": float(sleep_hours_per_night),
            "Stress_Level": stress_level,
            "Grouped_country": country_group,
        }
    ]
)

predicted_score = round(float(model.predict(input_row)[0]), 2)
clamped_score = max(0.0, min(10.0, predicted_score))

# =========================================================
# RESULTS & TELEMETRY HUB (RIGHT COLUMN)
# =========================================================
with col_results:
    st.subheader("Diagnostic Telemetry")

    if clamped_score >= 7.0:
        badge_html = '<span class="pill-optimal">🟢 Optimal Resilience</span>'
        narrative = f"Excellent balance! Your daily rhythms in **{country}** show healthy circadian rest and sustainable media usage."
    elif clamped_score >= 5.0:
        badge_html = '<span class="pill-balanced">🟡 Moderate Strain</span>'
        narrative = f"Manageable baseline in **{country}**. High screen time ({avg_daily_usage_hours}h) or fragmented sleep is creating slight attentional drag."
    else:
        badge_html = '<span class="pill-strain">🔴 Elevated Risk</span>'
        narrative = f"Noticeable strain detected in **{country}**. Heavy digital usage ({avg_daily_usage_hours}h) coupled with {stress_level.lower()} stress signals burnout risk."

    st.markdown(
        f"""
        <div class="score-card">
            <span style="font-size: 0.9rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">Predicted Wellness Score</span>
            <div class="score-num">{clamped_score:.2f} <span style="font-size: 1.5rem; color: #64748B;">/ 10</span></div>
            {badge_html}
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Visual gauge / progress bar
    st.progress(
        clamped_score / 10.0,
        text=f"Cohort Benchmark: {clamped_score:.1f} out of 10.0",
    )

    st.info(narrative)

    # Breakdown factor metrics
    st.markdown("#### Key Factor Breakdown")
    m1, m2 = st.columns(2)
    with m1:
        st.metric(
            label="Digital Load (67.5% Weight)",
            value=f"{avg_daily_usage_hours} hrs",
            delta="- Optimal" if avg_daily_usage_hours <= 4.0 else "+ High Load",
            delta_color="normal"
            if avg_daily_usage_hours <= 4.0
            else "inverse",
        )
    with m2:
        st.metric(
            label="Restorative Sleep (11.1%)",
            value=f"{sleep_hours_per_night} hrs",
            delta="+ Restorative"
            if sleep_hours_per_night >= 7.0
            else "- Deficit",
            delta_color="normal"
            if sleep_hours_per_night >= 7.0
            else "inverse",
        )

    # Actionable Recommendation Nudge
    if avg_daily_usage_hours > 5.0:
        st.success(
            f"💡 **AI Recommendation**: Trimming 1.5h of {most_used_platform} daily can lift your score by ~1.2 points."
        )
    elif sleep_hours_per_night < 7.0:
        st.success(
            "💡 **AI Recommendation**: Prioritize reaching 7.5h of sleep per night to maximize cognitive recovery."
        )
    else:
        st.success(
            "💡 **AI Recommendation**: Your current routine is well-calibrated. Maintain phone unlocks under 50 to preserve focus."
        )
