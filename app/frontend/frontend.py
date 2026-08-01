import streamlit as st
from PIL import Image

from app.diagnosis.predict import DiseasePredictor
from app.labels.class_names import CLASS_NAMES
from app.database.remedy_loader import get_remedy
from app.rag.rag_engine import ask_greenmind

st.set_page_config(
    page_title="GreenMind AI",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 GreenMind AI")
st.subheader("Plant Disease Diagnosis using Artificial Intelligence")

predictor = DiseasePredictor()

uploaded_file = st.file_uploader(
    "Upload a Plant Leaf Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🌿 GreenMind AI is analyzing the leaf..."):

        image.save("temp.jpg")

        prediction, confidence = predictor.predict("temp.jpg")

        disease_name = CLASS_NAMES.get(prediction, "Unknown Disease")

        remedy = get_remedy(disease_name)

    st.success("Diagnosis Completed Successfully ✅")

    st.subheader("🌱 Disease Detected")
    st.success(disease_name)

    st.subheader("📊 Confidence")
    st.progress(confidence)
    st.write(f"{confidence * 100:.2f}%")

    if remedy:

        st.subheader("🤒 Symptoms")

        for item in remedy.get("symptoms", []):
            st.write("•", item)

        st.subheader("🌿 Traditional Remedies")

        for item in remedy.get("traditional_remedy", []):
            st.write("•", item)

        st.subheader("🛡 Prevention")

        for item in remedy.get("prevention", []):
            st.write("•", item)

    st.divider()

    st.header("💬 GreenMind AI Assistant")

    st.info(f"Detected Disease: {disease_name}")

    question = st.text_input(
        "Ask anything about this disease",
        placeholder="Example: Can I use neem oil for this disease?"
    )

    if st.button("Ask GreenMind AI"):

        if question.strip():

            with st.spinner("🤖 GreenMind AI is thinking..."):

                try:

                    answer = ask_greenmind(
                        disease_name=disease_name,
                        confidence=confidence,
                        remedy=remedy,
                        question=question
                    )

                    st.success(answer)

                except Exception as e:

                    st.error(f"RAG Error: {e}")

        else:

            st.warning("Please enter a question.")