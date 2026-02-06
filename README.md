# Pravaah Hackathon – Causal Analysis over Conversational Data

This project builds a system to analyze multi-turn conversational transcripts
and generate causally grounded explanations for outcome events such as
escalation, complaint, or refund.

## Project Structure

data/        – raw and processed datasets  
src/         – source code  
README.md    – project documentation  
requirements.txt – environment dependencies  

## Step 1 Completed
- JSON preprocessing
- Turn-level conversation extraction
- Clean CSV generation

### Run preprocessing
```bash
python src/preprocess.py


## Step 2: Feature Engineering

### Purpose
The objective of this step is to convert raw conversational turns into
**structured, interpretable features** that reflect speaker behavior,
interaction patterns, and emotional signals.  
These features act as the foundation for downstream causal reasoning.

### Input
- `data/processed/conversations.csv`  
  (Generated after JSON preprocessing in Step 1)

### Output
- `data/processed/conversations_features.csv`

### Engineered Features

Each dialogue turn is enriched with the following attributes:

- **is_customer**  
  Identifies whether the turn is spoken by the customer or the agent.

- **sentiment**  
  A polarity score derived using TextBlob to capture emotional tone.

- **text_length**  
  Length of the utterance, used as a proxy for complaint severity.

- **contains_escalation_words**  
  Flags explicit escalation or complaint-related language.

These features preserve interpretability while enabling rule-based causal analysis.

### Execution

```bash
python src/feature_engineering.py

out put -- STEP 2 DONE: Features added. Rows = 84465



---

## ✅ **STEP 3: CAUSAL ANALYSIS AND EXPLANATION (TASK 1)**

```md
## Step 3: Causal Analysis and Explanation (Task 1)

### Purpose
This step focuses on answering **why** a particular outcome (such as
escalation or unresolved interaction) occurred, rather than predicting
whether it will occur.

The system produces **causally grounded explanations** supported by
explicit dialogue evidence.

### Input
- `data/processed/conversations_features.csv`

### Core Idea
Instead of using black-box models, the system applies
**deterministic causal rules** over conversational features to identify
root causes of interaction outcomes.

### Causal Heuristics Applied

The explanation engine considers multiple interaction-level factors:

- **Customer-dominated conversations**  
  Higher customer effort suggests unresolved concerns.

- **Conversation-level sentiment trend**  
  Sustained neutral-to-negative tone indicates dissatisfaction.

- **Extended interaction length**  
  Longer conversations act as a proxy for friction or failure to resolve issues.

- **Fallback causal rule**  
  Guarantees every conversation yields a grounded explanation without hallucination.

### Output Format

```json
{
  "conversation_id": "6794-8660-4606-3216",
  "causal_factors": [
    "Customer dominated the interaction indicating unresolved concern",
    "Extended interaction length indicating possible issue resolution difficulty"
  ],
  "evidence": [
    {
      "turn_id": 0,
      "speaker": "customer",
      "text": "i need help with my service"
    }
  ]
}

excuation -- python src/causal_analysis.py


## Step 4: Multi-Turn Context-Aware Query Handling (Task 2)

### Objective
Enable the system to support **multi-turn analytical interaction** where
follow-up queries depend on prior system responses, while maintaining
contextual consistency.

### Design Overview
This step introduces a lightweight memory mechanism that:
- Remembers the last referenced conversation
- Stores the causal explanation generated earlier
- Allows follow-up questions without repeating the conversation ID

The implementation is deterministic, interpretable, and evidence-based.

### Components

- **context_manager.py**  
  Maintains conversational state across multiple user queries.

- **query_engine.py**  
  Processes user queries and resolves them using stored context when applicable.

### Example Interaction

**Query 1 (Initial):**

**System Response:**
- Identifies causal factors
- Returns supporting dialogue turns as evidence

**Query 2 (Follow-up):**

**System Behavior:**
- Reuses the previously stored explanation
- Does not require the conversation ID again
- Returns consistent causal factors and evidence

### Sample Output

```json
{
  "conversation_id": "6794-8660-4606-3216",
  "causal_factors": [
    "Overall negative conversational tone over multiple turns",
    "Extended interaction length indicating possible issue resolution difficulty"
  ],
  "evidence": [
    {
      "turn_id": 1,
      "speaker": "Customer",
      "text": "hello im calling about an order that shows delivered but i never received it"
    }
  ]
}
