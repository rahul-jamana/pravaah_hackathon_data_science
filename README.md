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
