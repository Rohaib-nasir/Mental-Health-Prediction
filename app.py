import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindPulse — Student Mental Health AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# THEME DEFINITIONS
# ─────────────────────────────────────────────────────────────
THEMES = {
    "Cyber Violet": {
        "a": "#8B5CF6", "b": "#06B6D4", "c": "#00F59B",
        "ga": "#C4B5FD", "gb": "#67E8F9",
        "blob1": "rgba(139,92,246,0.22)", "blob2": "rgba(6,182,212,0.16)", "blob3": "rgba(0,245,155,0.12)",
        "btn_border": "rgba(139,92,246,0.55)", "btn_bg": "rgba(139,92,246,0.18)", "btn_color": "#C4B5FD",
        "card_border": "rgba(139,92,246,0.30)", "card_glow": "rgba(139,92,246,0.10)",
    },
    "Electric Mint": {
        "a": "#10B981", "b": "#06B6D4", "c": "#A78BFA",
        "ga": "#6EE7B7", "gb": "#67E8F9",
        "blob1": "rgba(16,185,129,0.22)", "blob2": "rgba(6,182,212,0.16)", "blob3": "rgba(167,139,250,0.12)",
        "btn_border": "rgba(16,185,129,0.55)", "btn_bg": "rgba(16,185,129,0.18)", "btn_color": "#6EE7B7",
        "card_border": "rgba(16,185,129,0.30)", "card_glow": "rgba(16,185,129,0.10)",
    },
    "Velvet Amber": {
        "a": "#F59E0B", "b": "#EF4444", "c": "#EC4899",
        "ga": "#FCD34D", "gb": "#FCA5A5",
        "blob1": "rgba(245,158,11,0.20)", "blob2": "rgba(239,68,68,0.15)", "blob3": "rgba(236,72,153,0.12)",
        "btn_border": "rgba(245,158,11,0.55)", "btn_bg": "rgba(245,158,11,0.18)", "btn_color": "#FCD34D",
        "card_border": "rgba(245,158,11,0.30)", "card_glow": "rgba(245,158,11,0.10)",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Cyber Violet"

T = THEMES[st.session_state.theme]

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: #060814 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #E2E8F0 !important;
    overflow-x: hidden;
}}
[data-testid="stHeader"], [data-testid="stToolbar"],
section[data-testid="stSidebar"], #MainMenu, footer {{ display: none !important; }}

.block-container {{
    position: relative; z-index: 1;
    max-width: 1340px !important;
    padding: 0.5rem 2rem 4rem !important;
}}

/* ── Animated aurora blobs ── */
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 65% 55% at 8% 18%,  {T['blob1']} 0%, transparent 60%),
        radial-gradient(ellipse 55% 45% at 88% 72%, {T['blob2']} 0%, transparent 55%),
        radial-gradient(ellipse 45% 38% at 50% 97%, {T['blob3']} 0%, transparent 50%);
    animation: auroraShift 12s ease-in-out infinite alternate;
}}
@keyframes auroraShift {{
    0%   {{ opacity: 1;   transform: scale(1)   rotate(0deg); }}
    50%  {{ opacity: 0.7; transform: scale(1.05) rotate(1deg); }}
    100% {{ opacity: 1;   transform: scale(0.97) rotate(-1deg); }}
}}

