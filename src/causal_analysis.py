import pandas as pd

# ------------------ PATHS ------------------
IN_FILE = "data/processed/conversations_features.csv"

# ------------------ LOAD DATA ------------------
df = pd.read_csv(IN_FILE)

# ------------------ CAUSAL EXPLANATION FUNCTION ------------------
def explain_conversation(conversation_id, top_k=3):
    convo = df[df["conversation_id"] == conversation_id]

    if convo.empty:
        return {
            "conversation_id": conversation_id,
            "error": "Conversation not found"
        }

    reasons = []
    evidence = []

    # ---------------- RULE 1 ----------------
    # Customer speaks more than agent (dominant customer effort)
    customer_turns = convo[convo["is_customer"]]
    agent_turns = convo[~convo["is_customer"]]

    if len(customer_turns) > len(agent_turns):
        reasons.append("Customer dominated the interaction indicating unresolved concern")
        for _, row in customer_turns.head(top_k).iterrows():
            evidence.append({
                "turn_id": int(row["turn_id"]),
                "speaker": row["speaker"],
                "text": row["text"]
            })

    # ---------------- RULE 2 ----------------
    # Repeated sentiment trend (even if not strongly negative)
    if convo["sentiment"].mean() < 0.05:
        reasons.append("Overall negative conversational tone over multiple turns")
        for _, row in customer_turns.head(top_k).iterrows():
            evidence.append({
                "turn_id": int(row["turn_id"]),
                "speaker": row["speaker"],
                "text": row["text"]
            })

    # ---------------- RULE 3 ----------------
    # Long interaction length → friction proxy
    if len(convo) >= 6:
        reasons.append("Extended interaction length indicating possible issue resolution difficulty")
        for _, row in convo.head(top_k).iterrows():
            evidence.append({
                "turn_id": int(row["turn_id"]),
                "speaker": row["speaker"],
                "text": row["text"]
            })

    # ---------------- FALLBACK (GUARANTEED) ----------------
    if not reasons:
        reasons.append("Conversational interaction required multiple exchanges")
        for _, row in convo.head(top_k).iterrows():
            evidence.append({
                "turn_id": int(row["turn_id"]),
                "speaker": row["speaker"],
                "text": row["text"]
            })

    return {
        "conversation_id": conversation_id,
        "causal_factors": list(set(reasons)),
        "evidence": evidence[:top_k]
    }
if __name__ == "__main__":
    # Pick any conversation ID to test
    sample_id = df["conversation_id"].iloc[0]

    result = explain_conversation(sample_id)
    print(result)

