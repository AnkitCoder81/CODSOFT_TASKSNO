# Task 1: Rule-Based Chatbot with Groq LLM Fallback

A chatbot that replies using predefined regex rules (if-else style pattern
matching). If no rule matches, the message is sent to a Groq-hosted LLM so the
bot can still answer.

## Features
- Regex-based rules for greetings, time, date, jokes, thanks and goodbye
- Groq LLM fallback (`openai/gpt-oss-120b`) for everything else
- Streamlit chat UI, with a toggle to turn the LLM fallback on or off
- Each reply is labelled as rule-based or Groq LLM
- Also runs in the terminal

## Project structure
```
chatbot.py         # rules + Groq fallback logic (also a terminal chat)
app.py             # Streamlit web UI
requirements.txt
.env.example       # template for your API key
```

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Get a free API key from https://console.groq.com/keys
3. Copy `.env.example` to `.env` and put your key in it:
   ```
   GROQ_API_KEY=your_key_here
   GROQ_MODEL=openai/gpt-oss-120b
   ```
4. Run the web app:
   ```
   streamlit run app.py
   ```
   Or chat in the terminal:
   ```
   python chatbot.py
   ```

## How it works
1. The user message is matched against the regex rules in `RULES` (first match wins).
2. If a rule matches, its predefined reply is returned.
3. Otherwise the message and recent chat history go to the Groq model.

