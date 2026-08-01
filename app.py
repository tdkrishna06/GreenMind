"""
GreenMind AI - AI Powered Plant Disease Diagnosis
====================================================
Bilingual (English / Tamil) Streamlit interface on top of your
existing modular backend:
    - app.diagnosis.predict.DiseasePredictor
    - app.labels.class_names.CLASS_NAMES
    - app.database.remedy_loader.get_remedy

Bilingual behaviour:
    - All fixed UI text (headers, buttons, labels) is translated via
      the TEXT dictionary below.
    - Remedy / class-name content coming from your own database is
      shown in the selected language automatically IF your data is
      stored as {"en": "...", "ta": "..."} dicts (recommended -- see
      the note at the bottom of this file). If your database only
      stores plain English strings, they are shown as-is and the app
      will not crash -- it just won't have a Tamil version for that
      particular field yet.
"""

import os
import tempfile

import streamlit as st
from PIL import Image

from app.diagnosis.predict import DiseasePredictor
from app.labels.class_names import CLASS_NAMES
from app.database.remedy_loader import get_remedy


# =====================================================================
# 1. PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="GreenMind AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================================
# 2. UI TRANSLATION STRINGS
# =====================================================================
TEXT = {
    "title": {"en": "🌿 GreenMind AI", "ta": "🌿 கிரீன்மைண்ட் AI"},
    "subtitle": {"en": "AI Powered Plant Disease Diagnosis", "ta": "AI அடிப்படையிலான தாவர நோய் கண்டறிதல்"},
    "language_label": {"en": "🌐 Language / மொழி", "ta": "🌐 Language / மொழி"},
    "uploader_label": {"en": "Upload Plant Leaf Image", "ta": "தாவர இலை படத்தை பதிவேற்றவும்"},
    "uploaded_caption": {"en": "Uploaded Leaf", "ta": "பதிவேற்றப்பட்ட இலை"},
    "diagnose_button": {"en": "🔍 Diagnose Plant", "ta": "🔍 தாவரத்தை பரிசோதிக்கவும்"},
    "analyzing": {"en": "Analyzing Plant...", "ta": "தாவரத்தை பகுப்பாய்வு செய்கிறது..."},
    "diagnosis_done": {"en": "Diagnosis Completed", "ta": "நோய் கண்டறிதல் முடிந்தது"},
    "disease_header": {"en": "🌱 Disease", "ta": "🌱 நோய்"},
    "confidence_header": {"en": "📊 Confidence", "ta": "📊 நம்பகத்தன்மை"},
    "symptoms_header": {"en": "🦠 Symptoms", "ta": "🦠 அறிகுறிகள்"},
    "remedy_header": {"en": "🌿 Traditional Remedy", "ta": "🌿 பாரம்பரிய தீர்வு"},
    "prevention_header": {"en": "🍀 Prevention", "ta": "🍀 தடுப்பு நடவடிக்கைகள்"},
    "no_remedy": {"en": "No remedy found for this disease.", "ta": "இந்த நோய்க்கு தீர்வு எதுவும் கிடைக்கவில்லை."},
    "analysis_success": {"en": "Plant Analysis Completed Successfully", "ta": "தாவர பகுப்பாய்வு வெற்றிகரமாக முடிந்தது"},
    "no_image_warning": {"en": "Please upload a leaf image first.", "ta": "முதலில் ஒரு இலை படத்தை பதிவேற்றவும்."},
    "unknown_disease": {"en": "Unknown Disease", "ta": "அறியப்படாத நோய்"},
}


def t(key: str, lang: str) -> str:
    """Translate a fixed UI string key."""
    return TEXT.get(key, {}).get(lang, key)


def loc(value, lang: str):
    """
    Translate content coming from CLASS_NAMES / get_remedy().
    Supports three shapes so it never breaks on your existing data:
      - {"en": "...", "ta": "..."}          -> returns value[lang]
      - ["item1", "item2"]                  -> translates each item
      - "plain string"                      -> returned as-is
    """
    if isinstance(value, dict) and ("en" in value or "ta" in value):
        return value.get(lang, value.get("en", ""))
    if isinstance(value, list):
        return [loc(v, lang) for v in value]
    return value


