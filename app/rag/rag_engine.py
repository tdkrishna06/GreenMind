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
                metadata={"disease": disease}
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    db = FAISS.from_documents(
        docs,
        embedding
    )

    db.save_local(str(VECTOR_DB))


def ask_greenmind(
    disease_name,
    confidence,
    remedy,
    question
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
        doc.page_content for doc in docs
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

    prompt = f"""
You are GreenMind AI, an agricultural expert.

Detected Disease:
{disease_name}

Prediction Confidence:
{confidence * 100:.2f}%

Disease Information:
{remedy_text}

Knowledge Retrieved From Database:
{context}

Farmer Question:
{question}

Rules:

1. Answer only using the disease information and retrieved knowledge.
2. Recommend traditional and eco-friendly farming practices whenever possible.
3. Keep the answer simple and practical.
4. If the user asks in Tamil, answer in Tamil.
5. If the answer is unavailable, reply:
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