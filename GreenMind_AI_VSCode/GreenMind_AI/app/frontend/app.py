"""GreenMind AI Streamlit dashboard."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.database.history import append, read
from app.database.remedy_service import get_remedy, prettify
from app.diagnosis.predictor import DiseasePredictor
from app.utils.image_processing import load_upload
from app.utils.report import create_report
from configs.settings import MAX_UPLOAD_BYTES

st.set_page_config(page_title="GreenMind AI", page_icon="🌿", layout="wide")

CSS = """
<style>
.stApp { background: #f7faf5; color: #193c28; }
.hero { background: linear-gradient(120deg,#174f37,#2e7d4f); color:#fff; padding:2.4rem; border-radius:20px; margin-bottom:1.5rem; }
.hero h1 { margin:0; font-size:2.7rem; } .hero p { font-size:1.12rem; margin:.5rem 0 0; opacity:.92; }
.card { background:#fff; border:1px solid #dbe8db; border-radius:16px; padding:1.2rem; min-height:110px; box-shadow:0 3px 12px #1e402208; }
.metric { color:#1e6a42; font-size:1.8rem; font-weight:700; } .muted { color:#5e7465; }
div[data-testid="stMetric"] { background:#fff; padding:1rem; border-radius:12px; border:1px solid #dbe8db; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def show_list(title: str, items: list[str]) -> None:
    st.markdown(f"#### {title}")
    for item in items:
        st.markdown(f"- {item}")


def render_result(raw: bytes, image, prediction, facts: dict) -> None:
    col_image, col_result = st.columns([1, 1.6], gap="large")
    with col_image:
        st.image(image, caption="Uploaded leaf image", use_container_width=True)
    with col_result:
        st.success("Diagnosis completed")
        st.markdown(f"## {prettify(prediction.label)}")
        st.caption(f"Plant: {facts['plant']} · {facts['scientific_name']}")
        a, b, c = st.columns(3)
        a.metric("Confidence", f"{prediction.confidence:.1%}")
        b.metric("Severity", facts["severity"])
        c.metric("AI time", f"{prediction.inference_seconds:.2f}s")
        st.progress(prediction.confidence, text=f"Model confidence: {prediction.confidence:.1%}")
    st.markdown("### Disease information")
    st.write(facts["description"])
    detail, remedy, prevention = st.columns(3, gap="large")
    with detail:
        show_list("Symptoms", facts["symptoms"])
        st.markdown("#### Likely cause")
        st.write(facts["cause"])
        st.caption(f"Affected parts: {facts['affected_parts']}")
    with remedy:
        show_list("Traditional approach", facts["traditional_remedy"])
        show_list("Organic approach", facts["organic_remedy"])
        st.info(facts["application"])
    with prevention:
        show_list("Prevention", facts["prevention"])
    st.caption(facts["note"])
    chart = pd.DataFrame({"Prediction": [prettify(label) for label, _ in prediction.top_predictions], "Confidence": [score for _, score in prediction.top_predictions]}).set_index("Prediction")
    st.markdown("### Top predictions")
    st.bar_chart(chart, horizontal=True)
    report = create_report(prediction, facts)
    st.download_button("Download PDF report", report, "greenmind_diagnosis_report.pdf", "application/pdf", use_container_width=False)


def main() -> None:
    with st.sidebar:
        st.header("🌿 GreenMind AI")
        page = st.radio("Navigate", ["Diagnose", "History", "About"])
        st.caption("Organic-first decision support")
        st.divider()
        st.caption("AI diagnosis is a screening aid; confirm high-impact decisions locally.")
    if page == "History":
        st.title("Diagnosis history")
        entries = read()
        if entries:
            data = pd.DataFrame(entries)
            data["disease"] = data["label"].map(prettify)
            st.dataframe(data[["timestamp", "disease", "confidence"]], use_container_width=True, hide_index=True)
        else:
            st.info("No diagnoses saved yet. Results remain on this device only.")
        return
    if page == "About":
        st.title("About GreenMind AI")
        st.write("GreenMind AI classifies 38 PlantVillage leaf categories using a ResNet50 model and pairs the result with sustainable, organic-first guidance.")
        st.warning("Image classifications can be wrong. A model result is not a substitute for inspection by an agricultural extension officer, particularly before applying any crop treatment.")
        return
    st.markdown('<section class="hero"><h1>🌿 GreenMind AI</h1><p>AI-powered sustainable plant disease diagnosis — from a leaf photo to practical next steps.</p></section>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    for col, title, body in ((f1, "Fast screening", "ResNet50 diagnosis with top-three probabilities."), (f2, "Sustainable advice", "Traditional and organic-first care guidance."), (f3, "Private history", "Diagnosis history stays in a local JSON file.")):
        col.markdown(f'<div class="card"><h3>{title}</h3><p class="muted">{body}</p></div>', unsafe_allow_html=True)
    st.markdown("### Upload a plant leaf image")
    upload = st.file_uploader("JPG or PNG, up to 10 MB", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if not upload:
        return
    raw = upload.getvalue()
    if len(raw) > MAX_UPLOAD_BYTES:
        st.error("The image is larger than 10 MB. Please choose a smaller file.")
        return
    try:
        image = load_upload(raw)
    except ValueError as exc:
        st.error(str(exc)); return
    st.image(image, caption=f"Ready to diagnose · {image.width} × {image.height}px", width=320)
    if st.button("Diagnose plant", type="primary"):
        with st.spinner("Loading the AI model and examining the leaf…"):
            try:
                prediction = DiseasePredictor().predict(image)
                facts = get_remedy(prediction.label)
                append({"label": prediction.label, "confidence": round(prediction.confidence, 4), "inference_seconds": round(prediction.inference_seconds, 3)})
            except RuntimeError as exc:
                st.error(str(exc)); return
            except Exception:
                st.error("Prediction failed. Please try a clear, well-lit leaf image."); return
        render_result(raw, image, prediction, facts)


if __name__ == "__main__":
    main()
