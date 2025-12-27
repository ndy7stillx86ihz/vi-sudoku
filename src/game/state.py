from typing import Optional
from datetime import datetime, timedelta
from src.game.board import Board


class Move:
    def __init__(self, row: int, col: int, old_value: Optional[int], new_value: Optional[int]):
        self.row = row
        self.col = col
        self.old_value = old_value
        self.new_value = new_value
        self.timestamp = datetime.now()


class GameState:
    def __init__(self, puzzle: Board, solution: Board):
        self.puzzle = puzzle.copy()
        self.current = puzzle.copy()
        self.solution = solution

        self.fixed_cells: set[tuple[int, int]] = set()
        self._populate_fixed_cells()

        self.history: list[Move] = []
        self.redo_stack: list[Move] = []

        self.cursor_row = 0
        self.cursor_col = 0
        self._find_first_empty_cell()

        self.start_time = datetime.now()
        self.elapsed_time = timedelta()
        self.paused = False

        self.errors_count = 0
        self.hints_used = 0

    def _populate_fixed_cells(self):
        for i in range(self.puzzle.length):
            for j in range(self.puzzle.length):
                if not self.puzzle.is_empty(i, j):
                    self.fixed_cells.add((i, j))

    def _find_first_empty_cell(self):
        for i in range(self.current.length):
            for j in range(self.current.length):
                if self.current.is_empty(i, j):
                    self.cursor_row = i
                    self.cursor_col = j
                    return

    def is_cell_fixed(self, row: int, col: int) -> bool:
        return (row, col) in self.fixed_cells

    def is_cell_error(self, row: int, col: int) -> bool:
        current_value = self.current.get_cell(row, col)
        if current_value is None:
            return False

        solution_value = self.solution.get_cell(row, col)
        return current_value != solution_value

    def get_conflicts(self, row: int, col: int) -> list[tuple[int, int]]:
        conflicts = []
        value = self.current.get_cell(row, col)

        if value is None:
            return conflicts

        for j in range(self.current.length):
            if j != col and self.current.get_cell(row, j) == value:
                conflicts.append((row, j))

        for i in range(self.current.length):
            if i != row and self.current.get_cell(i, col) == value:
                conflicts.append((i, col))

        chunk_row = row // self.current.chunk_size
        chunk_col = col // self.current.chunk_size
        start_row = chunk_row * self.current.chunk_size
        start_col = chunk_col * self.current.chunk_size

        for i in range(start_row, start_row + self.current.chunk_size):
            for j in range(start_col, start_col + self.current.chunk_size):
                if (i, j) != (row, col) and self.current.get_cell(i, j) == value:
                    conflicts.append((i, j))

        return list(set(conflicts))

    def set_value(self, row: int, col: int, value: Optional[int]) -> bool:
        if self.is_cell_fixed(row, col):
            return False

        old_value = self.current.get_cell(row, col)
        if old_value == value:
            return False

        move = Move(row, col, old_value, value)
        self.history.append(move)
        self.redo_stack.clear()

        self.current.set_cell(row, col, value)

        if value is not None and self.solution.get_cell(row, col) != value:
            self.errors_count += 1

        return True

    def undo(self) -> bool:
        if not self.history:
            return False

        move = self.history.pop()
        self.redo_stack.append(move)

        self.current.set_cell(move.row, move.col, move.old_value)
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False

        move = self.redo_stack.pop()
        self.history.append(move)

        self.current.set_cell(move.row, move.col, move.new_value)
        return True

    def move_cursor(self, delta_row: int, delta_col: int):
        new_row = (self.cursor_row + delta_row) % self.current.length
        new_col = (self.cursor_col + delta_col) % self.current.length

        self.cursor_row = new_row
        self.cursor_col = new_col

    def get_hint(self) -> bool:
        if self.current.is_empty(self.cursor_row, self.cursor_col):
            solution_value = self.solution.get_cell(self.cursor_row, self.cursor_col)
            self.set_value(self.cursor_row, self.cursor_col, solution_value)
            self.hints_used += 1
            return True
        return False

    def get_candidates(self, row: int, col: int) -> list[int]:
        if not self.current.is_empty(row, col):
            return []

        candidates = []
        for num in range(1, self.current.length + 1):
            valid = True

            for j in range(self.current.length):
                if self.current.get_cell(row, j) == num:
                    valid = False
                    break

            if valid:
                for i in range(self.current.length):
                    if self.current.get_cell(i, col) == num:
                        valid = False
                        break

            if valid:
                chunk_row = row // self.current.chunk_size
                chunk_col = col // self.current.chunk_size
                start_row = chunk_row * self.current.chunk_size
                start_col = chunk_col * self.current.chunk_size

                for i in range(start_row, start_row + self.current.chunk_size):
                    for j in range(start_col, start_col + self.current.chunk_size):
                        if self.current.get_cell(i, j) == num:
                            valid = False
                            break
                    if not valid:
                        break

            if valid:
                candidates.append(num)

        return candidates

    def is_complete(self) -> bool:
        return self.current.is_full

    def is_won(self) -> bool:
        if not self.is_complete():
            return False

        for i in range(self.current.length):
            for j in range(self.current.length):
                if self.current.get_cell(i, j) != self.solution.get_cell(i, j):
                    return False

        return True

    def get_elapsed_time(self) -> timedelta:
        if self.paused:
            return self.elapsed_time
        return self.elapsed_time + (datetime.now() - self.start_time)

    def pause(self):
        if not self.paused:
            self.elapsed_time += (datetime.now() - self.start_time)
            self.paused = True

    def resume(self):
        if self.paused:
            self.start_time = datetime.now()
            self.paused = False

    def get_progress_percentage(self) -> float:
        total_cells = self.current.length ** 2
        filled_cells = total_cells - len(self.current.empty_cells)
        fixed_cells_count = len(self.fixed_cells)

        user_filled = filled_cells - fixed_cells_count
        user_total = total_cells - fixed_cells_count

        if user_total == 0:
            return 100.0

        return (user_filled / user_total) * 100.0