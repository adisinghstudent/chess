import chess

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
