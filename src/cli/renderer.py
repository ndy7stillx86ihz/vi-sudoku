import curses
from src.game.state import GameState
from src.cli.colors import ColorPairs


class Renderer:
    def __init__(self, stdscr, state: GameState):
        self.stdscr = stdscr
        self.state = state
        self.show_candidates = False
        self.show_conflicts = False

        self.board_start_row = 3
        self.board_start_col = 2

        self.cell_width = 4
        self.cell_height = 2

    def render(self):
        self.stdscr.clear()

        self._render_header()
        self._render_board()
        self._render_info_panel()
        self._render_help()

        self.stdscr.refresh()

    def _render_header(self):
        header = "=== VI SUDOKU ==="
        self.stdscr.addstr(0, 2, header, curses.color_pair(ColorPairs.HEADER) | curses.A_BOLD)

        elapsed = self.state.get_elapsed_time()
        time_str = f"Time: {int(elapsed.total_seconds() // 60):02d}:{int(elapsed.total_seconds() % 60):02d}"
        self.stdscr.addstr(0, 30, time_str, curses.color_pair(ColorPairs.INFO))

    def _render_board(self):
        board = self.state.current
        conflicts_set = set()

        if self.show_conflicts:
            conflicts = self.state.get_conflicts(self.state.cursor_row, self.state.cursor_col)
            conflicts_set = set(conflicts)

        for i in range(board.length):
            for j in range(board.length):
                self._render_cell(i, j, conflicts_set)

        self._render_board_grid()

    def _render_cell(self, row: int, col: int, conflicts_set: set):
        cell_row = self.board_start_row + row * self.cell_height
        cell_col = self.board_start_col + col * self.cell_width

        value = self.state.current.get_cell(row, col)
        is_cursor = (row == self.state.cursor_row and col == self.state.cursor_col)
        is_fixed = self.state.is_cell_fixed(row, col)
        is_error = self.state.is_cell_error(row, col)
        is_conflict = (row, col) in conflicts_set

        if is_error:
            color_pair = ColorPairs.ERROR
            bold = True
        elif is_conflict:
            color_pair = ColorPairs.CONFLICT
            bold = False
        elif is_fixed:
            color_pair = ColorPairs.FIXED
            bold = True
        else:
            color_pair = ColorPairs.NORMAL
            bold = False

        if is_cursor:
            attr = curses.color_pair(ColorPairs.CURSOR) | curses.A_BOLD
        else:
            attr = curses.color_pair(color_pair)
            if bold:
                attr |= curses.A_BOLD

        if value is not None:
            display = str(value)
        else:
            display = '.'

        self.stdscr.addstr(cell_row, cell_col + 1, display, attr)

        if self.show_candidates and value is None and not is_cursor:
            candidates = self.state.get_candidates(row, col)
            if candidates:
                cand_str = ''.join(str(c) for c in candidates[:3])
                self.stdscr.addstr(cell_row + 1, cell_col, cand_str[:3],
                                   curses.color_pair(ColorPairs.CANDIDATE))

    def _render_board_grid(self):
        board = self.state.current

        for i in range(board.length + 1):
            row = self.board_start_row + i * self.cell_height

            if i % board.chunk_size == 0:
                line_char = '═'
                attr = curses.A_NORMAL
            else:
                line_char = '-'
                attr = curses.A_DIM

            line_length = board.length * self.cell_width
            line = line_char * line_length
            try:
                self.stdscr.addstr(row - 1, self.board_start_col, line, attr)
            except curses.error:
                pass

        for j in range(board.length + 1):
            col = self.board_start_col + j * self.cell_width

            if j % board.chunk_size == 0:
                line_char = '║'
                attr = curses.A_NORMAL
            else:
                line_char = '│'
                attr = curses.A_DIM

            for i in range(board.length):
                row = self.board_start_row + i * self.cell_height
                try:
                    self.stdscr.addstr(row, col - 1, line_char, attr)
                except curses.error:
                    pass

    def _render_info_panel(self):
        info_row = self.board_start_row + self.state.current.length * self.cell_height + 2

        progress = self.state.get_progress_percentage()
        elapsed = self.state.get_elapsed_time()

        info_lines = [
            f"Progress: {progress:.1f}%",
            f"Errors: {self.state.errors_count}",
            f"Hints: {self.state.hints_used}",
            f"Moves: {len(self.state.history)}",
        ]

        for i, line in enumerate(info_lines):
            self.stdscr.addstr(info_row + i, self.board_start_col, line,
                               curses.color_pair(ColorPairs.INFO))

        if self.state.is_won():
            win_msg = "*** CONGRATULATIONS! YOU WON! ***"
            time_msg = f"Time: {int(elapsed.total_seconds() // 60):02d}:{int(elapsed.total_seconds() % 60):02d}"
            exit_msg = "Press 'q' or Enter to exit"

            msg_row = info_row + len(info_lines) + 2
            self.stdscr.addstr(msg_row, self.board_start_col, win_msg,
                               curses.color_pair(ColorPairs.HEADER) | curses.A_BOLD | curses.A_BLINK)
            self.stdscr.addstr(msg_row + 1, self.board_start_col, time_msg,
                               curses.color_pair(ColorPairs.INFO) | curses.A_BOLD)
            self.stdscr.addstr(msg_row + 2, self.board_start_col, exit_msg,
                               curses.color_pair(ColorPairs.HEADER) | curses.A_DIM)

    def _render_help(self):
        if self.state.is_won():
            return

        help_row = self.board_start_row + self.state.current.length * self.cell_height + 8

        help_text = [
            "Navigation: h/j/k/l (vim style)",
            "Input: 1-9 to set value, x/Delete to clear",
            "Actions: u=undo, Ctrl+r=redo, H=hint",
            "View: c=toggle conflicts, n=toggle candidates",
            "Quit: q or :q, Save: w or :w"
        ]

        for i, line in enumerate(help_text):
            try:
                self.stdscr.addstr(help_row + i, self.board_start_col, line)
            except curses.error:
                pass

    def toggle_candidates(self):
        self.show_candidates = not self.show_candidates

    def toggle_conflicts(self):
        self.show_conflicts = not self.show_conflicts


