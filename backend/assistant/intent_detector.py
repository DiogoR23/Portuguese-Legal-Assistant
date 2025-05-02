"""
intent_detector.py

This module defines the IntentDetector class, which is responsible for detecting the intent of user input.

The class uses a set of predefined keywords and patterns to classify the input into different categories:
- Greeting: Identifies if the user is greeting the assistant.
- Legal Query: Identifies if the user is asking a legal question or seeking legal information.
- Unknown: If the input does not match any known patterns or keywords, it is classified as unknown.

The detect method takes a user input string and returns the detected intent as a string.

The class is used in the get_ai_response function to classify user input before generating a response.
"""
import re

class IntentDetector:
    def __init__(self):
        self.greetings = [
            'olá', 'bom dia', 'boa tarde', 'boa noite', 'tudo bem', 'oi', 'boas', 'ola'
        ]

        self.legal_keywords = [
            "artigo", "lei", "código", "direito", "obrigação", "contrato", "responsabilidade",
            "testamento", "herança", "divórcio", "casamento", "sucessão", "penal", "civil",
            "trabalho", "constituição", "empresa", "negócio", "sociedade", "tributário", "impostos"
        ]

        self.legal_patterns = [
            r"qual.*direito", r"é permitido", r"é proibido", r"posso.*", r"quais.*obrigações",
            r"quais.*direitos", r"como funciona.*", r"o que diz.*lei", r"como proceder.*",
            r"como abrir.*empresa", r"abrir.*negócio"
        ]

    def detect(self, user_input: str) -> str:
        user_input_lower = user_input.lower()

        greeting_score = 0
        legal_score = 0

        if any(greet in user_input_lower for greet in self.greetings):
            greeting_score += 1

        if any(keyword in user_input_lower for keyword in self.legal_keywords):
            legal_score += 1

        if any(re.search(pattern, user_input_lower) for pattern in self.legal_patterns):
            legal_score += 2

        if legal_score > greeting_score and legal_score > 0:
            return "legal_query"

        elif greeting_score > 0 and legal_score == 0:
            return "greeting"

        else:
            return "unknown"