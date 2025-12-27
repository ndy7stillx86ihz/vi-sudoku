from typing import Optional

from src.game.board import Board


def find_empty_cell(board: Board) -> Optional[tuple[int, int]]:
    for i in range(board.length):
        for j in range(board.length):
            if board.is_empty(i, j):
                return i, j
    return None


def find_empty_cell_smart(board: Board) -> Optional[tuple[int, int]]:
    min_candidates = board.length + 1
    best_cell = None

    for i in range(board.length):
        for j in range(board.length):
            if board.is_empty(i, j):
                valid = get_valid_numbers(board, i, j)
                candidates_count = len(valid)

                if candidates_count < min_candidates:
                    min_candidates = candidates_count
                    best_cell = (i, j)

                    if min_candidates == 1:
                        return best_cell

    return best_cell




def get_valid_numbers(board: Board, row: int, col: int) -> list[int]:
    valid = []
    for num in range(1, board.length + 1):
        if is_valid_placement(board, row, col, num):
            valid.append(num)
    return valid

def is_valid_placement(board: Board, row: int, col: int, num: int) -> bool:
    for j in range(board.length):
        if board.get_cell(row, j) == num:
            return False

    for i in range(board.length):
        if board.get_cell(i, col) == num:
            return False

    chunk_row = row // board.chunk_size
    chunk_col = col // board.chunk_size

    start_row = chunk_row * board.chunk_size
    start_col = chunk_col * board.chunk_size

    for i in range(start_row, start_row + board.chunk_size):
        for j in range(start_col, start_col + board.chunk_size):
            if board.get_cell(i, j) == num:
                return False

    return True