# =====================================================================
# 3. CUSTOM CSS
# =====================================================================
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background-color: #f6faf6; }
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #43a047, #1b5e20); }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================================
# 4. SIDEBAR - LANGUAGE SELECTOR
# =====================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2909/2909769.png", width=90)
    lang_choice = st.radio("🌐 Language / மொழி", ["English", "தமிழ்"], horizontal=True)
    lang = "en" if lang_choice == "English" else "ta"


# =====================================================================
# 5. TITLE
# =====================================================================
st.title(t("title", lang))
st.subheader(t("subtitle", lang))
st.markdown("---")


# =====================================================================
# 6. LOAD AI MODEL (cached so it only loads once per session)
# =====================================================================
@st.cache_resource(show_spinner=False)
def load_predictor():
    return DiseasePredictor()


predictor = load_predictor()


# =====================================================================
# 7. UPLOAD IMAGE
# =====================================================================
uploaded_file = st.file_uploader(t("uploader_label", lang), type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption=t("uploaded_caption", lang), use_container_width=True)


# =====================================================================
# 8. DIAGNOSE
# =====================================================================
if st.button(t("diagnose_button", lang)):

    if image is None:
        st.warning(t("no_image_warning", lang))
    else:
        with st.spinner(t("analyzing", lang)):

            # Save uploaded image temporarily for the predictor
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                    temp_path = temp.name
                    image.save(temp_path)

                # Predict disease
                prediction, confidence = predictor.predict(temp_path)

                # Convert prediction index to disease name (bilingual-aware)
                raw_name = CLASS_NAMES.get(prediction, t("unknown_disease", lang))
                disease_name = loc(raw_name, lang)
                # Remedy lookups are usually keyed by the canonical (English) name
                lookup_name = loc(raw_name, "en") if isinstance(raw_name, dict) else raw_name

                # Get remedy -- try a language-aware call first, fall back gracefully
                try:
                    remedy = get_remedy(lookup_name, lang)
                except TypeError:
                    remedy = get_remedy(lookup_name)

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        st.success(t("diagnosis_done", lang))
        st.markdown("---")

        # -----------------------------
        # Disease
        # -----------------------------
        st.header(t("disease_header", lang))
        st.write(disease_name)

        # -----------------------------
        # Confidence
        # -----------------------------
        st.header(t("confidence_header", lang))
        st.write(f"{confidence * 100:.2f}%")
        st.progress(min(max(confidence, 0.0), 1.0))

        st.markdown("---")

        # -----------------------------
        # Remedy
        # -----------------------------
        if remedy is None:
            st.error(t("no_remedy", lang))
        else:
            symptoms = loc(remedy.get("symptoms", []), lang)
            traditional_remedy = loc(remedy.get("traditional_remedy", []), lang)
            prevention = loc(remedy.get("prevention", []), lang)

            st.header(t("symptoms_header", lang))
            for item in symptoms:
                st.write("•", item)
            st.markdown("---")

            st.header(t("remedy_header", lang))
            for item in traditional_remedy:
                st.write("•", item)
            st.markdown("---")

            st.header(t("prevention_header", lang))
            for item in prevention:
                st.write("•", item)
            st.markdown("---")

            st.success(t("analysis_success", lang))


# =====================================================================
# NOTE ON MAKING YOUR DATABASE FULLY BILINGUAL
# =====================================================================
# For get_remedy() / CLASS_NAMES content to show real Tamil text (not
# just the UI chrome), store each field as a small dict instead of a
# plain string, e.g. in remedy_loader.py:
#
#   "symptoms": [
#       {"en": "Dark concentric-ring spots on leaves",
#        "ta": "இலைகளில் கருமையான வளைய புள்ளிகள்"},
#       ...
#   ]
#
# The loc() helper above already detects this shape automatically and
# will pick the right language -- no other code changes needed. If a
# field is still a plain string, it will simply display in whatever
# language it was written in.