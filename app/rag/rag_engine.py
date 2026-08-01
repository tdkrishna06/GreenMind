import json
from pathlib import Path

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from ollama import chat


ROOT = Path(__file__).resolve().parents[2]

JSON_FILE = ROOT / "app" / "database" / "remedies.json"

VECTOR_DB = ROOT / "app" / "rag" / "vector_db"


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_database():

    if VECTOR_DB.exists():
        return

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        remedies = json.load(file)

    documents = []

    for disease, info in remedies.items():

        text = f"""
Disease:
{disease}

Symptoms:
{', '.join(info.get('symptoms', []))}

Traditional Remedies:
{', '.join(info.get('traditional_remedy', []))}

Prevention:
{', '.join(info.get('prevention', []))}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "disease": disease
                }
            )
        )


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )


    docs = splitter.split_documents(
        documents
    )


    db = FAISS.from_documents(
        docs,
        embedding
    )


    db.save_local(
        str(VECTOR_DB)
    )



def ask_greenmind(
    disease_name,
    confidence,
    remedy,
    question,
    language="English"
):

    build_database()


    db = FAISS.load_local(
        str(VECTOR_DB),
        embedding,
        allow_dangerous_deserialization=True
    )


    docs = db.similarity_search(
        question,
        k=3
    )


    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )


    remedy_text = ""


    if remedy:

        remedy_text = f"""
Symptoms:
{', '.join(remedy.get('symptoms', []))}

Traditional Remedies:
{', '.join(remedy.get('traditional_remedy', []))}

Prevention:
{', '.join(remedy.get('prevention', []))}
"""


    if language == "Tamil":

        response_language = """
Respond completely in Tamil language.
Use simple Tamil words that farmers can easily understand.
Do not use English unless the technical word is unavoidable.
"""

    else:

        response_language = """
Respond completely in English language.
Use simple agricultural terms that farmers can understand.
"""


    prompt = f"""

You are GreenMind AI, an expert agricultural assistant.

Language Instruction:
{response_language}


Detected Plant Disease:

{disease_name}


AI Prediction Confidence:

{confidence * 100:.2f}%


Disease Information:

{remedy_text}


Retrieved Knowledge:

{context}


Farmer Question:

{question}



Answer Rules:

1. Answer only based on the provided agricultural knowledge.
2. Explain the disease clearly.
3. Provide practical traditional and organic remedies.
4. Provide prevention methods when useful.
5. Keep the response simple and farmer-friendly.
6. Do not create false information.
7. If information is unavailable, say:
"I don't have enough agricultural information."

"""


    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]