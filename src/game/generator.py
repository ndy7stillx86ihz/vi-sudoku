import random

from src.consts import Difficulty
from src.game.board import Board
from src.game.model import DifficultyScore
from src.game.solver import is_valid_placement
from src.game.utils import get_valid_numbers, find_empty_cell_smart, find_empty_cell


def generate_puzzle(difficulty: Difficulty = Difficulty.MEDIUM) -> Board:
    board = Board()
    _generate_solved_board_random(board)

# todo: hacerlo dinamico
    removal_targets = {
        Difficulty.EASY: 34,
        Difficulty.MEDIUM: 45,
        Difficulty.HARD: 52,
        Difficulty.EXPERT: 58
    }

    cells_to_remove = removal_targets.get(difficulty)

    removed = 0
    all_cells = [(i, j) for i in range(board.length) for j in range(board.length)]
    random.shuffle(all_cells)

    for row, col in all_cells:
        if removed >= cells_to_remove:
            break

        backup = board.get_cell(row, col)
        board.set_cell(row, col, None)

        if _count_solutions(board, limit=2) == 1:
            removed += 1
        else:
            board.set_cell(row, col, backup)

    return board


def generate_puzzle_symmetric(difficulty: Difficulty = Difficulty.MEDIUM) -> Board:
    board = Board()
    _generate_solved_board_random(board)

    removal_targets = {
        Difficulty.EASY: 1,
        Difficulty.MEDIUM: 44,
        Difficulty.HARD: 52,
        Difficulty.EXPERT: 58
    }

    target = removal_targets.get(difficulty)

    removed = 0
    attempts = 0
    max_attempts = target * 3

    while removed < target and attempts < max_attempts:
        attempts += 1

        row = random.randint(0, board.length - 1)
        col = random.randint(0, board.length - 1)

        if board.is_empty(row, col):
            continue

        sym_row = board.length - 1 - row
        sym_col = board.length - 1 - col

        backup1 = board.get_cell(row, col)
        backup2 = board.get_cell(sym_row, sym_col)

        board.set_cell(row, col, None)

        if row == sym_row and col == sym_col:
            if _count_solutions(board, limit=2) == 1:
                removed += 1
            else:
                board.set_cell(row, col, backup1)
        else:
            board.set_cell(sym_row, sym_col, None)

            if _count_solutions(board, limit=2) == 1:
                removed += 2
            else:
                board.set_cell(row, col, backup1)
                board.set_cell(sym_row, sym_col, backup2)

    return board


def calculate_difficulty_score(board: Board) -> DifficultyScore:
    branch_score_result = [0]
    steps_result = [0]
    max_candidates_result = [0]
    empty_count = len(board.empty_cells)

    board_copy = board.copy()
    success = _solve_with_scoring(board_copy, branch_score_result, steps_result, max_candidates_result)

    if not success:
        return DifficultyScore(
            branch_score=float('inf'),
            total_score=float('inf'),
            steps=0,
            max_candidates=0,
            empty_cells=empty_count,
            difficulty=Difficulty.INHUMAN
        )

    branch_score = branch_score_result[0]
    total_score = branch_score * 100 + empty_count

    if total_score < 100:
        difficulty_label = Difficulty.EASY
    elif total_score < 300:
        difficulty_label = Difficulty.MEDIUM
    elif total_score < 600:
        difficulty_label = Difficulty.HARD
    else:
        difficulty_label = Difficulty.EXPERT

    return DifficultyScore(
        branch_score=branch_score,
        total_score=total_score,
        steps=steps_result[0],
        max_candidates=max_candidates_result[0],
        empty_cells=empty_count,
        difficulty=difficulty_label
    )


def _generate_solved_board_random(board: Board) -> bool:
    empty_cell = find_empty_cell(board)

    if empty_cell is None:
        return True

    row, col = empty_cell

    numbers = list(range(1, board.length + 1))
    random.shuffle(numbers)

    for num in numbers:
        if is_valid_placement(board, row, col, num):
            board.set_cell(row, col, num)

            if _generate_solved_board_random(board):
                return True

            board.set_cell(row, col, None)

    return False


def _count_solutions(board: Board, limit: int = 2) -> int:
    count = [0]

    def solve_count(b: Board):
        if count[0] >= limit:
            return

        empty = find_empty_cell(b)
        if empty is None:
            count[0] += 1
            return

        row, col = empty
        for num in range(1, b.length + 1):
            if is_valid_placement(b, row, col, num):
                b.set_cell(row, col, num)
                solve_count(b)
                b.set_cell(row, col, None)

                if count[0] >= limit:
                    return

    board_copy = board.copy()
    solve_count(board_copy)
    return count[0]


def _solve_with_scoring(board: Board, branch_score: list, steps: list, max_candidates: list) -> bool:
    empty = find_empty_cell_smart(board)

    if empty is None:
        return True

    row, col = empty
    valid_nums = get_valid_numbers(board, row, col)

    steps[0] += 1

    num_candidates = len(valid_nums)
    if num_candidates > max_candidates[0]:
        max_candidates[0] = num_candidates

    if num_candidates > 1:
        branch_score[0] += (num_candidates - 1) ** 2

    for num in valid_nums:
        board.set_cell(row, col, num)

        if _solve_with_scoring(board, branch_score, steps, max_candidates):
            return True

        board.set_cell(row, col, None)

    return False

# #%%
# puzzle_easy = generate_puzzle(Difficulty.EASY)
# puzzle_medium = generate_puzzle(Difficulty.MEDIUM)
# puzzle_hard = generate_puzzle(Difficulty.HARD)
# puzzle_expert = generate_puzzle(Difficulty.EXPERT)
#
# scores = calculate_difficulty_score(puzzle_medium)
#
# for diff in Difficulty:
#     if diff != Difficulty.INHUMAN:
#         p = generate_puzzle(diff)
#         print(p)
#         s = calculate_difficulty_score(p)
#         print(f"{diff.value}: score={s.total_score}")
#%%
# b = generate_puzzle(Difficulty.HARD)
# b.save_compact('puzzle.bin')
#
# # Cargar
# loaded = Board.load_compact('puzzle.bin')
# print(loaded)
#
# # Serializar a bytes (para transmitir)
# data = b.to_compact_bytes()
# print(f"Tamaño: {len(data)} bytes")  # 82 bytes para 9x9
#
# # Deserializar
# restored = Board.from_compact_bytes(data)
#
# # Verificar que son iguales
# for i in range(9):
#     for j in range(9):
#         assert b.get_cell(i, j) == restored.get_cell(i, j)
