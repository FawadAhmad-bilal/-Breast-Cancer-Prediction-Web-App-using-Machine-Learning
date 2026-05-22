import streamlit as st
import numpy as np
import pickle
import os
from PIL import Image

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Breast Cancer Predictor",
    page_icon="🎗️",
    layout="wide"
)

# =========================================================
# LOAD IMAGE
# =========================================================
IMAGE_PATH = "breast_cancer_banner.png"

image = None
if os.path.exists(IMAGE_PATH):
    image = Image.open(IMAGE_PATH)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: #060816;
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Main Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(236,72,153,0.15), transparent 25%),
        radial-gradient(circle at bottom right, rgba(59,130,246,0.12), transparent 25%),
        linear-gradient(135deg, #050816 0%, #0f172a 100%);
}

/* Main Container */
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

/* HERO SECTION */
.hero-container {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 30px;
    padding: 3rem;
    backdrop-filter: blur(18px);
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

.hero-badge {
    display: inline-block;
    padding: 0.55rem 1.2rem;
    border-radius: 999px;
    background: rgba(236,72,153,0.15);
    color: #ff6eb4;
    border: 1px solid rgba(236,72,153,0.35);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1.1rem;
    line-height: 1.9;
    max-width: 850px;
    margin: auto;
}

/* SECTION TITLE */
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    color: white;
}

/* SLIDER CONTAINER */
div[data-testid="stSlider"] {
    background: rgba(17, 25, 40, 0.75);
    padding: 20px 20px 10px 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    transition: 0.3s ease;
}

/* HOVER EFFECT */
div[data-testid="stSlider"]:hover {
    border: 1px solid rgba(236,72,153,0.35);
    transform: translateY(-2px);
}

/* SLIDER LABEL */
.stSlider label {
    color: white !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}

/* SLIDER BAR */
.stSlider > div > div > div > div {
    background: linear-gradient(
        90deg,
        #ec4899,
        #8b5cf6
    ) !important;
}

/* SLIDER VALUE */
.stSlider span {
    color: #f472b6 !important;
    font-weight: 700 !important;
}

/* SLIDER LABEL */
.stSlider label {
    color: white !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* SLIDER COLOR */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #ec4899, #8b5cf6) !important;
}
/* BUTTON */
.stButton > button {

    width: 100%;
    height: 65px;

    border: none;
    border-radius: 18px;

    background: linear-gradient(
        135deg,
        #ec4899,
        #8b5cf6
    );

    color: white;
    font-size: 20px;
    font-weight: 700;

    transition: 0.3s ease;

    box-shadow:
        0 10px 30px rgba(236,72,153,0.35);

    letter-spacing: 1px;
}

/* BUTTON HOVER */
.stButton > button:hover {

    transform: translateY(-3px) scale(1.02);

    box-shadow:
        0 18px 40px rgba(236,72,153,0.45);

    background: linear-gradient(
        135deg,
        #f472b6,
        #a855f7
    );
}
/* RESULT CARD */
.result-card {

    margin-top: 35px;

    padding: 35px 30px;

    border-radius: 24px;

    text-align: center;

    max-width: 700px;

    margin-left: auto;
    margin-right: auto;

    backdrop-filter: blur(14px);

    animation: fadeIn 0.5s ease;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);
}

/* BENIGN */
.benign-card {

    background: rgba(34,197,94,0.12);

    border: 1px solid rgba(34,197,94,0.35);
}

/* MALIGNANT */
.malignant-card {

    background: rgba(239,68,68,0.12);

    border: 1px solid rgba(239,68,68,0.35);
}

/* RESULT EMOJI */
.result-emoji {

    font-size: 65px;

    margin-bottom: 10px;
}

/* RESULT TITLE */
.result-title {

    font-size: 42px;

    font-weight: 700;

    color: white;

    margin-bottom: 15px;
}

/* RESULT TEXT */
.result-text {

    font-size: 18px;

    color: #e2e8f0;

    line-height: .8;
}
.benign-card {
    background: rgba(34,197,94,0.12);
    border: 2px solid rgba(34,197,94,0.35);
    box-shadow: 0 20px 50px rgba(34,197,94,0.12);
}

.malignant-card {
    background: rgba(239,68,68,0.12);
    border: 2px solid rgba(239,68,68,0.35);
    box-shadow: 0 20px 50px rgba(239,68,68,0.12);
}

.result-emoji {
    font-size: 5rem;
}

.result-title {
    font-size: 3rem;
    font-weight: 700;
    margin-top: 1rem;
}

.result-text {
    color: #e2e8f0;
    line-height: 2;
    margin-top: 1rem;
    font-size: 1.05rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.9);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* METRIC BOX */
.metric-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 1rem;
}

.metric-box h3 {
    margin: 0;
    font-size: 1.8rem;
}

