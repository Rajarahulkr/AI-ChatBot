from mistralai.client import Mistral

from config import MISTRAL_API_KEY, MODEL

client = Mistral(api_key=MISTRAL_API_KEY)


def ask_ai(messages):

    response = client.chat.complete(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content