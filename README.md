# GreenMind
AI-powered sustainable farming assistant
# 🌿 GreenMind AI

### AI-Based Plant Disease Diagnosis and Traditional Remedy Recommendation System

GreenMind AI is an intelligent agricultural assistance system that helps farmers identify plant diseases from leaf images and provides traditional, eco-friendly remedies. The project combines Deep Learning, Computer Vision, Retrieval-Augmented Generation (RAG), and a local Large Language Model (LLM) to deliver accurate disease diagnosis and interactive agricultural guidance.

---

## 📌 Project Overview

Plant diseases significantly reduce crop yield and quality. Farmers often depend on manual inspection or expert consultation, which can be time-consuming and expensive.

GreenMind AI addresses this problem by using Artificial Intelligence to automatically detect plant diseases from uploaded leaf images and recommend traditional treatment methods. The integrated AI assistant also allows farmers to ask follow-up questions in natural language.

---

## 🎯 Objectives

- Detect plant diseases from leaf images using Deep Learning
- Recommend traditional and organic remedies
- Promote sustainable farming practices
- Provide an AI-powered agricultural assistant
- Improve early disease detection and crop management

---

## ✨ Features

- 🌿 Plant disease diagnosis from uploaded leaf images
- 🤖 Deep Learning image classification
- 📊 Prediction confidence score
- 🌱 Traditional and organic remedy recommendation
- 🛡️ Disease prevention guidelines
- 💬 AI chatbot powered by RAG and a local LLM
- 🖥️ Simple and farmer-friendly Streamlit interface
- 🔒 Offline inference using Ollama

---

## 🏗 System Architecture

```
Farmer
  │
  ▼
Upload Leaf Image
  │
  ▼
Image Preprocessing
  │
  ▼
ResNet50 Disease Classification Model
  │
  ▼
Disease Prediction
  │
  ▼
Traditional Remedy Database (JSON)
  │
  ▼
Retrieval-Augmented Generation (RAG)
  │
  ▼
Qwen2.5:3B Local LLM (Ollama)
  │
  ▼
AI Agricultural Assistant
  │
  ▼
Farmer Receives Diagnosis and Guidance
```

---

## 🧠 Technologies Used

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Deep Learning | PyTorch |
| Image Classification | ResNet50 |
| Transformer Library | Hugging Face Transformers |
| Vector Database | FAISS |
| Embedding Model | Sentence Transformers (all-MiniLM-L6-v2) |
| RAG Framework | LangChain |
| Large Language Model | Qwen2.5:3B |
| LLM Runtime | Ollama |
| Database | JSON |
| IDE | Visual Studio Code |
| Operating System | macOS |

---

## 📂 Project Structure

```
GreenMind_AI/
└── app/
    ├── frontend/            # Streamlit user interface
    ├── diagnosis/           # Disease prediction logic
    ├── models/              # AI model loading
    ├── labels/              # Disease class names
    ├── database/
    │   ├── remedies.json
    │   └── ...              # Remedy loader
    ├── rag/                 # Retrieval-Augmented Generation
    ├── utils/               # Image processing
    └── traditional_remedy/
```

---

## ⚙️ Workflow

1. User uploads a plant leaf image.
2. Image is preprocessed.
3. ResNet50 classifies the disease.
4. Disease confidence score is generated.
5. Traditional remedies are retrieved from the JSON database.
6. Relevant information is indexed and retrieved using FAISS.
7. The Qwen2.5:3B LLM generates intelligent responses based on retrieved knowledge.
8. The farmer receives disease diagnosis, remedies, and prevention tips, and can ask additional questions through the chatbot.

---

## 🌱 Traditional Remedy Database

The remedy database is stored as a JSON file. Each disease entry contains:

- **Symptoms**
- **Traditional Remedy**
- **Prevention**

---

## 🤖 RAG-Based AI Assistant

The project uses Retrieval-Augmented Generation (RAG) to improve response quality.

**Pipeline:**

```
User Question
  │
  ▼
Embedding Generation
  │
  ▼
FAISS Vector Search
  │
  ▼
Relevant Agricultural Knowledge Retrieval
  │
  ▼
Context Sent to Qwen2.5:3B
  │
  ▼
Accurate AI Response
```

**Advantages:**

- More reliable responses
- Reduced hallucinations
- Context-aware agricultural guidance
- Local and private execution

---

## 🚀 Installation

**1. Clone the repository:**

```bash
git clone <repository-url>
cd GreenMind_AI
```

**2. Create a virtual environment:**

```bash
python -m venv .venv
```

**3. Activate the environment:**

macOS/Linux:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

**4. Install dependencies:**

```bash
pip install -r requirements.txt
```

**5. Install Ollama and download the model:**

```bash
ollama pull qwen2.5:3b
```

**6. Run the application:**

```bash
streamlit run app/frontend/frontend.py
```

---

## 🔭 Future Enhancements

- Train a custom plant disease classification model
- Support additional crops and diseases
- Mobile application
- Voice-based farmer assistant
- Weather forecasting integration
- Smart irrigation recommendations
- IoT sensor integration
- Multilingual voice interaction

---

## 💡 Benefits

- Early disease detection
- Reduced crop loss
- Eco-friendly farming support
- Easy-to-use interface
- AI-powered agricultural guidance
- Offline LLM support
- Promotes sustainable agriculture

---

## 📝 Conclusion

GreenMind AI demonstrates how Artificial Intelligence, Deep Learning, Computer Vision, Retrieval-Augmented Generation, and Local Large Language Models can work together to assist farmers in disease diagnosis and sustainable crop management. The project provides an intelligent, scalable, and user-friendly solution that contributes to modern precision agriculture.

---

## 👥 Authors

**GreenMind AI Development Team**
Department of Computer Science and Engineering (Artificial Intelligence and Machine Learning)
Anna University
