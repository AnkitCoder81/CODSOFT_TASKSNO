# Task 2: Tic-Tac-Toe AI

An AI agent that plays Tic-Tac-Toe against a human using the **Minimax**
algorithm, with optional **Alpha-Beta pruning**. The AI plays perfectly, so the
best a human can do is a draw.

## Features
- Minimax search over the full game tree
- Alpha-Beta pruning (toggle it to compare the number of positions explored)
- Choose whether the human or the AI moves first
- Streamlit web UI, and a terminal version

## How it works
- The AI (O) tries every available move and simulates all possible replies.
- Scores: AI win = +10 minus depth (faster wins are better), human win = depth minus 10, draw = 0.
- The AI picks the move with the highest score, assuming the human always
  plays their best move.
- Alpha-Beta pruning skips branches that cannot change the result. From an
  empty board it explores about 34,000 positions instead of about 550,000.

## Project structure
```
tictactoe.py       # game rules, Minimax + Alpha-Beta, terminal game
app.py             # Streamlit web UI
requirements.txt
```

## Run
```
pip install -r requirements.txt
streamlit run app.py
```
Or play in the terminal:
```
python tictactoe.py
```

## Testing
Every possible human move sequence was simulated against the AI: the human
never won, in both the human-first and AI-first cases.