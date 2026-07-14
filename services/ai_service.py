from ai.service import generate_response


class AIService:

    @staticmethod
    def get_response(messages):
        return generate_response(messages)