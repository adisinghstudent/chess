import streamlit as st
import chess
import chess.svg
from io import StringIO
import base64
import random

# Initialize chess board
st.title("chess against my Machine Learning chessbot")

# Initialize the chess board and session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Create AI move function
def ai_move(board, depth=3):
    best_move = get_best_move_alpha_beta(board, depth)
    board.push(best_move)

# Create Minimax and Alpha-Beta pruning logic
def evaluate_board(board):
    if board.is_checkmate():
        return -10000 if board.turn == chess.WHITE else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000}
    
    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                eval += value
            else:
                eval -= value
    
    # Bonus for controlling the center
    central_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
    for square in central_squares:
        if board.is_attacked_by(chess.WHITE, square):
            eval += 10
        if board.is_attacked_by(chess.BLACK, square):
            eval -= 10
    
    # Bonus for piece mobility
    eval += len(list(board.legal_moves)) * 5 if board.turn == chess.WHITE else -len(list(board.legal_moves)) * 5
    
    # Penalty for exposed king
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    eval -= len(board.attackers(chess.BLACK, white_king_square)) * 50
    eval += len(board.attackers(chess.WHITE, black_king_square)) * 50

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
    best_moves = []
    best_move_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
        board.pop()
        if board_value > best_move_value:
            best_move_value = board_value
            best_moves = [move]
        elif board_value == best_move_value:
            best_moves.append(move)
    return random.choice(best_moves)

# Function to render the chess board as SVG and display it in Streamlit
def render_svg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    st.write(html, unsafe_allow_html=True)

# Add this function to check for threefold repetition
def is_threefold_repetition(board):
    return board.is_repetition(3)

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
                # Check for threefold repetition
                if is_threefold_repetition(st.session_state.board):
                    st.write("Threefold repetition detected. The game is a draw.")
                    st.session_state.board.set_result("1/2-1/2")
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
