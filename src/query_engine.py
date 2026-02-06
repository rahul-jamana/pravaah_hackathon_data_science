from context_manager import ContextManager
from causal_analysis import explain_conversation

class QueryEngine:
    """
    Handles user queries with context awareness.
    """

    def __init__(self):
        self.context = ContextManager()

    def process_query(self, query, conversation_id=None):
        """
        Processes a user query.
        If conversation_id is provided, resets context.
        Otherwise, uses stored context.
        """

        # Initial query with conversation ID
        if conversation_id:
            explanation = explain_conversation(conversation_id)
            self.context.update(conversation_id, explanation)
            return {
                "query": query,
                "response": explanation
            }

        # Follow-up query (context required)
        if self.context.has_context():
            previous = self.context.get_last_explanation()

            return {
                "query": query,
                "response": {
                    "conversation_id": self.context.get_conversation_id(),
                    "causal_factors": previous["causal_factors"],
                    "evidence": previous["evidence"]
                }
            }

        # No context available
        return {
            "query": query,
            "error": "No prior context available. Please specify a conversation ID."
        }


# ------------------ DEMO ------------------
if __name__ == "__main__":
    engine = QueryEngine()

    # First query (explicit conversation)
    q1 = engine.process_query(
        query="Why did this conversation escalate?",
        conversation_id="6794-8660-4606-3216"
    )
    print("\nQ1 Response:\n", q1)

    # Follow-up query (context-aware)
    q2 = engine.process_query(
        query="Which dialogue turns support this explanation?"
    )
    print("\nQ2 Response:\n", q2)
