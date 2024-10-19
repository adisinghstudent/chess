import streamlit as st
import chess
import chess.svg
from io import StringIO
import base64

# Initialize chess board
st.title("Play Chess Against AI")

# Initialize the chess board and session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Create AI move function
def ai_move(board, depth=2):
    best_move = get_best_move_alpha_beta(board, depth)
    board.push(best_move)

# Create Minimax and Alpha-Beta pruning logic (reuse from previous code)
def evaluate_board(board):
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
    eval = 0
    for piece_type in piece_values:
        eval += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        eval -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return eval

def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move_alpha_beta(board, depth):
    best_move = None
    best_move_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
        board.pop()
        if board_value > best_move_value:
            best_move_value = board_value
            best_move = move
    return best_move

# Function to render the chess board as SVG and display it in Streamlit
def render_svg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    st.write(html, unsafe_allow_html=True)

# Display the chess board
board_svg = chess.svg.board(board=st.session_state.board)
render_svg(board_svg)

# Handle human move input
move_input = st.text_input("Enter your move in UCI notation (e.g., e2e4):")

if move_input:
    try:
        # Parse the UCI move input
        move = chess.Move.from_uci(move_input)
        
        # Check if the move is legal
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.write(f"You played: {move_input}")
            
            # After human move, let the AI move
            if not st.session_state.board.is_game_over():
                ai_move(st.session_state.board)
        else:
            st.error("Invalid move. Please enter a valid UCI move.")
    except ValueError as e:
        st.error(f"Error: {e}. Please make sure the move is in UCI format like 'e2e4'.")

# Update the board after moves
board_svg = chess.svg.board(board=st.session_state.board)
render_svg(board_svg)

# Check if the game is over
if st.session_state.board.is_game_over():
    st.write("Game over!")
    result = st.session_state.board.result()
    st.write(f"Result: {result}")
a