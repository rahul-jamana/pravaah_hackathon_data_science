import pandas as pd
from textblob import TextBlob
import os

# ------------------ PATHS ------------------
IN_FILE = "data/processed/conversations.csv"
OUT_FILE = "data/processed/conversations_features.csv"

# ------------------ LOAD DATA ------------------
df = pd.read_csv(IN_FILE)

# ------------------ FEATURE FUNCTIONS ------------------
def get_sentiment(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

ESCALATION_KEYWORDS = [
    "refund",
    "complaint",
    "escalate",
    "manager",
    "cancel",
    "not happy",
    "bad service"
]

def has_escalation_words(text):
    text = str(text).lower()
    return any(word in text for word in ESCALATION_KEYWORDS)

# ------------------ FEATURE ENGINEERING ------------------
df["sentiment"] = df["text"].apply(get_sentiment)
df["is_negative"] = df["sentiment"] < -0.2
df["text_length"] = df["text"].astype(str).apply(len)
df["is_customer"] = df["speaker"].str.lower().eq("customer")
df["contains_escalation_words"] = df["text"].apply(has_escalation_words)

# ------------------ SAVE ------------------
df.to_csv(OUT_FILE, index=False)

print(f"STEP 2 DONE: Features added. Rows = {len(df)}")
