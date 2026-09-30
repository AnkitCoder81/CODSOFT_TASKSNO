"""
Task 1: Chatbot with rule-based responses (+ Groq LLM fallback)

How it works:
1. Every user message is checked against a list of regex rules (if-else style).
2. If a rule matches, the predefined response is returned (fast, free, predictable).
3. If nothing matches, the message is sent to a Groq LLM so the bot never
   says "I don't understand".

Run in terminal:   python chatbot.py
Run the web UI:    streamlit run app.py
"""

import os
import random
import re
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Change this if Groq retires the model: https://console.groq.com/docs/models
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

SYSTEM_PROMPT = (
    "You are a friendly, concise assistant inside a chatbot project. "
    "Answer clearly in 2-4 sentences unless the user asks for more detail."
)


# --------------------------------------------------------------------------
# 1. RULE-BASED PART
# --------------------------------------------------------------------------
def _time_reply() -> str:
    return f"The current time is {datetime.now().strftime('%I:%M %p')}."


def _date_reply() -> str:
    return f"Today's date is {datetime.now().strftime('%A, %d %B %Y')}."


# Each rule: (regex pattern, list of possible responses OR a function returning str)
# Order matters: the first matching rule wins.
RULES = [
    (r"\b(hi|hello|hey|namaste|good (morning|afternoon|evening))\b",
     ["Hello! How can I help you today?",
      "Hey there! What would you like to talk about?",
      "Hi! Nice to see you."]),

    (r"\bhow are you\b|\bhow('s| is) it going\b",
     ["I'm doing great, thanks for asking! How about you?",
      "All good on my side. What can I do for you?"]),

    (r"\b(your name|who are you)\b",
     ["I'm a simple chatbot that mixes rules with an AI model from Groq."]),

    (r"\bwhat can you do\b|\bhelp\b",
     ["I can chat, tell the time and date, tell jokes, and answer general "
      "questions using an LLM. Try asking me anything!"]),

    (r"\bwhat('s| is)? the time\b|\bcurrent time\b|\btime now\b|\bwhat time\b", _time_reply),
    (r"\b(date|day today|today's date)\b", _date_reply),

    (r"\bjoke\b",
     ["Why do programmers prefer dark mode? Because light attracts bugs.",
      "I would tell you a UDP joke, but you might not get it.",
      "There are 10 kinds of people: those who understand binary and those who don't."]),

    (r"\b(thanks|thank you|thx)\b",
     ["You're welcome!", "Happy to help!", "Anytime!"]),

    (r"\b(bye|goodbye|see you|exit|quit)\b",
     ["Goodbye! Have a great day.", "See you later!"]),
]

COMPILED_RULES = [(re.compile(p, re.IGNORECASE), r) for p, r in RULES]


def rule_based_reply(user_input: str):
    """Return a predefined reply if any rule matches, else None."""
    text = user_input.strip()
    for pattern, response in COMPILED_RULES:
        if pattern.search(text):
            return response() if callable(response) else random.choice(response)
    return None


# --------------------------------------------------------------------------
# 2. GROQ LLM PART
# --------------------------------------------------------------------------
def groq_reply(user_input: str, history=None, api_key=None) -> str:
    """
    Ask a Groq-hosted LLM. `history` is a list of
    {"role": "user"/"assistant", "content": "..."} dicts (optional).
    """
    from groq import Groq  # imported here so rule-only mode works without it

    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        return ("I don't have a rule for that, and no GROQ_API_KEY is set, "
                "so I can't ask the AI model.")

    client = Groq(api_key=api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages += history[-10:]  # keep the last 10 messages for context
    messages.append({"role": "user", "content": user_input})

    try:
        kwargs = {}
        if "gpt-oss" in GROQ_MODEL:
            # reasoning model: keep thinking short so the answer isn't cut off
            kwargs["extra_body"] = {"reasoning_effort": "low"}
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            **kwargs,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:  # network errors, bad key, rate limit, etc.
        return f"Sorry, the AI model had a problem: {e}"


# --------------------------------------------------------------------------
# 3. COMBINED ENTRY POINT
# --------------------------------------------------------------------------
def get_reply(user_input: str, history=None, use_llm=True):
    """Returns (reply_text, source) where source is 'rule' or 'groq'."""
    reply = rule_based_reply(user_input)
    if reply is not None:
        return reply, "rule"
    if use_llm:
        return groq_reply(user_input, history), "groq"
    return "Sorry, I don't understand that yet. Try asking something else.", "rule"


# --------------------------------------------------------------------------
# 4. TERMINAL CHAT
# --------------------------------------------------------------------------
def main():
    print("Chatbot ready! Type 'bye' to quit.\n")
    history = []
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        reply, source = get_reply(user, history)
        print(f"Bot [{source}]: {reply}\n")
        history += [{"role": "user", "content": user},
                    {"role": "assistant", "content": reply}]
        if re.search(r"\b(bye|goodbye|exit|quit)\b", user, re.IGNORECASE):
            break


if __name__ == "__main__":
    main()
