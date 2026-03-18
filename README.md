# Amel.IA – Portuguese Legal Assistant
Amel.IA is designed to simplify access to Portuguese legal information, enabling users to quickly understand laws and regulations without requiring legal expertise.

It is a privacy-focused, open-source AI assistant powered by a locally hosted LLM using LM Studio, combined with a Retrieval-Augmented Generation (RAG) pipeline to deliver accurate answers from official legal sources such as the Diário da República Eletrónico (DRE).

## Key Highlights
- Retrieval-Augmented Generation (RAG) pipeline for grounded legal responses  
- Local LLM deployment using LM Studio (privacy-focused, no external APIs)  
- Integration with official legal sources (Diário da República)  
- End-to-end system: React frontend, Django backend, and containerized databases  
- Embedding-based retrieval for contextual understanding  
- Fully self-hosted architecture (LLM, embeddings, and data storage)

## Purpose
This project was developed as part of a final year bachelor's degree in Data Science. The primary objective was to create a privacy-focused legal chatbot that offers simple, fast, and reliable legal information, while ensuring a modern, accessible user experience.

---

## Features
- **Protected chat environment** (authenticated users only)
- **Dark/Light theme** with persistent settings
- **Conversation history** stored locally per user
- **Natural chat interface** with real-time typing simulation
- **Intent Detection** to handle irrelevant or out-of-context queries
- Fully open-source and **self-hosted LLM** (privacy by design)

---

## Architecture Overview

### Frontend
- React  
- Tailwind CSS  

### Backend
- Django REST Framework  
- LangChain (LLM orchestration & RAG pipeline)  

### AI / LLM
- LM Studio (local LLM hosting)  
- Local embedding models  

### Data & Storage
- Cassandra (legal documents & chat history)  

### Infrastructure
- Docker (database containerization)  
- Poetry (dependency management)  

---

## Local Setup
> This setup assumes you are running the LLM locally and have your backend and database containers ready via Docker.

### 1. Clone the repository
```bash
git clone https://github.com/DiogoR23/ai-assistant-project
cd ai-assistant-project
```

### 2. Start the Frontend
```bash
cd frontend
pnpm install
pnpm run dev
```

### 3. Start the Server
```bash
docker-compose up --build
```
Ensure `.env` files are properly configured with API keys and backend URL

### 4. .env
```bash
# LM-Studio
BASE_URL = ""
OPENAI_API_KEY=""

# Cassandra
PORT = ""
CASSANDRA_USERNAME = ""
CASSANDRA_PASSWORD = ""
CASSANDRA_KEYSPACE = ""

# PostGre SQL
PORT_POSTGRES = ''
POSTGRES_NAME = ''
POSTGRES_USER = ''
POSTGRES_PASS = ''

SECRET_KEY = ""
```

## Authentication
Only authenticated users can access the chatbot. The system supports:
- Register/Login via email and password;
- Persistent session storage using tokens (JWT);
- (Future Work) OAuth via google & password recovery;

## Limitations
- The LLM is hosted locally and may have slower response times
- Lightweight rule-based intent detection system, with planned upgrade to embedding-based intent detection.
- UI currently lacks message editing and advanced error recovery mechanisms

## Future Improvements
- RLHF (Reinforcement Learning from user feedback) for continuous improvement
- Smarter embedding-based intent detection
- Password reset & profile settings
- Editable messages and multi-turn enhancements

## Acknowledgements
- Legal data sourced from the Diário da República Eletrónico (dre.pt)
- LLM stack inspired by open-source RAG pipelines and LangChain examples.

## License
This project is licensed under the MIT License.

## Disclaimer
This project uses publicly available legal data from official sources (Diário da República Eletrónico).  
The information provided is for informational purposes only and should not be considered legal advice.  
Users are responsible for verifying the accuracy and applicability of the content.

## Author
- Diogo Gonçalves Rodrigues
- Bachelor's in Data Science, Catholic University of Portugal - Braga
