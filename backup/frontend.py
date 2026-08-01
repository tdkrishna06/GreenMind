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

    if st.button("Diagnose Plant"):

        image.save("temp.jpg")

        prediction, confidence = predictor.predict("temp.jpg")

        disease_name = CLASS_NAMES.get(prediction, "Unknown Disease")

        st.success("Diagnosis Completed")

        st.write("## 🌱 Disease")
        st.write(disease_name)

        st.write("## 📊 Confidence")
        st.write(f"{confidence * 100:.2f}%")

        remedy = get_remedy(disease_name)

        if remedy:

            st.write("## 🤒 Symptoms")
            for item in remedy.get("symptoms", []):
                st.write("•", item)

            st.write("## 🌿 Traditional Remedies")
            for item in remedy.get("traditional_remedy", []):
                st.write("•", item)

            st.write("## 🛡 Prevention")
            for item in remedy.get("prevention", []):
                st.write("•", item)

        else:
            st.warning("No remedy found for this disease.")

    st.divider()

    st.header("💬 Ask GreenMind AI")

    question = st.text_input(
        "Ask any agriculture question",
        placeholder="Example: How can I control Potato Early Blight naturally?"
    )

    if st.button("Ask GreenMind"):

        if question.strip():

            with st.spinner("Thinking..."):

                try:
                    answer = ask_greenmind(question)
                    st.success(answer)

                except Exception as e:
                    st.error(f"RAG Error: {e}")

        else:
            st.warning("Please enter a question.")