from typing import Optional



from src.game.board import Board


def is_valid_board(board: Board) -> bool:
    for line in board.lines:
        if not is_valid_line(line):
            return False

    for chunk in board.chunks:
        if not is_valid_chunk(chunk):
            return False

    return True


def is_valid_line(line: list[Optional[int]]) -> bool:
    if any(cell is None for cell in line):
        return False

    numbers: list[bool] = [False for _ in range(len(line))]

    for v in line:
        if v is not None and ( 0  < v <= len(line)):
            if is_unique_in_list(v, line):
                numbers[v-1] = True

    return all(numbers)


def is_valid_chunk(chunk: list[list[Optional[int]]]) -> bool:
    return is_valid_line(__parse_chunk_to_list(chunk))


def is_unique_in_list(n: Optional[int], l: list[Optional[int]]) -> bool:
    if n is None:
        return False

    repetitions = 0

    for i in l:
        if i is not None and i == n:
            repetitions += 1
        if repetitions > 1:
            return False

    if repetitions == 0:
        return False

    return True


def __parse_chunk_to_list(c: list[list[Optional[int]]]) -> list[Optional[int]]:
    return [cell for row in c for cell in row]


# #%%
# b = [
#     [5,3,4, 6,7,8, 9,1,2],
#     [6,7,2, 1,9,5, 3,4,8],
#     [1,9,8, 3,4,2, 5,6,7],
#
#     [8,5,9, 7,6,1, 4,2,9],
#     [4,2,6, 8,5,3, 7,9,1],
#     [7,1,3, 9,2,4, 8,5,6],
#
#     [9,6,1, 5,3,7, 2,8,4],
#     [2,8,7, 4,1,9, 6,3,5],
#     [3,4,5, 2,8,6, 1,7,9]
# ]
#
# bo = Board(9)
# bo._board = b
#
# print(is_valid_board(bo))