.metric-box p {
    margin: 0;
    color: #cbd5e1;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 5rem;
    padding-bottom: 2rem;
    font-size: 0.95rem;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FEATURE LABELS
# =========================================================
FEATURE_LABELS = {
    "radius_mean": "Average Tumor Radius",
    "texture_mean": "Average Cell Texture",
    "smoothness_mean": "Average Cell Smoothness",
    "compactness_mean": "Average Tumor Compactness",
    "concavity_mean": "Average Tumor Concavity",
    "concave_points_mean": "Average Concave Points",
    "symmetry_mean": "Average Cell Symmetry",

    "radius_se": "Radius Error",
    "compactness_se": "Compactness Error",
    "concavity_se": "Concavity Error",
    "concave_points_se": "Concave Points Error",

    "radius_worst": "Largest Tumor Radius",
    "texture_worst": "Largest Cell Texture",
    "smoothness_worst": "Highest Smoothness",
    "compactness_worst": "Highest Compactness",
    "concavity_worst": "Highest Concavity",
    "concave_points_worst": "Highest Concave Points",
    "symmetry_worst": "Highest Symmetry"
}

# =========================================================
# FEATURE GROUPS
# =========================================================
FEATURE_GROUPS = {
    "📊 Average Measurements": [
        ("radius_mean", 6.981, 28.11, 14.13),
        ("texture_mean", 9.71, 39.28, 19.29),
        ("smoothness_mean", 0.053, 0.163, 0.096),
        ("compactness_mean", 0.019, 0.345, 0.104),
        ("concavity_mean", 0.0, 0.427, 0.089),
        ("concave_points_mean", 0.0, 0.201, 0.049),
        ("symmetry_mean", 0.106, 0.304, 0.181),
    ],

    "🧪 Measurement Errors": [
        ("radius_se", 0.112, 2.873, 0.405),
        ("compactness_se", 0.002, 0.135, 0.025),
        ("concavity_se", 0.0, 0.396, 0.032),
        ("concave_points_se", 0.0, 0.053, 0.012),
    ],

    "⚠️ Highest Recorded Values": [
        ("radius_worst", 7.93, 36.04, 16.27),
        ("texture_worst", 12.02, 49.54, 25.68),
        ("smoothness_worst", 0.071, 0.223, 0.132),
        ("compactness_worst", 0.027, 1.058, 0.254),
        ("concavity_worst", 0.0, 1.252, 0.272),
        ("concave_points_worst", 0.0, 0.291, 0.115),
        ("symmetry_worst", 0.157, 0.664, 0.290),
    ]
}

FEATURE_ORDER = list(FEATURE_LABELS.keys())

# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():

    model_path = "breast_cancer_model (1).pkl"

    if not os.path.exists(model_path):
        st.error("❌ Model file not found.")
        st.stop()

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model

model = load_model()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("🎗️ AI Diagnostic Tool")

    st.markdown("### 📌 About")
    st.write("""
This AI predicts whether a breast tumor is:

- **Benign (Non-Cancerous)**
- **Malignant (Cancerous)**

using machine learning and medical measurements.
""")

    st.markdown("""
<div class="metric-box">
<h3>97.37%</h3>
<p>Model Accuracy</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
if image:
    st.image(image, use_container_width=True)

st.markdown("""
<div class="hero-container">

<div class="hero-badge">
Built By Fawad Ahmad Bilal  · AdaBoost · Machine Learning</div>

<div class="hero-title">
Breast Cancer <span>Predictor</span>
</div>

<div class="hero-subtitle">
Enter the medical measurements below and the AI model will predict
whether the tumor is benign or malignant with high accuracy.
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUTS
# =========================================================
values = {}

for group_name, features in FEATURE_GROUPS.items():

    st.markdown(
        f'<div class="section-title">{group_name}</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, (feat, fmin, fmax, fdef) in enumerate(features):

        with cols[i % 2]:

            values[feat] = st.slider(
                FEATURE_LABELS[feat],
                min_value=float(fmin),
                max_value=float(fmax),
                value=float(fdef),
                step=round((fmax - fmin) / 200, 6),
                key=feat
            )

# =========================================================
# BUTTON
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

_, center, _ = st.columns([1,2,1])

with center:
    clicked = st.button("🔬 Predict Diagnosis")

# =========================================================
# PREDICTION
# =========================================================
if clicked:

    input_array = np.array([
        [values[f] for f in FEATURE_ORDER]
    ])

    prediction = model.predict(input_array)[0]

    probability = model.predict_proba(input_array)[0]

    # confidence = probability[int(prediction)] * 100

    if prediction == 0:

        st.markdown(f"""
<div class="result-card benign-card">

<div class="result-emoji">✅</div>

<div class="result-title">
Benign
</div>

<div class="result-text">

The AI model predicts this tumor is
<strong>non-cancerous</strong>.

<br><br>


<br><br>

<em>Please consult a licensed medical professional.</em>

</div>

</div>
""", unsafe_allow_html=True)

    else:

        st.markdown(f"""
<div class="result-card malignant-card">

<div class="result-emoji">⚠️</div>

<div class="result-title">
Malignant
</div>

<div class="result-text">

The AI model predicts this tumor may be
<strong>cancerous</strong>.

<br><br>

<br><br>

<em>Please seek immediate consultation with a licensed oncologist.</em>

</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
""", unsafe_allow_html=True)