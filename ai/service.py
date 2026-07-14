from ai.mistral_client import ask_ai


def generate_response(prompt: str):
    return ask_ai(prompt)