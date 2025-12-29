import curses
import sys
from typing import Union, Literal, cast

from src.cli.colors import init_colors
from src.cli.input_handler import InputHandler
from src.cli.renderer import Renderer
from src.game.board import Board
from src.game.generator import generate_puzzle, Difficulty, calculate_difficulty_score
from src.game.state import GameState


def solve_puzzle(puzzle: Board) -> Board:
    from src.game.utils import is_valid_placement, find_empty_cell

    solution = puzzle.copy()

    def solve_recursive(board: Board) -> bool:
        empty = find_empty_cell(board)
        if empty is None:
            return True

        row, col = empty
        for num in range(1, board.length + 1):
            if is_valid_placement(board, row, col, num):
                board.set_cell(row, col, num)
                if solve_recursive(board):
                    return True
                board.set_cell(row, col, None)

        return False

    solve_recursive(solution)
    return solution


def main_menu(stdscr) -> Union[Difficulty, Literal['load'], None]:
    curses.curs_set(0)
    init_colors()

    menu_items = [
        "1. New Game - Easy",
        "2. New Game - Medium",
        "3. New Game - Hard",
        "4. New Game - Expert",
        "5. Load Saved Game",
        "6. Exit"
    ]

    current_selection = 0

    while True:
        stdscr.clear()

        stdscr.addstr(1, 2, "=== VI SUDOKU - MAIN MENU ===", curses.A_BOLD)
        stdscr.addstr(2, 2, "Use j/k or arrows to navigate, Enter to select", curses.A_DIM)

        for idx, item in enumerate(menu_items):
            y = 4 + idx
            if idx == current_selection:
                stdscr.addstr(y, 4, f"> {item}", curses.A_REVERSE)
            else:
                stdscr.addstr(y, 4, f"  {item}")

        stdscr.refresh()

        key = stdscr.getch()

        if key in [ord('j'), curses.KEY_DOWN]:
            current_selection = (current_selection + 1) % len(menu_items)
        elif key in [ord('k'), curses.KEY_UP]:
            current_selection = (current_selection - 1) % len(menu_items)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if current_selection == 0:
                return Difficulty.EASY
            elif current_selection == 1:
                return Difficulty.MEDIUM
            elif current_selection == 2:
                return Difficulty.HARD
            elif current_selection == 3:
                return Difficulty.EXPERT
            elif current_selection == 4:
                return 'load'
            elif current_selection == 5:
                return None
        elif key == ord('q'):
            return None


def game_loop(stdscr, difficulty: Union[Difficulty, Literal['load']]):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(-1)
    init_colors()

    stdscr.clear()
    stdscr.addstr(1, 2, "Generating puzzle...", curses.A_BOLD)
    stdscr.refresh()

    if difficulty == 'load':
        try:
            puzzle = Board.load_compact('~save')
            stdscr.addstr(2, 2, "Solving puzzle to verify...", curses.A_DIM)
            stdscr.refresh()
            solution = solve_puzzle(puzzle)
        except Exception as e:
            stdscr.addstr(3, 2, f"Failed to load game: {e}", curses.color_pair(4))
            stdscr.addstr(4, 2, "Press any key to return to menu...")
            stdscr.refresh()
            stdscr.getch()
            return
    else:
        difficulty_level = cast(Difficulty, difficulty)
        puzzle = generate_puzzle(difficulty_level)

        stdscr.addstr(2, 2, "Calculating difficulty...", curses.A_DIM)
        stdscr.refresh()

        scores = calculate_difficulty_score(puzzle)

        stdscr.addstr(3, 2, f"Difficulty score: {scores.total_score} ({scores.difficulty.value})",
                      curses.A_DIM)
        stdscr.addstr(4, 2, f"Empty cells: {scores.empty_cells}", curses.A_DIM)
        stdscr.refresh()

        stdscr.addstr(6, 2, "Solving puzzle...", curses.A_DIM)
        stdscr.refresh()

        solution = solve_puzzle(puzzle)

    stdscr.addstr(7, 2, "Starting game...", curses.A_BOLD)
    stdscr.refresh()
    curses.napms(500)

    state = GameState(puzzle, solution)
    renderer = Renderer(stdscr, state)
    input_handler = InputHandler(state, renderer)

    renderer.render()

    while input_handler.is_running():
        cmd_buffer = input_handler.get_command_buffer()
        if cmd_buffer:
            try:
                stdscr.addstr(curses.LINES - 1, 0, cmd_buffer)
            except curses.error:
                pass

        stdscr.refresh()

        try:
            key = stdscr.getch()
        except:
            continue

        if key != -1:
            input_handler.handle_input(key)
            renderer.render()


def main(stdscr):
    while True:
        difficulty = main_menu(stdscr)

        if difficulty is None:
            break

        game_loop(stdscr, difficulty)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)