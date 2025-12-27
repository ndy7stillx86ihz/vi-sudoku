import math
from typing import Optional


class Board:
    def __init__(self, length: int = 9, board: list[list[Optional[int]]] = None):
        self.chunk_size = int(math.sqrt(length))
        self.length = self.chunk_size ** 2

        self._board: list[list[Optional[int]]] = \
            [[None for _ in range(length)] for _ in range(length)]

        if board is not None:
            self._board = board

    def get_cell(self, row: int, col: int) -> Optional[int]:
        return self._board[row][col]

    def set_cell(self, row: int, col: int, value: Optional[int]) -> None:
        self._board[row][col] = value

    def is_empty(self, row: int, col: int) -> bool:
        return self._board[row][col] is None

    def copy(self) -> 'Board':
        board_copy = [row[:] for row in self._board]
        return Board(length=self.length, board=board_copy)

    @property
    def is_solved(self) -> bool:
        if not self.is_full:
            return False

        for line in self.lines:
            seen = set()
            for cell in line:
                if cell in seen or cell < 1 or cell > self.length:
                    return False
                seen.add(cell)

        for chunk in self.chunks:
            seen = set()
            for row in chunk:
                for cell in row:
                    if cell in seen or cell < 1 or cell > self.length:
                        return False
                    seen.add(cell)

        return True

    @property
    def board(self):
        return self._board

    @property
    def empty_cells(self) -> list[tuple[int, int]]:
        l: list[tuple[int, int]] = []

        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell is None:
                    l.append((i, j))

        return l

    @property
    def lines(self) -> list[list[Optional[int]]]:
        lines: list[list[Optional[int]]] = []

        for row in self._board:
            lines.append(row)

        for col_idx in range(self.length):
            column = []
            for row_idx in range(self.length):
                column.append(self._board[row_idx][col_idx])
            lines.append(column)

        return lines

    @property
    def chunks(self) -> list[list[list[Optional[int]]]]:
        chunks: list[list[list[Optional[int]]]] = []

        for chunk_row in range(self.chunk_size):
            for chunk_col in range(self.chunk_size):
                chunk: list[list[Optional[int]]] = []

                start_row = chunk_row * self.chunk_size
                start_col = chunk_col * self.chunk_size

                for row_offset in range(self.chunk_size):
                    row_data = []
                    for col_offset in range(self.chunk_size):
                        row_idx = start_row + row_offset
                        col_idx = start_col + col_offset
                        row_data.append(self._board[row_idx][col_idx])
                    chunk.append(row_data)

                chunks.append(chunk)

        return chunks

    @property
    def is_full(self) -> bool:
        return all(cell is not None for row in self._board for cell in row)

    def __getitem__(self, index):
        return self._board[index]

    def __setitem__(self, index, value):
        self._board[index] = value

    def __iter__(self):
        return iter(self._board)

    def __str__(self):
        s: str = ""

        for i, row in enumerate(self._board):

            if i > 0 and i% self.chunk_size == 0:
                s += "-" * ((self.length * 2 + self.length // self.chunk_size - 1) + 1) + "\n"

            for j, cell in enumerate(row):
                if j > 0 and j %self.chunk_size== 0:
                    s += '| '

                s += (str(cell) if cell is not None else '.') + ' '

            s += '\n'

        return f'Board {self.length}x{self.length}\n{"=" * self.length * self.chunk_size}\n\n' + s + '\n'
