from enum import Enum

from util import load_categories


class Color(Enum):
    WHITE = 'w'
    BLACK = 'b'


def render_fen(annotations: dict, meta: dict):
    categories = load_categories()
    move = meta['move_id']
    current_move = Color.WHITE if move % 2 == 0 else Color.BLACK
    pieces = annotations['pieces']
    fen_map = {
        piece['chessboard_position']: categories[piece['category_id']]['fen_id']
        for piece in pieces
    }
    return generate_fen(fen_map, Color.BLACK)


def generate_fen(piece_positions: dict, move: Color = Color.WHITE):
    # Initialize an 8x8 board with all squares set to '1'
    board = [['1' for _ in range(8)] for _ in range(8)]

    # Update the board with the piece positions
    for position, piece in piece_positions.items():
        row = 8 - int(position[1])  # Rows are numbered from 8 to 1
        col = ord(position[0]) - ord('a')  # Columns are labeled 'a' to 'h'
        board[row][col] = piece

    print_board(board)
    # Replace consecutive '1's with their count
    for i in range(8):
        new_row = []
        count = 0
        for j in range(8):
            if board[i][j] == '1':
                count += 1
            else:
                if count > 1:
                    new_row.append(str(count))
                elif count == 1:
                    new_row.append('1')
                new_row.append(board[i][j])
                count = 0
        if count > 1:
            new_row.append(str(count))
        elif count == 1:
            new_row.append('1')

        board[i] = new_row

    # Join each row with '/' to form the final FEN string
    fen = '/'.join(''.join(row) for row in board)
    fen += f' {move.value}'
    return fen


def print_board(board: list[list[str]]):
    """
    Utility for rendering the 8x8 matrix representing the board state
    :param board: list of lists of chess pieces and 1s
    :return:
    """
    for row in board:
        print(row)
