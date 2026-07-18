from ai.mistral_client import ask_ai


def generate_response(messages):
    """
    Sends messages directly to Mistral AI.
    """
    return ask_ai(messages)