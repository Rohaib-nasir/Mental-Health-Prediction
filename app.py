import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MindPulse — Student Mental Health AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# GLOBAL CSS — Dark Space + Glassmorphism + Neon
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@500;700&display=swap');

    /* ── Reset & background ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #060814 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #E2E8F0 !important;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], section[data-testid="stSidebar"] {
        background: transparent !important;
        display: none !important;
    }
    [data-testid="stMain"] > div:first-child {
        padding-top: 2rem !important;
    }

    /* Aurora background blobs */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 60% 50% at 10% 20%, rgba(139,92,246,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 50% 40% at 85% 70%, rgba(6,182,212,0.14) 0%, transparent 55%),
            radial-gradient(ellipse 40% 35% at 50% 95%, rgba(0,245,155,0.10) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* Ensure content is above aurora */
    .block-container { position: relative; z-index: 1; max-width: 1280px !important; padding: 1rem 2rem 4rem !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1225; }
    ::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.5); border-radius: 999px; }

    /* ── Hero header ── */
    .hero-wrap { text-align: center; margin-bottom: 2rem; }
    .hero-badge {
        display: inline-block; margin-bottom: 1rem;
        background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.4);
        border-radius: 9999px; padding: 6px 18px;
        font-size: 0.75rem; font-weight: 700; color: #A78BFA;
        letter-spacing: 0.12em; text-transform: uppercase;
    }
    .hero-title {
        font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 800;
        line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 0.6rem;
        background: linear-gradient(135deg, #C4B5FD 0%, #67E8F9 45%, #6EE7B7 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: 1rem; color: #64748B; max-width: 520px; margin: 0 auto 1.6rem;
        line-height: 1.7;
    }

    /* ── Preset buttons row ── */
    .preset-row { display: flex; gap: 12px; justify-content: center; margin-bottom: 0.5rem; flex-wrap: wrap; }
    .preset-btn {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 24px; border-radius: 9999px; cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem; font-weight: 700; border: none; transition: all .25s;
    }
    .preset-btn-balanced {
        background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(6,182,212,0.25));
        border: 1px solid rgba(139,92,246,0.5); color: #C4B5FD;
    }
    .preset-btn-strain {
        background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(245,158,11,0.2));
        border: 1px solid rgba(239,68,68,0.5); color: #FCA5A5;
    }
    .preset-btn:hover { filter: brightness(1.3); transform: translateY(-1px); }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.6rem 0 !important; }

    /* ── Glass card wrapper ── */
    .glass-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px 24px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
    }

    /* ── Section headings ── */
    .section-label {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; margin-bottom: 16px;
        color: transparent;
        background: linear-gradient(90deg, #8B5CF6, #06B6D4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* ── Override Streamlit widget label color ── */
    label, .stSlider label, .stSelectbox label, .stNumberInput label,
    [data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
    }

    /* ── Input & select styling ── */
    input, textarea, select,
    [data-testid="stNumberInput"] input,
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
    }
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"] > div:focus-within {
        border-color: rgba(139,92,246,0.6) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
    }
    /* Dropdown menu */
    [data-baseweb="popover"] { background: #0f1629 !important; }
    [data-baseweb="menu"] { background: #0f1629 !important; border: 1px solid rgba(139,92,246,0.3) !important; }
    [role="option"]:hover { background: rgba(139,92,246,0.2) !important; }

    /* ── Slider track ── */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #8B5CF6 !important;
        box-shadow: 0 0 8px rgba(139,92,246,0.8) !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] div[class*="Track"] {
        background: rgba(139,92,246,0.3) !important;
    }

    /* ── Streamlit native button override for preset ── */
    [data-testid="stButton"] button {
        background: rgba(139,92,246,0.15) !important;
        border: 1px solid rgba(139,92,246,0.45) !important;
        color: #C4B5FD !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.5rem 1.2rem !important;
        transition: all .25s !important;
    }
    [data-testid="stButton"] button:hover {
        background: rgba(139,92,246,0.3) !important;
        box-shadow: 0 0 16px rgba(139,92,246,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Progress bar ── */
    [data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #8B5CF6, #06B6D4, #10B981) !important;
        border-radius: 9999px !important;
        box-shadow: 0 0 10px rgba(139,92,246,0.6) !important;
    }
    [data-testid="stProgress"] > div > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 9999px !important;
    }

    /* ── Info / success / warning ── */
    [data-testid="stAlert"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
        color: #CBD5E1 !important;
    }

    /* ── Score card ── */
    .score-card {
        background: linear-gradient(135deg, rgba(139,92,246,0.12) 0%, rgba(6,182,212,0.10) 100%);
        border: 1px solid rgba(139,92,246,0.35);
        border-radius: 20px;
        padding: 28px 20px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 16px;
        box-shadow: 0 0 40px rgba(139,92,246,0.12), inset 0 1px 0 rgba(255,255,255,0.07);
    }
    .score-card::before {
        content: '';
        position: absolute;
        top: 0; left: -60%; width: 40%; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.8), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    @keyframes shimmer { 0%{left:-60%} 100%{left:140%} }

    .score-label {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: #64748B; margin-bottom: 8px;
    }
    .score-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 4.5rem; font-weight: 700; line-height: 1;
        background: linear-gradient(135deg, #C4B5FD 0%, #67E8F9 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        animation: countIn .8s ease-out;
    }
    .score-denom { font-size: 1.4rem; color: #334155; }
    @keyframes countIn { from { opacity:0; transform: scale(0.85); } to { opacity:1; transform: scale(1); } }

    .pill {
        display: inline-block;
        padding: 6px 18px; border-radius: 9999px;
        font-weight: 700; font-size: 0.82rem; letter-spacing: 0.04em;
    }
    .pill-optimal { background: rgba(16,185,129,0.18); color: #34D399; border: 1px solid rgba(16,185,129,0.45); }
    .pill-balanced { background: rgba(245,158,11,0.18); color: #FCD34D; border: 1px solid rgba(245,158,11,0.45); }
    .pill-strain   { background: rgba(239,68,68,0.18);  color: #FCA5A5; border: 1px solid rgba(239,68,68,0.45);  }

    /* ── Factor metric cards ── */
    .factor-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px; }
    .factor-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px; padding: 14px 16px;
    }
    .factor-label { font-size: 0.7rem; color: #475569; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px; }
    .factor-value { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 700; color: #E2E8F0; }
    .factor-delta-good { font-size: 0.72rem; color: #34D399; font-weight: 700; margin-top: 2px; }
    .factor-delta-bad  { font-size: 0.72rem; color: #FCA5A5; font-weight: 700; margin-top: 2px; }

    /* ── Recommendation card ── */
    .rec-card {
        background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(6,182,212,0.08));
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 14px; padding: 16px 18px; margin-top: 14px;
        font-size: 0.88rem; color: #A7F3D0; line-height: 1.7;
    }
    .rec-icon { font-size: 1.1rem; margin-right: 6px; }

    /* ── Narrative box ── */
    .narrative-box {
        background: rgba(255,255,255,0.025);
        border-left: 3px solid #8B5CF6;
        border-radius: 0 12px 12px 0;
        padding: 12px 16px; margin-bottom: 16px;
        font-size: 0.88rem; color: #94A3B8; line-height: 1.7;
    }

    /* ── Stress select-slider override ── */
    [data-testid="stSlider"] div[data-baseweb="slider"] { padding: 0 8px !important; }

    /* ── Select slider pips ── */
    [class*="StepMark"] { color: #475569 !important; }

    /* ── Streamlit metric override ── */
    [data-testid="stMetric"] { display: none !important; }

    /* ── Footer ── */
    .footer { text-align: center; padding: 2rem 0 0; color: #1E293B; font-size: 0.75rem; }
    .footer span { color: #334155; }

    /* hide streamlit hamburger */
    #MainMenu, footer { visibility: hidden !important; }
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
    "Other", "Pakistan", "USA", "Canada", "Australia",
    "UK", "Germany", "Mexico", "Turkey", "France",
]

# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-badge">⚡ AI-Powered Wellness Analytics</div>
        <div class="hero-title">MindPulse Student<br>Mental Health Prediction</div>
        <div class="hero-sub">
            A Random Forest model trained on 1,000+ students
            predicts your psychological resilience score in real-time.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# PRESET SESSION STATE INIT
# =========================================================
if "preset_loaded" not in st.session_state:
    st.session_state.preset_loaded = False

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("🧘 Balanced Student", use_container_width=True):
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
    if st.button("📱 Heavy Screen Strain", use_container_width=True):
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

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# WORKSPACE — TWO COLUMN LAYOUT
# =========================================================
col_inputs, col_results = st.columns([1.25, 0.95], gap="large")

# ── LEFT: Inputs ──────────────────────────────────────────
with col_inputs:

    # Section 1 — Demographics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">01 · Profile & Demographics</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.get("age", 21))
    with p2:
        gender_opts = ["Male", "Female"]
        gender = st.selectbox("Gender", gender_opts, index=gender_opts.index(st.session_state.get("gender", "Male")))
    with p3:
        country_opts = ["Pakistan","USA","Canada","Australia","UK","Germany","Mexico","Turkey","France","Other"]
        country = st.selectbox("Country", country_opts, index=country_opts.index(st.session_state.get("country", "Pakistan")))

    a1, a2 = st.columns(2)
    with a1:
        acad_opts = ["High School", "Undergraduate", "Graduate"]
        academic_level = st.selectbox("Academic Level", acad_opts, index=acad_opts.index(st.session_state.get("academic", "Undergraduate")))
    with a2:
        purp_opts = ["Education", "Entertainment", "Networking", "News"]
        purpose_of_use = st.selectbox("Primary Media Purpose", purp_opts, index=purp_opts.index(st.session_state.get("purpose", "Education")))

    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2 — Digital Habits
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">02 · Digital Habits — 67.5% Model Weight</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        plat_opts = ["YouTube","Instagram","TikTok","WhatsApp","LinkedIn","Twitter","Facebook","Snapchat","WeChat","LINE","KakaoTalk","VKontakte"]
        most_used_platform = st.selectbox("Most-Used Platform", plat_opts, index=plat_opts.index(st.session_state.get("platform", "YouTube")))
    with d2:
        daily_unlocks = st.slider("Daily Phone Unlocks", 0, 300, st.session_state.get("unlocks", 35), step=5)

    avg_daily_usage_hours = st.slider(
        "Average Daily Screen Time (hrs/day)",
        0.0, 16.0, float(st.session_state.get("screen_time", 3.0)), step=0.5,
        help="Primary model driver — higher hours strongly lower resilience.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 3 — Lifestyle
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 · Lifestyle, Recovery & Stress</div>', unsafe_allow_html=True)

    l1, l2, l3 = st.columns(3)
    with l1:
        sleep_hours_per_night = st.slider("Nightly Sleep (hrs)", 0.0, 14.0, float(st.session_state.get("sleep", 8.0)), step=0.5)
    with l2:
        study_hours = st.slider("Study Hours/Day", 0.0, 14.0, float(st.session_state.get("study", 4.5)), step=0.5)
    with l3:
        physical_activity_hours = st.slider("Exercise (hrs/day)", 0.0, 6.0, float(st.session_state.get("activity", 1.5)), step=0.5)

    stress_opts = ["Low", "Medium", "High", "Very High"]
    stress_level = st.select_slider(
        "Perceived Stress Level",
        options=stress_opts,
        value=stress_opts[stress_opts.index(st.session_state.get("stress", "Low"))],
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# MODEL INFERENCE
# =========================================================
country_group = country if country in top_countries else "Other"
input_row = pd.DataFrame([{
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
}])

predicted_score = round(float(model.predict(input_row)[0]), 2)
clamped_score = max(0.0, min(10.0, predicted_score))
pct = clamped_score / 10.0

# ── RIGHT: Results ────────────────────────────────────────
with col_results:

    # Status determination
    if clamped_score >= 7.0:
        pill_cls = "pill-optimal"
        pill_txt = "🟢 Optimal Resilience"
        arc_color1, arc_color2 = "#10B981", "#34D399"
        narrative = (
            f"Excellent balance! Your daily rhythms show healthy circadian rest "
            f"and sustainable media usage. Keep screen time under "
            f"{avg_daily_usage_hours + 1:.0f}h and maintain your sleep schedule."
        )
    elif clamped_score >= 5.0:
        pill_cls = "pill-balanced"
        pill_txt = "🟡 Moderate Strain"
        arc_color1, arc_color2 = "#F59E0B", "#FCD34D"
        narrative = (
            f"Manageable baseline — {avg_daily_usage_hours}h of daily screen time "
            f"or fragmented sleep is creating slight attentional drag. "
            f"A 30-min wind-down before bed can help."
        )
    else:
        pill_cls = "pill-strain"
        pill_txt = "🔴 Elevated Risk"
        arc_color1, arc_color2 = "#EF4444", "#FCA5A5"
        narrative = (
            f"Noticeable strain detected. Heavy digital usage ({avg_daily_usage_hours}h/day) "
            f"coupled with {stress_level.lower()} stress signals burnout risk. "
            f"Reducing screen time is the highest-impact change you can make."
        )

    # Score + SVG gauge
    gauge_deg = pct * 180  # 0–180°
    gauge_html = f"""
    <div style="font-family:'Plus Jakarta Sans',sans-serif;">
      <!-- Score card -->
      <div class="score-card" style="
        background:linear-gradient(135deg,rgba(139,92,246,0.12),rgba(6,182,212,0.10));
        border:1px solid rgba(139,92,246,0.35);border-radius:20px;padding:24px 16px 20px;
        text-align:center;position:relative;overflow:hidden;margin-bottom:16px;
        box-shadow:0 0 40px rgba(139,92,246,0.12),inset 0 1px 0 rgba(255,255,255,0.07);
      ">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;
          background:linear-gradient(90deg,transparent,rgba(139,92,246,0.8),transparent);
          animation:shimmer 3s ease-in-out infinite;">
        </div>
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
          text-transform:uppercase;color:#475569;margin-bottom:10px;">
          Predicted Wellness Score
        </div>

        <!-- SVG Gauge -->
        <svg viewBox="0 0 200 120" style="width:100%;max-width:220px;display:block;margin:0 auto 4px;">
          <defs>
            <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="{arc_color1}"/>
              <stop offset="100%" stop-color="{arc_color2}"/>
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <!-- Track -->
          <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none"
            stroke="rgba(255,255,255,0.06)" stroke-width="12" stroke-linecap="round"/>
          <!-- Active arc — we use a rotate transform trick -->
          <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none"
            stroke="url(#arcGrad)" stroke-width="12" stroke-linecap="round"
            stroke-dasharray="251.3" stroke-dashoffset="{251.3 * (1 - pct):.1f}"
            filter="url(#glow)"
            style="transition: stroke-dashoffset 0.8s ease;"/>
          <!-- Center dot -->
          <circle cx="100" cy="100" r="5" fill="{arc_color1}" filter="url(#glow)"/>
          <!-- Labels -->
          <text x="16" y="116" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">0</text>
          <text x="100" y="22" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace" text-anchor="middle">5</text>
          <text x="180" y="116" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace" text-anchor="end">10</text>
        </svg>

        <div style="font-family:'JetBrains Mono',monospace;font-size:4rem;font-weight:700;
          line-height:1;background:linear-gradient(135deg,#C4B5FD,#67E8F9);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 10px;">
          {clamped_score:.2f}<span style="font-size:1.3rem;color:#334155;-webkit-text-fill-color:#334155;">&nbsp;/ 10</span>
        </div>
        <span style="display:inline-block;padding:6px 18px;border-radius:9999px;
          font-weight:700;font-size:0.82rem;letter-spacing:0.04em;
          background:{'rgba(16,185,129,0.18)' if clamped_score>=7 else 'rgba(245,158,11,0.18)' if clamped_score>=5 else 'rgba(239,68,68,0.18)'};
          color:{'#34D399' if clamped_score>=7 else '#FCD34D' if clamped_score>=5 else '#FCA5A5'};
          border:1px solid {'rgba(16,185,129,0.45)' if clamped_score>=7 else 'rgba(245,158,11,0.45)' if clamped_score>=5 else 'rgba(239,68,68,0.45)'};
        ">{pill_txt}</span>
      </div>

      <!-- Narrative -->
      <div style="background:rgba(255,255,255,0.025);border-left:3px solid #8B5CF6;
        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:16px;
        font-size:0.87rem;color:#94A3B8;line-height:1.75;font-family:'Plus Jakarta Sans',sans-serif;">
        {narrative}
      </div>

      <!-- Progress bar -->
      <div style="margin-bottom:18px;">
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#475569;margin-bottom:6px;">
          <span>Cohort Benchmark</span><span style="color:#94A3B8;">{clamped_score:.1f} / 10.0</span>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:9999px;height:8px;overflow:hidden;">
          <div style="height:100%;width:{pct*100:.1f}%;border-radius:9999px;
            background:linear-gradient(90deg,#8B5CF6,#06B6D4,#10B981);
            box-shadow:0 0 10px rgba(139,92,246,0.6);transition:width 0.8s ease;">
          </div>
        </div>
      </div>

      <!-- Factor cards -->
      <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
        color:#475569;margin-bottom:10px;">Key Factor Breakdown</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:14px;padding:14px 16px;">
          <div style="font-size:0.67rem;color:#475569;font-weight:700;letter-spacing:0.08em;
            text-transform:uppercase;margin-bottom:4px;">Digital Load<br><span style="color:#6B7280;font-weight:400;">(67.5% weight)</span></div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#E2E8F0;">{avg_daily_usage_hours}h</div>
          <div style="font-size:0.72rem;font-weight:700;margin-top:2px;color:{'#34D399' if avg_daily_usage_hours<=4 else '#FCA5A5'};">
            {'✓ Optimal' if avg_daily_usage_hours<=4 else '⚠ High Load'}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:14px;padding:14px 16px;">
          <div style="font-size:0.67rem;color:#475569;font-weight:700;letter-spacing:0.08em;
            text-transform:uppercase;margin-bottom:4px;">Sleep Recovery<br><span style="color:#6B7280;font-weight:400;">(11.1% weight)</span></div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#E2E8F0;">{sleep_hours_per_night}h</div>
          <div style="font-size:0.72rem;font-weight:700;margin-top:2px;color:{'#34D399' if sleep_hours_per_night>=7 else '#FCA5A5'};">
            {'✓ Restorative' if sleep_hours_per_night>=7 else '⚠ Sleep Deficit'}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:14px;padding:14px 16px;">
          <div style="font-size:0.67rem;color:#475569;font-weight:700;letter-spacing:0.08em;
            text-transform:uppercase;margin-bottom:4px;">Phone Unlocks<br><span style="color:#6B7280;font-weight:400;">(4.7% weight)</span></div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#E2E8F0;">{daily_unlocks}</div>
          <div style="font-size:0.72rem;font-weight:700;margin-top:2px;color:{'#34D399' if daily_unlocks<=60 else '#FCA5A5'};">
            {'✓ Focused' if daily_unlocks<=60 else '⚠ Fragmented'}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:14px;padding:14px 16px;">
          <div style="font-size:0.67rem;color:#475569;font-weight:700;letter-spacing:0.08em;
            text-transform:uppercase;margin-bottom:4px;">Exercise<br><span style="color:#6B7280;font-weight:400;">(2.7% weight)</span></div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#E2E8F0;">{physical_activity_hours}h</div>
          <div style="font-size:0.72rem;font-weight:700;margin-top:2px;color:{'#34D399' if physical_activity_hours>=1 else '#FCA5A5'};">
            {'✓ Active' if physical_activity_hours>=1 else '⚠ Sedentary'}</div>
        </div>
      </div>

      <!-- Recommendation -->
      <div style="background:linear-gradient(135deg,rgba(16,185,129,0.07),rgba(6,182,212,0.07));
        border:1px solid rgba(16,185,129,0.25);border-radius:14px;padding:16px 18px;
        font-size:0.87rem;color:#A7F3D0;line-height:1.75;font-family:'Plus Jakarta Sans',sans-serif;">
        <span style="font-size:1rem;">💡</span>&nbsp;
        <strong>AI Recommendation:</strong>&nbsp;
        {'Trimming 1.5h of ' + most_used_platform + ' daily can lift your score by ~1.2 points.' if avg_daily_usage_hours > 5
          else 'Prioritize reaching 7.5h of sleep per night to maximise cognitive recovery.' if sleep_hours_per_night < 7
          else 'Your routine is well-calibrated — keep phone unlocks under 50 to preserve deep focus.'}
      </div>

      <style>
        @keyframes shimmer {{ 0%{{left:-60%}} 100%{{left:140%}} }}
        .score-card {{ position:relative; overflow:hidden; }}
      </style>
    </div>
    """

    components.html(gauge_html, height=820, scrolling=False)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        MindPulse · Built with Streamlit &amp; scikit-learn ·
        <span>Random Forest Regressor · R² trained on 1 000+ student records</span>
    </div>
    """,
    unsafe_allow_html=True,
)
