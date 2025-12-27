from typing import Optional
from src.game.board import Board
from src.game.utils import is_valid_placement, find_empty_cell


def solve_board(board: Board) -> Optional[Board]:
    board_copy = board.copy()

    if solve_recursive(board_copy):
        return board_copy

    return None


def solve_recursive(board: Board) -> bool:
    empty_cell = find_empty_cell(board)

    if empty_cell is None:
        return True

    row, col = empty_cell

    for num in range(1, board.length + 1):
        if is_valid_placement(board, row, col, num):
            board.set_cell(row, col, num)

            if solve_recursive(board):
                return True

            board.set_cell(row, col, None)

    return False

# #%%
# b = Board(board=[
#     [5,None,4, 6,7,8, 9,1,2],
#     [6,7,2, 1, None,5, 3,4,8],
#     [None,9,8, 3,4,2, 5,6,7],
#     [8,5,9, 7,6,1, 4,2,None],
#     [4,None,6, 8,5,None, 7,9,1],
#     [7,1,3, 9,2,4, 8,None,6],
#     [9,6,1, 5,None,7, 2,None,None],
#     [2,8,7, 4,None,9, None,None,None],
#     [3,4,None, 2,None,6, None,None,None]
# ])
#
# solved = solve_board(b)
# if solved:
#     print(solved)
#     print(f"¿Resuelto? {solved.is_solved}")
# else:
#     print("No tiene solución")