import sys
import os

# Add GreenMind_AI root directory to Python path
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.append(ROOT_DIR)


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



languages = {

    "English": {

        "title": "🌿 GreenMind AI",

        "subtitle":
        "Plant Disease Diagnosis using Artificial Intelligence",

        "upload":
        "Upload a Plant Leaf Image",

        "analyzing":
        "🌿 GreenMind AI is analyzing the leaf...",

        "complete":
        "Diagnosis Completed Successfully ✅",

        "disease":
        "🌱 Disease Detected",

        "confidence":
        "📊 Confidence",

        "symptoms":
        "🤒 Symptoms",

        "remedies":
        "🌿 Traditional Remedies",

        "prevention":
        "🛡 Prevention",

        "assistant":
        "💬 GreenMind AI Assistant",

        "ask":
        "Ask anything about this disease",

        "button":
        "Ask GreenMind AI",

        "thinking":
        "🤖 GreenMind AI is thinking...",

        "warning":
        "Please enter a question."

    },


    "Tamil": {


        "title":
        "🌿 கிரீன்மைண்ட் AI",


        "subtitle":
        "செயற்கை நுண்ணறிவு மூலம் தாவர நோய் கண்டறிதல்",


        "upload":
        "தாவர இலை படத்தை பதிவேற்றவும்",


        "analyzing":
        "🌿 GreenMind AI இலைப் படத்தை ஆய்வு செய்கிறது...",


        "complete":
        "நோய் கண்டறிதல் வெற்றிகரமாக முடிந்தது ✅",


        "disease":
        "🌱 கண்டறியப்பட்ட நோய்",


        "confidence":
        "📊 நம்பகத்தன்மை",


        "symptoms":
        "🤒 அறிகுறிகள்",


        "remedies":
        "🌿 பாரம்பரிய தீர்வுகள்",


        "prevention":
        "🛡 தடுப்பு முறைகள்",


        "assistant":
        "💬 GreenMind AI உதவியாளர்",


        "ask":
        "இந்த நோய் பற்றி கேள்வி கேளுங்கள்",


        "button":
        "GreenMind AI கேளுங்கள்",


        "thinking":
        "🤖 GreenMind AI யோசிக்கிறது...",


        "warning":
        "தயவுசெய்து கேள்வியை உள்ளிடவும்."

    }

}



language = st.sidebar.selectbox(
    "Language / மொழி",
    [
        "English",
        "Tamil"
    ]
)


text = languages[language]



st.title(
    text["title"]
)


st.subheader(
    text["subtitle"]
)



predictor = DiseasePredictor()



uploaded_file = st.file_uploader(

    text["upload"],

    type=[
        "jpg",
        "jpeg",
        "png"
    ]

)



if uploaded_file:


    image = Image.open(uploaded_file).convert("RGB")


    st.image(

        image,

        caption="Uploaded Image",

        use_container_width=True

    )



    with st.spinner(
        text["analyzing"]
    ):


        image.save(
            "temp.jpg"
        )


        prediction, confidence = predictor.predict(
            "temp.jpg"
        )


        disease_name = CLASS_NAMES.get(
            prediction,
            "Unknown Disease"
        )


        remedy = get_remedy(
            disease_name
        )



    st.success(
        text["complete"]
    )



    st.subheader(
        text["disease"]
    )


    st.success(
        disease_name
    )



    st.subheader(
        text["confidence"]
    )


    st.progress(
        confidence
    )


    st.write(
        f"{confidence*100:.2f}%"
    )



    if remedy:


        st.subheader(
            text["symptoms"]
        )


        for item in remedy.get(
            "symptoms",
            []
        ):

            st.write(
                "•",
                item
            )



        st.subheader(
            text["remedies"]
        )


        for item in remedy.get(
            "traditional_remedy",
            []
        ):

            st.write(
                "•",
                item
            )



        st.subheader(
            text["prevention"]
        )


        for item in remedy.get(
            "prevention",
            []
        ):

            st.write(
                "•",
                item
            )



    st.divider()



    st.header(
        text["assistant"]
    )



    question = st.text_input(
        text["ask"]
    )



    if st.button(
        text["button"]
    ):



        if question.strip():



            with st.spinner(
                text["thinking"]
            ):


                answer = ask_greenmind(

                    disease_name=disease_name,

                    confidence=confidence,

                    remedy=remedy,

                    question=question,

                    language=language

                )



            st.success(
                answer
            )



        else:


            st.warning(
                text["warning"]
            )