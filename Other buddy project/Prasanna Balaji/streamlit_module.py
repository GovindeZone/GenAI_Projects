import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", page_icon="⭕", layout="centered")

st.title("🎮 Tic Tac Toe")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "current_player" not in st.session_state:
    st.session_state.current_player = "X"

if "winner" not in st.session_state:
    st.session_state.winner = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# Winning combinations
WIN_PATTERNS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def check_winner():
    board = st.session_state.board

    for pattern in WIN_PATTERNS:
        a, b, c = pattern

        if board[a] and board[a] == board[b] == board[c]:
            st.session_state.winner = board[a]
            st.session_state.game_over = True
            return

    # Draw condition
    if "" not in board:
        st.session_state.winner = "Draw"
        st.session_state.game_over = True


def make_move(index):
    if (
        st.session_state.board[index] == ""
        and not st.session_state.game_over
    ):
        st.session_state.board[index] = st.session_state.current_player

        check_winner()

        if not st.session_state.game_over:
            st.session_state.current_player = (
                "O"
                if st.session_state.current_player == "X"
                else "X"
            )


# Display status
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.info("🤝 It's a Draw!")
    else:
        st.success(f"🏆 Player {st.session_state.winner} Wins!")
else:
    st.write(f"### Current Turn: {st.session_state.current_player}")


# Create 3x3 grid
for row in range(3):
    cols = st.columns(3)

    for col in range(3):
        idx = row * 3 + col

        with cols[col]:
            st.button(
                st.session_state.board[idx] or " ",
                key=idx,
                on_click=make_move,
                args=(idx,),
                use_container_width=True,
            )


# Reset button
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False


st.divider()

if st.button("🔄 Restart Game", use_container_width=True):
    reset_game()