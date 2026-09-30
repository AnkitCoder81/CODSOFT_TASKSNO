import streamlit as st

from tictactoe import AI, EMPTY, HUMAN, best_move, game_over, winner

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="⭕")
st.title("⭕ Tic-Tac-Toe AI")
st.caption("You are X. The AI (O) uses Minimax, so it can't be beaten.")

# ---------------- Default settings ----------------
st.session_state.setdefault("ai_first", False)
st.session_state.setdefault("use_pruning", True)


def ai_move():
    move, nodes = best_move(st.session_state.board, st.session_state.use_pruning)
    if move is not None:
        st.session_state.board[move] = AI
        st.session_state.nodes = nodes


def new_game():
    st.session_state.board = [EMPTY] * 9
    st.session_state.nodes = None
    if st.session_state.ai_first:
        ai_move()


def play(i):
    board = st.session_state.board
    if board[i] == EMPTY and not game_over(board):
        board[i] = HUMAN
        if not game_over(board):
            ai_move()


if "board" not in st.session_state:
    new_game()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    st.toggle("AI plays first", key="ai_first")
    st.toggle("Use Alpha-Beta pruning", key="use_pruning")
    st.button("New game", on_click=new_game, use_container_width=True)
    st.caption("Change settings, then press New game.")

# ---------------- Board ----------------
board = st.session_state.board
over = game_over(board)

for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        i = r * 3 + c
        label = board[i] if board[i] != EMPTY else "\u00a0"
        cols[c].button(
            label,
            key=f"cell_{i}",
            on_click=play,
            args=(i,),
            disabled=(board[i] != EMPTY or over),
            use_container_width=True,
        )

# ---------------- Status ----------------
w = winner(board)
if w == AI:
    st.error("AI wins! Try again.")
elif w == HUMAN:
    st.success("You win!")
elif over:
    st.info("It's a draw. That's the best anyone can do against this AI.")
else:
    st.write("Your turn.")

if st.session_state.get("nodes"):
    mode = "with" if st.session_state.use_pruning else "without"
    st.caption(f"AI explored {st.session_state.nodes} positions ({mode} Alpha-Beta pruning).")