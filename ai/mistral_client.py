from mistralai.client import Mistral

from config import MISTRAL_API_KEY, MODEL
from ai.prompts import SYSTEM_PROMPTS

client = Mistral(api_key=MISTRAL_API_KEY)


def ask_ai(user_message: str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPTS["Normal"]
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.chat.complete(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content