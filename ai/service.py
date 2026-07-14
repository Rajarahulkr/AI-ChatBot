from ai.prompts import SYSTEM_PROMPTS
from ai.mistral_client import ask_ai


def generate_response(messages):

    personality = "Default"

    if "personality" in messages[0]:

        personality = messages[0]["personality"]

    system_prompt = SYSTEM_PROMPTS.get(
        personality,
        SYSTEM_PROMPTS["Default"]
    )

    final_messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    for message in messages:

        final_messages.append(

            {
                "role": message["role"],
                "content": message["content"]
            }

        )

    return ask_ai(final_messages)