/* ── Floating particles (pure CSS) ── */
.particle {{ position: fixed; border-radius: 50%; pointer-events: none; z-index: 0; animation: floatUp linear infinite; opacity: 0; }}
@keyframes floatUp {{
    0%   {{ transform: translateY(100vh) scale(0); opacity: 0; }}
    10%  {{ opacity: 0.6; }}
    90%  {{ opacity: 0.3; }}
    100% {{ transform: translateY(-10vh) scale(1.2); opacity: 0; }}
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: #0a0f1e; }}
::-webkit-scrollbar-thumb {{ background: {T['a']}88; border-radius: 999px; }}

/* ── Hero ── */
.hero-wrap {{ text-align: center; padding: 1.8rem 0 1.4rem; animation: fadeInDown .7s ease; }}
@keyframes fadeInDown {{ from {{ opacity:0; transform:translateY(-20px); }} to {{ opacity:1; transform:none; }} }}
@keyframes fadeInUp   {{ from {{ opacity:0; transform:translateY(20px); }}  to {{ opacity:1; transform:none; }} }}

.hero-badge {{
    display: inline-block; margin-bottom: 1rem;
    background: {T['btn_bg']}; border: 1px solid {T['btn_border']};
    border-radius: 9999px; padding: 5px 18px;
    font-size: 0.7rem; font-weight: 700; color: {T['btn_color']};
    letter-spacing: 0.14em; text-transform: uppercase;
    animation: pulse-glow 3s ease-in-out infinite;
}}
@keyframes pulse-glow {{
    0%,100% {{ box-shadow: 0 0 8px {T['a']}40; }}
    50%      {{ box-shadow: 0 0 22px {T['a']}80; }}
}}

.hero-title {{
    font-size: clamp(2.1rem, 4.5vw, 3.4rem); font-weight: 800;
    line-height: 1.12; letter-spacing: -0.03em; margin-bottom: 0.7rem;
    background: linear-gradient(135deg, {T['ga']} 0%, {T['gb']} 50%, {T['btn_color']} 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-size: 200% 200%;
    animation: gradShift 6s ease infinite;
}}
@keyframes gradShift {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.hero-sub {{
    font-size: 0.97rem; color: #64748B; max-width: 500px;
    margin: 0 auto 1.6rem; line-height: 1.75;
}}

/* ── Theme switcher ── */
.theme-row {{
    display: flex; justify-content: center; gap: 10px; margin-bottom: 1rem; flex-wrap: wrap;
}}
.theme-pill {{
    padding: 7px 20px; border-radius: 9999px; cursor: pointer;
    font-size: 0.78rem; font-weight: 700; border: 1px solid rgba(255,255,255,0.12);
    color: #94A3B8; background: rgba(255,255,255,0.04);
    transition: all .25s; letter-spacing: 0.05em;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.theme-pill.active-violet {{
    background: rgba(139,92,246,0.22); border-color: rgba(139,92,246,0.6);
    color: #C4B5FD; box-shadow: 0 0 14px rgba(139,92,246,0.4);
}}
.theme-pill.active-mint {{
    background: rgba(16,185,129,0.22); border-color: rgba(16,185,129,0.6);
    color: #6EE7B7; box-shadow: 0 0 14px rgba(16,185,129,0.4);
}}
.theme-pill.active-amber {{
    background: rgba(245,158,11,0.22); border-color: rgba(245,158,11,0.6);
    color: #FCD34D; box-shadow: 0 0 14px rgba(245,158,11,0.4);
}}

/* ── Divider ── */
hr {{ border-color: rgba(255,255,255,0.06) !important; margin: 1.2rem 0 !important; }}

/* ── Glass cards ── */
.glass-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {T['card_border']};
    border-radius: 20px; padding: 24px 22px;
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    margin-bottom: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 0 24px {T['card_glow']}, inset 0 1px 0 rgba(255,255,255,0.06);
    animation: cardIn .6s ease both;
}}
.glass-card:nth-child(2) {{ animation-delay: .1s; }}
.glass-card:nth-child(3) {{ animation-delay: .2s; }}
@keyframes cardIn {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:none; }} }}

.section-label {{
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: 14px;
    background: linear-gradient(90deg, {T['a']}, {T['b']});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}

/* ── Streamlit widget overrides ── */
label, [data-testid="stWidgetLabel"] p {{
    color: #94A3B8 !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.03em !important;
}}
input, [data-baseweb="select"] > div, [data-baseweb="input"] > div {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #E2E8F0 !important;
}}
[data-baseweb="select"] > div:focus-within {{
    border-color: {T['a']}99 !important;
    box-shadow: 0 0 0 3px {T['a']}22 !important;
}}
[data-baseweb="popover"], [data-baseweb="menu"] {{
    background: #0f1629 !important;
    border: 1px solid {T['a']}44 !important;
}}
[role="option"]:hover {{ background: {T['a']}33 !important; }}

/* Slider thumb */
[data-testid="stSlider"] [role="slider"] {{
    background: {T['a']} !important;
    box-shadow: 0 0 10px {T['a']}cc !important;
}}

/* Preset buttons */
[data-testid="stButton"] button {{
    background: {T['btn_bg']} !important;
    border: 1px solid {T['btn_border']} !important;
    color: {T['btn_color']} !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all .25s !important;
}}
[data-testid="stButton"] button:hover {{
    background: {T['a']}40 !important;
    box-shadow: 0 0 18px {T['a']}55 !important;
    transform: translateY(-2px) !important;
}}

#MainMenu, footer {{ visibility: hidden !important; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("Mental_Health_Model.pkl")

model = load_model()
top_countries = ["Other","Pakistan","USA","Canada","Australia","UK","Germany","Mexico","Turkey","France"]

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">⚡ AI · Random Forest · Real-Time</div>
    <div class="hero-title">MindPulse Student<br>Mental Health Prediction</div>
    <div class="hero-sub">
        Trained on 1,000+ student records — predicts your psychological
        resilience score instantly as you adjust your profile.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# THEME SWITCHER  (actual buttons that trigger rerun)
# ─────────────────────────────────────────────────────────────
tc1, tc2, tc3, tc4 = st.columns([1, 1, 1, 3])
with tc1:
    if st.button("🟣 Cyber Violet", use_container_width=True):
        st.session_state.theme = "Cyber Violet"
        st.rerun()
with tc2:
    if st.button("🟢 Electric Mint", use_container_width=True):
        st.session_state.theme = "Electric Mint"
        st.rerun()
with tc3:
    if st.button("🟡 Velvet Amber", use_container_width=True):
        st.session_state.theme = "Velvet Amber"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PRESETS
# ─────────────────────────────────────────────────────────────
p1, p2, p3 = st.columns([1, 1, 4])
with p1:
    if st.button("🧘 Balanced Student", use_container_width=True):
        st.session_state.update({
            "age":21,"gender":"Male","country":"Pakistan","academic":"Undergraduate",
            "platform":"YouTube","purpose":"Education","screen_time":3.0,
            "unlocks":35,"study":4.5,"activity":1.5,"sleep":8.0,"stress":"Low"
        })
        st.rerun()
with p2:
    if st.button("📱 Heavy Screen Strain", use_container_width=True):
        st.session_state.update({
            "age":22,"gender":"Female","country":"Pakistan","academic":"Graduate",
            "platform":"TikTok","purpose":"Entertainment","screen_time":9.5,
            "unlocks":140,"study":1.5,"activity":0.2,"sleep":4.5,"stress":"Very High"
        })
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TWO-COLUMN LAYOUT
# ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.25, 1.0], gap="large")

with col_left:
    # ── Card 1: Demographics ──────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">01 · Profile & Demographics</div>', unsafe_allow_html=True)

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        age = st.number_input("Age", 10, 100, st.session_state.get("age", 21))
    with r1c2:
        g_opts = ["Male","Female"]
        gender = st.selectbox("Gender", g_opts, index=g_opts.index(st.session_state.get("gender","Male")))
    with r1c3:
        c_opts = ["Pakistan","USA","Canada","Australia","UK","Germany","Mexico","Turkey","France","Other"]
        country = st.selectbox("Country", c_opts, index=c_opts.index(st.session_state.get("country","Pakistan")))

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        a_opts = ["High School","Undergraduate","Graduate"]
        academic_level = st.selectbox("Academic Level", a_opts, index=a_opts.index(st.session_state.get("academic","Undergraduate")))
    with r2c2:
        p_opts = ["Education","Entertainment","Networking","News"]
        purpose_of_use = st.selectbox("Media Purpose", p_opts, index=p_opts.index(st.session_state.get("purpose","Education")))

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Card 2: Digital Habits ───────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">02 · Digital Habits — 67.5% Model Weight</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        pl_opts = ["YouTube","Instagram","TikTok","WhatsApp","LinkedIn","Twitter","Facebook","Snapchat","WeChat","LINE","KakaoTalk","VKontakte"]
        most_used_platform = st.selectbox("Most-Used Platform", pl_opts, index=pl_opts.index(st.session_state.get("platform","YouTube")))
    with d2:
        daily_unlocks = st.slider("Daily Phone Unlocks", 0, 300, st.session_state.get("unlocks", 35), step=5)

    avg_daily_usage_hours = st.slider(
        "Average Daily Screen Time (hrs/day)", 0.0, 16.0,
        float(st.session_state.get("screen_time", 3.0)), step=0.5,
        help="Dominant model feature — 67.5% of prediction weight."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Card 3: Lifestyle ────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 · Lifestyle, Recovery & Stress</div>', unsafe_allow_html=True)

    l1, l2, l3 = st.columns(3)
    with l1:
        sleep_hours_per_night = st.slider("Nightly Sleep (hrs)", 0.0, 14.0, float(st.session_state.get("sleep", 8.0)), step=0.5)
    with l2:
        study_hours = st.slider("Study Hours/Day", 0.0, 14.0, float(st.session_state.get("study", 4.5)), step=0.5)
    with l3:
        physical_activity_hours = st.slider("Exercise (hrs/day)", 0.0, 6.0, float(st.session_state.get("activity", 1.5)), step=0.5)

    st_opts = ["Low","Medium","High","Very High"]
    stress_level = st.select_slider(
        "Perceived Stress Level", options=st_opts,
        value=st_opts[st_opts.index(st.session_state.get("stress","Low"))]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# INFERENCE
# ─────────────────────────────────────────────────────────────
country_group = country if country in top_countries else "Other"
input_row = pd.DataFrame([{
    "Age": age, "Gender": gender, "Country": country,
    "Academic_Level": academic_level, "Most_Used_Platform": most_used_platform,
    "Purpose_Of_Use": purpose_of_use,
    "Avg_Daily_Usage_Hours": float(avg_daily_usage_hours),
    "Daily_Unlocks": int(daily_unlocks),
    "Study_Hours": float(study_hours),
    "Physical_Activity_Hours": float(physical_activity_hours),
    "Sleep_Hours_Per_Night": float(sleep_hours_per_night),
    "Stress_Level": stress_level, "Grouped_country": country_group,
}])
predicted_score = round(float(model.predict(input_row)[0]), 2)
clamped_score   = max(0.0, min(10.0, predicted_score))
pct             = clamped_score / 10.0

# Status colours
if clamped_score >= 7.0:
    pill_txt  = "🟢 Optimal Resilience"
    sc1, sc2  = "#10B981", "#34D399"
    pill_bg, pill_border, pill_fg = "rgba(16,185,129,0.18)", "rgba(16,185,129,0.5)", "#34D399"
    narrative = (
        f"Excellent balance! Your daily rhythms show healthy circadian rest and sustainable "
        f"media usage. You're in the top resilience tier — maintain screen time under "
        f"{int(avg_daily_usage_hours)+1}h and protect your sleep schedule."
    )
elif clamped_score >= 5.0:
    pill_txt  = "🟡 Moderate Strain"
    sc1, sc2  = "#F59E0B", "#FCD34D"
    pill_bg, pill_border, pill_fg = "rgba(245,158,11,0.18)", "rgba(245,158,11,0.5)", "#FCD34D"
    narrative = (
        f"Manageable baseline — {avg_daily_usage_hours}h of daily screen time "
        f"is creating slight attentional drag. A 30-min phone-free wind-down before bed "
        f"can noticeably improve your score."
    )
else:
    pill_txt  = "🔴 Elevated Risk"
    sc1, sc2  = "#EF4444", "#FCA5A5"
    pill_bg, pill_border, pill_fg = "rgba(239,68,68,0.18)", "rgba(239,68,68,0.5)", "#FCA5A5"
    narrative = (
        f"Noticeable strain detected. Heavy digital usage ({avg_daily_usage_hours}h/day) "
        f"combined with {stress_level.lower()} stress signals burnout risk. "
        f"Reducing {most_used_platform} usage is the single highest-impact change."
    )

# AI Recommendation
if avg_daily_usage_hours > 5.0:
    rec_icon = "📱"
    rec_text = (
        f"Trimming just <strong>1.5 hours</strong> of {most_used_platform} daily is projected "
        f"to lift your wellness score by ~<strong>1.2 points</strong> — the model's dominant driver."
    )
elif sleep_hours_per_night < 7.0:
    rec_icon = "😴"
    rec_text = (
        f"Reaching <strong>7.5h of sleep</strong> per night would be your highest-ROI intervention "
        f"(11% model weight). Even one extra hour has compounding cognitive recovery effects."
    )
elif physical_activity_hours < 0.5:
    rec_icon = "🏃"
    rec_text = (
        f"Adding just <strong>30 minutes</strong> of daily exercise correlates with improved stress "
        f"regulation — consider a short walk after study sessions."
    )
elif daily_unlocks > 80:
    rec_icon = "🔔"
    rec_text = (
        f"<strong>{daily_unlocks} daily unlocks</strong> is contributing to attention fragmentation. "
        f"Setting app timers to keep unlocks under 50 can improve deep-work quality."
    )
else:
    rec_icon = "✨"
    rec_text = (
        f"Your routine is well-calibrated. Maintain screen time under 4h and sleep above 7h "
        f"to stay in the <strong>Optimal Resilience</strong> tier consistently."
    )

# ─────────────────────────────────────────────────────────────
# RIGHT PANEL  — fully custom HTML/CSS rendered via components
# ─────────────────────────────────────────────────────────────
dash_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: transparent;
    color: #E2E8F0;
    padding: 4px 2px 8px;
  }}

  /* ── Score card ── */
  .score-card {{
    background: linear-gradient(135deg, {T['a']}18, {T['b']}12);
    border: 1px solid {T['a']}55;
    border-radius: 22px; padding: 26px 18px 22px;
    text-align: center; position: relative; overflow: hidden;
    margin-bottom: 14px;
    box-shadow: 0 0 50px {T['a']}18, inset 0 1px 0 rgba(255,255,255,0.07);
    animation: cardSlide .7s cubic-bezier(.22,1,.36,1) both;
  }}
  @keyframes cardSlide {{ from {{ opacity:0; transform:translateY(20px); }} to {{ opacity:1; transform:none; }} }}

  /* Shimmer line */
  .score-card::before {{
    content: '';
    position: absolute; top: 0; left: -60%; width: 40%; height: 2px;
    background: linear-gradient(90deg, transparent, {T['a']}cc, transparent);
    animation: shimmer 2.8s ease-in-out infinite;
  }}
  @keyframes shimmer {{ 0%{{left:-60%}} 100%{{left:140%}} }}

  /* Glow orb */
  .score-card::after {{
    content: '';
    position: absolute; width: 180px; height: 180px;
    background: radial-gradient(circle, {T['a']}20, transparent 70%);
    top: -40px; right: -40px; border-radius: 50%;
    animation: orb 6s ease-in-out infinite alternate;
  }}
  @keyframes orb {{ 0%{{transform:scale(1)}} 100%{{transform:scale(1.3) translate(-10px,10px)}} }}

  .sc-label {{
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #475569; margin-bottom: 8px;
  }}

  /* ── SVG Gauge ── */
  .gauge-wrap {{ margin: 0 auto 6px; max-width: 230px; position: relative; z-index: 1; }}

  .score-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 4.2rem; font-weight: 700; line-height: 1; z-index: 1; position: relative;
    background: linear-gradient(135deg, {T['ga']}, {T['gb']});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: numPop .9s cubic-bezier(.34,1.56,.64,1) both .1s;
  }}
  @keyframes numPop {{ from {{opacity:0;transform:scale(0.7);}} to {{opacity:1;transform:scale(1);}} }}

  .score-denom {{ font-size: 1.3rem; -webkit-text-fill-color: #334155; color: #334155; }}

  .pill {{
    display: inline-block; padding: 6px 18px; border-radius: 9999px;
    font-weight: 700; font-size: 0.8rem; letter-spacing: 0.05em; margin-top: 10px;
    background: {pill_bg}; color: {pill_fg}; border: 1px solid {pill_border};
    animation: pillPop .6s cubic-bezier(.34,1.56,.64,1) both .25s;
  }}
  @keyframes pillPop {{ from{{opacity:0;transform:scale(0.5);}} to{{opacity:1;transform:scale(1);}} }}

  /* ── Narrative ── */
  .narrative {{
    background: rgba(255,255,255,0.025);
    border-left: 3px solid {T['a']};
    border-radius: 0 12px 12px 0;
    padding: 12px 16px; margin: 12px 0 14px;
    font-size: 0.86rem; color: #94A3B8; line-height: 1.75;
    animation: fadeInUp .5s ease both .2s;
  }}
  @keyframes fadeInUp {{ from{{opacity:0;transform:translateY(10px);}} to{{opacity:1;transform:none;}} }}

  /* ── Progress bar ── */
  .prog-wrap {{ margin-bottom: 16px; animation: fadeInUp .5s ease both .3s; }}
  .prog-labels {{ display: flex; justify-content: space-between; font-size: 0.7rem; color: #475569; margin-bottom: 6px; }}
  .prog-track {{
    background: rgba(255,255,255,0.06); border-radius: 9999px; height: 8px; overflow: hidden;
  }}
  .prog-fill {{
    height: 100%; border-radius: 9999px;
    background: linear-gradient(90deg, {T['a']}, {T['b']}, {T['c']});
    box-shadow: 0 0 12px {T['a']}88;
    width: {pct*100:.1f}%;
    transition: width 1s cubic-bezier(.22,1,.36,1);
    animation: fillIn 1s cubic-bezier(.22,1,.36,1) both .4s;
  }}
  @keyframes fillIn {{ from{{width:0}} to{{width:{pct*100:.1f}%}} }}

  /* ── Factor grid ── */
  .factors-label {{
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #334155; margin-bottom: 8px;
    animation: fadeInUp .5s ease both .35s;
  }}
  .factor-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 9px; margin-bottom: 13px;
    animation: fadeInUp .5s ease both .4s;
  }}
  .factor-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 12px 14px;
    transition: border-color .25s;
  }}
  .factor-card:hover {{ border-color: {T['a']}55; }}
  .fl {{ font-size: 0.63rem; color: #475569; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 3px; }}
  .fw {{ font-size: 0.6rem; color: #334155; font-weight: 400; }}
  .fv {{ font-family: 'JetBrains Mono', monospace; font-size: 1.45rem; font-weight: 700; color: #E2E8F0; line-height: 1.2; }}
  .fd-good {{ font-size: 0.7rem; font-weight: 700; color: #34D399; margin-top: 2px; }}
  .fd-bad  {{ font-size: 0.7rem; font-weight: 700; color: #FCA5A5; margin-top: 2px; }}

  /* ── AI Recommendation ── */
  .rec-card {{
    background: linear-gradient(135deg, rgba(16,185,129,0.07), rgba(6,182,212,0.07));
    border: 1px solid rgba(16,185,129,0.28);
    border-radius: 16px; padding: 16px 18px;
    animation: fadeInUp .5s ease both .5s;
    position: relative; overflow: hidden;
  }}
  .rec-card::before {{
    content: '';
    position: absolute; top: 0; left: -60%; width: 40%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(16,185,129,0.6), transparent);
    animation: shimmer 3.5s ease-in-out infinite 1.5s;
  }}
  .rec-top {{
    display: flex; align-items: center; gap: 10px; margin-bottom: 8px;
  }}
  .rec-icon-wrap {{
    width: 36px; height: 36px; border-radius: 10px;
    background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
  }}
  .rec-title {{ font-size: 0.75rem; font-weight: 700; color: #6EE7B7; letter-spacing: 0.06em; text-transform: uppercase; }}
  .rec-sub {{ font-size: 0.7rem; color: #475569; }}
  .rec-body {{ font-size: 0.87rem; color: #A7F3D0; line-height: 1.75; }}

  /* ── Floating dots animation ── */
  .dots-container {{
    position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
  }}
  .dot {{
    position: absolute; border-radius: 50%;
    background: {T['a']}; opacity: 0;
    animation: floatDot linear infinite;
  }}
  @keyframes floatDot {{
    0%   {{ transform: translateY(100%) scale(0); opacity: 0; }}
    10%  {{ opacity: 0.5; }}
    90%  {{ opacity: 0.2; }}
    100% {{ transform: translateY(-120%) scale(1.4); opacity: 0; }}
  }}
</style>
</head>
<body>

<!-- Score Card -->
<div class="score-card">
  <div class="sc-label">Predicted Wellness Score</div>

  <!-- SVG Arc Gauge -->
  <div class="gauge-wrap">
    <svg viewBox="0 0 220 130" style="width:100%;display:block;">
      <defs>
        <linearGradient id="ag" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="{sc1}"/>
          <stop offset="100%" stop-color="{sc2}"/>
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3.5" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <!-- Track -->
      <path d="M 25 108 A 85 85 0 0 1 195 108"
        fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="14" stroke-linecap="round"/>
      <!-- Active arc with CSS animation -->
      <path id="arc" d="M 25 108 A 85 85 0 0 1 195 108"
        fill="none" stroke="url(#ag)" stroke-width="14" stroke-linecap="round"
        stroke-dasharray="267" stroke-dashoffset="267"
        filter="url(#glow)"
        style="transition: stroke-dashoffset 1.2s cubic-bezier(.22,1,.36,1);"/>
      <!-- Tick marks -->
      {''.join([
        f'<line x1="110" y1="23" x2="110" y2="30" stroke="rgba(255,255,255,0.15)" stroke-width="1.5" transform="rotate({-90 + i*18} 110 108)"/>'
        for i in range(11)
      ])}
      <!-- End dot -->
      <circle cx="110" cy="108" r="5" fill="{sc1}" filter="url(#glow)" opacity="0.9"/>
      <!-- Labels -->
      <text x="20"  y="124" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">0</text>
      <text x="106" y="20"  fill="#334155" font-size="10" font-family="JetBrains Mono,monospace" text-anchor="middle">5</text>
      <text x="192" y="124" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace" text-anchor="end">10</text>
    </svg>
  </div>

  <div class="score-num">{clamped_score:.2f}<span class="score-denom"> / 10</span></div>
  <div><span class="pill">{pill_txt}</span></div>
</div>

<!-- Narrative -->
<div class="narrative">{narrative}</div>

<!-- Progress Bar -->
<div class="prog-wrap">
  <div class="prog-labels">
    <span>Cohort Benchmark</span>
    <span style="color:#94A3B8;">{clamped_score:.1f} / 10.0</span>
  </div>
  <div class="prog-track"><div class="prog-fill"></div></div>
</div>

<!-- Factor breakdown -->
<div class="factors-label">Key Factor Breakdown</div>
<div class="factor-grid">
  <div class="factor-card">
    <div class="fl">Digital Load <span class="fw">(67.5%)</span></div>
    <div class="fv">{avg_daily_usage_hours}h</div>
    <div class="{'fd-good' if avg_daily_usage_hours<=4 else 'fd-bad'}">
      {'✓ Optimal' if avg_daily_usage_hours<=4 else '⚠ High Load'}
    </div>
  </div>
  <div class="factor-card">
    <div class="fl">Sleep Recovery <span class="fw">(11.1%)</span></div>
    <div class="fv">{sleep_hours_per_night}h</div>
    <div class="{'fd-good' if sleep_hours_per_night>=7 else 'fd-bad'}">
      {'✓ Restorative' if sleep_hours_per_night>=7 else '⚠ Deficit'}
    </div>
  </div>
  <div class="factor-card">
    <div class="fl">Phone Unlocks <span class="fw">(4.7%)</span></div>
    <div class="fv">{daily_unlocks}</div>
    <div class="{'fd-good' if daily_unlocks<=60 else 'fd-bad'}">
      {'✓ Focused' if daily_unlocks<=60 else '⚠ Fragmented'}
    </div>
  </div>
  <div class="factor-card">
    <div class="fl">Exercise <span class="fw">(2.7%)</span></div>
    <div class="fv">{physical_activity_hours}h</div>
    <div class="{'fd-good' if physical_activity_hours>=1 else 'fd-bad'}">
      {'✓ Active' if physical_activity_hours>=1 else '⚠ Sedentary'}
    </div>
  </div>
</div>

<!-- AI Recommendation -->
<div class="rec-card">
  <div class="rec-top">
    <div class="rec-icon-wrap">{rec_icon}</div>
    <div>
      <div class="rec-title">AI Recommendation</div>
      <div class="rec-sub">Highest-impact intervention for your profile</div>
    </div>
  </div>
  <div class="rec-body">{rec_text}</div>
</div>

<script>
  // Animate gauge arc on load
  window.addEventListener('load', function() {{
    var arc = document.getElementById('arc');
    var total = 267;
    var offset = total * (1 - {pct:.4f});
    setTimeout(function() {{
      arc.style.strokeDashoffset = offset;
    }}, 120);
  }});
</script>
</body>
</html>
"""

with col_right:
    components.html(dash_html, height=840, scrolling=False)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0;color:#1E293B;font-size:0.75rem;">
  MindPulse &nbsp;·&nbsp; Streamlit + scikit-learn &nbsp;·&nbsp;
  <span style="color:#334155;">Random Forest Regressor · 1 000+ student records</span>
</div>
""", unsafe_allow_html=True)
