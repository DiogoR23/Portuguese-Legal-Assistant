# ai-assistant-project
This project consists in creating an AI Assistant specialized in Portuguese Laws.

Using LLMs and RAGs, this assistant is able to talk about some troubles or answers the user has. With the use of web scraping, this agent got the articles from DRE (Diário República Eletrónico) of Portugal.

This project is running fully local, which means, it's not the fastest one, neither the best one. To use this agent, it is needed to create a `cassandra-docker.yaml` & `docker-compsoe.yaml`, next it is needed to update the `CassandraSession` class.



##  Requirements
```bash
pytest-playwright = "^0.5.1"
cassandra-driver = "^3.29.1"
playwright = "^1.45.0"
beautifulsoup4 = "^4.12.3"
lxml = "^5.2.2"
langchain = {extras = ["all"], version = "^0.2.5"}
jsonpatch = "^1.33"
jsonpointer = "^2.4"
langchain-astradb = "*"
langchain-core = "*"
langchain-openai = "*"
langchain-text-splitters = "*"
langchainhub = "*"
langsmith = "*"
numpy = "*"
openai = "*"
python-dotenv = "*"
requests = "*"
nltk = "*"
tenacity = "*"
langchain-experimental = "^0.0.61"
astrapy = "^1.2.1"
bson = "^0.5.10"
transformers = "^4.41.2"
langchain-huggingface = "^0.0.3"
text-generation = "^0.7.0"
cassio = "^0.1.8"
langchain-community = "^0.2.11"
pyinstall = "*"
flask = "^3.1.0"
django = "^5.1.6"
rank-bm25 = "^0.2.2"
djangorestframework = "^3.15.2"
django-cassandra-engine = "^1.9.0"
django-cors-headers = "^4.7.0"
```
