class MemoryService:

    @staticmethod
    def build_context(messages, max_messages=10):
        """
        Keep only the most recent messages to stay
        within the model's context window.
        """

        if len(messages) <= max_messages:
            return messages

        return messages[-max_messages:]