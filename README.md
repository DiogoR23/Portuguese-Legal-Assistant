# Amel.IA – Portuguese Legal Assistant

Amel.IA is an open-source AI-powered assistant that provides real-time legal support based on Portuguese law. It leverages a local LLM (Large Language Model) integrated with a Retrieval-Augmented Generation (RAG) pipeline to deliver accurate and trustworthy answers from official legal sources such as the Diário da República Eletrónico (DRE).

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

## Tech Stack

### Frontend
- **React**
- **Tailwind CSS**
- **React Router**
- **Heroicons**

### Backend
- **Python / Django REST Framework**
- **Custom LLM + RAG architecture**
- **Cassandra (for storing legal documents & conversation history)**

### Other Tools
- **Playwright** (web scraping from DRE)
- **BeautifulSoup** (HTML parsing)
- **Docker** (local deployment of backend and database)

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
- Register/Login via username and email;
- Persistent session storage using tokens (JWT);
- (Future Work) OAuth via google & password recovery;

## Limitations

- The LLM is hosted locally and may have slower response times
- Intent detection uses simple keyword logic (to be improved with embeddings)
- UI lacks message editing and full error recovery features

## Future Improvements

- RLHF: Reinforcement Learning with user feedback
- Smarter embedding-based intent detection
- Password reset & profile settings
- Editable messages and multi-turn enhancements

## Acknowledgements

- Special thanks to ChatGPT for assisting in writing documentation and improving interface ideas during the development phase.
- Legal data sourced from the Diário da República Eletrónico (dre.pt)
- LLM stack inspired by open-source RAG pipelines and LangChain examples.

## License

This project is licensed under the MIT License.

## Author

Diogo Gonçalves Rodrigues
Bachelor's in Data Science, Catholic University of Portugal - Braga