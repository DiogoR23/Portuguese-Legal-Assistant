# Amel.IA Backend

This is the backend for **Amel.IA**, an open-source intelligent assistant designed to provide real-time legal guidance based on Portuguese legislation. It powers the user authentication system, conversation management, and communication with the local LLM pipeline.

---

## Features

- **JWT-based authentication** (Register, Login, Logout)
- **Conversation storage and history** (Cassandra DB)
- **LLM integration** (via local API or model server)
- **REST API** built with Django REST Framework
- **Protected routes** to secure chat access

---

## Tech Stack

- **Python 3.11**
- **Django 4.x**
- **Django REST Framework**
- **Apache Cassandra** (for fast, scalable NoSQL storage)
- **Simple JWT** (token-based authentication)
- **CORS Headers** (for frontend communication)

---

## Project Structure

```text
backend/
|-- api/                  # Core logic and endpoints
|-- users/                # Authentication and user logic
|-- conversations/        # Conversation model and logic
|-- assistant/            # LLM integration handler
|-- settings.py           # Django settings
|-- urls.py               # Project URL routing
|-- manage.py
```

## Setup Instructions
1. **Clone the Repository**
```bash
git clone https://github.com/DiogoR23/ai-assistant-project/tree/main/backend

cd ai-assistant-project/backend
```

2. **Install Dependencies**

Make sure you have [Poetry](https://python-poetry.org/docs/#ci-recommendations) installed.
```bash
poetry install
```

3. **Activate the Poetry Virtual Environment**
```bash
poetry shell
```

4. **Perform database migrations**

```bash
# PostgreSQL
python3 manage.py migrate
python3 manage.py makemigrations

# Cassandra
python3 manage.py sync_cassandra
```

5. **Run the Development Server**
```bash
python3 manage.py runserver
```

## Cassandra Database

The backend uses Cassandra for storing:
- User Conversations;
- Messages History;

Make sure Cassandra is running and the keyspace/tables are created. You can initialize the schema manually or use CQL scrpit (e.g. `cassandra-init.cql`).

## Authentication

All protected routes use JWT tokens.
- Register: `POST /api/register/`
- Login: `POST /api/token/`
- Refresh token: `POST /api/token/refresh/`
- Access protected endpoints with: `Authorization: Bearer <your_access_token>`

## LLM Integration

The assistant expects a running endpoint that receives a user question and returns a generated legal answer using a local or remote LLM model.
- The generation logic is abstracted in the `assistant/` module.
- Replace or adapt the `generate_response()` function as needed for your model.

## API Endpoints

| Endpoint                   | Method | Description                      |
| -------------------------- | ------ | -------------------------------- |
| `/api/register/`           | POST   | Register a new user              |
| `/api/token/`              | POST   | Login and receive JWT tokens     |
| `/api/token/refresh/`      | POST   | Refresh JWT access token         |
| `/api/conversations/`      | GET    | List all user conversations      |
| `/api/conversations/`      | POST   | Create a new conversation        |
| `/api/conversations/<id>/` | GET    | Get messages from a conversation |
| `/api/send-message/`       | POST   | Send a message to the assistant  |

## License
This project is open-source and available under the **MIT License**.