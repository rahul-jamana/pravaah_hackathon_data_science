class ContextManager:
    """
    Maintains multi-turn query context.
    Stores last referenced conversation and its explanation.
    """

    def __init__(self):
        self.current_conversation_id = None
        self.last_explanation = None

    def update(self, conversation_id, explanation):
        self.current_conversation_id = conversation_id
        self.last_explanation = explanation

    def get_conversation_id(self):
        return self.current_conversation_id

    def get_last_explanation(self):
        return self.last_explanation

    def has_context(self):
        return self.current_conversation_id is not None
