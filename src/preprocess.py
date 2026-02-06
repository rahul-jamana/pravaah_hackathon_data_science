import json
import pandas as pd
import os
import re

# ------------------ PATHS ------------------
RAW_PATH = "data/raw/Conversational_Transcript_Dataset.json"
OUT_DIR = "data/processed"
OUT_FILE = "conversations.csv"

# ------------------ SETUP ------------------
os.makedirs(OUT_DIR, exist_ok=True)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()

# ------------------ LOAD JSON ------------------
with open(RAW_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ------------------ PROCESS ------------------
rows = []

# Top-level structure: { "transcripts": [ ... ] }
for convo in data["transcripts"]:

    transcript_id = convo.get("transcript_id")
    domain = convo.get("domain")
    intent = convo.get("intent")
    reason_for_call = convo.get("reason_for_call")
    time_of_interaction = convo.get("time_of_interaction")

    # THIS is the correct turns list
    turns = convo.get("conversation")

    if not isinstance(turns, list):
        continue

    for turn_index, turn in enumerate(turns):
        text = turn.get("text")
        speaker = turn.get("speaker")

        if not text or not speaker:
            continue

        rows.append({
            "conversation_id": transcript_id,
            "turn_id": turn_index,
            "speaker": speaker,
            "text": clean_text(text),
            "intent": intent,
            "domain": domain,
            "reason_for_call": reason_for_call,
            "time_of_interaction": time_of_interaction
        })

# ------------------ SAVE ------------------
df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT_DIR, OUT_FILE), index=False)

print(f"STEP 1 DONE: {len(df)} rows written to {OUT_FILE}")


