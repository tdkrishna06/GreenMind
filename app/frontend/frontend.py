import streamlit as st
from PIL import Image

from app.diagnosis.predict import DiseasePredictor
from app.labels.class_names import CLASS_NAMES
from app.database.remedy_loader import get_remedy

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

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Diagnose Plant"):

        # Save uploaded image
        image.save("temp.jpg")

        # Predict disease
        prediction, confidence = predictor.predict("temp.jpg")

        # Get disease name
        disease_name = CLASS_NAMES.get(prediction, "Unknown Disease")
        st.write("Prediction Number:", prediction)
        st.write("Disease Name:", disease_name)

        st.success("Diagnosis Completed")

        st.write("## 🌱 Disease")
        st.write(disease_name)

        st.write("## 📊 Confidence")
        st.write(f"{confidence * 100:.2f}%")

        # Load remedy
        remedy = get_remedy(disease_name)
        st.write("Remedy:", remedy)
        if remedy:

            st.write("## 🤒 Symptoms")

            for item in remedy["symptoms"]:
                st.write("•", item)

            st.write("## 🌿 Traditional Remedy")

            for item in remedy["traditional_remedy"]:
                st.write("•", item)

            st.write("## 🛡 Prevention")

            for item in remedy["prevention"]:
                st.write("•", item)

        else:
            st.warning("No remedy found for this disease.")