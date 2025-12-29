import curses
from src.game.state import GameState
from src.cli.renderer import Renderer


class InputHandler:
    def __init__(self, state: GameState, renderer: Renderer):
        self.state = state
        self.renderer = renderer
        self.running = True
        self.command_mode = False
        self.command_buffer = ""

    def handle_input(self, key: int) -> bool:
        if self.state.is_won():
            if key in [ord('q'), curses.KEY_ENTER, 10, 13]:
                self.running = False
                return True
            return False

        if self.command_mode:
            return self._handle_command_mode(key)

        if key == ord('q'):
            self.running = False
            return True

        elif key == ord(':'):
            self.command_mode = True
            self.command_buffer = ":"
            return True

        elif key == ord('h'):
            self.state.move_cursor(0, -1)
            return True

        elif key == ord('j'):
            self.state.move_cursor(1, 0)
            return True

        elif key == ord('k'):
            self.state.move_cursor(-1, 0)
            return True

        elif key == ord('l'):
            self.state.move_cursor(0, 1)
            return True

        elif key == curses.KEY_LEFT:
            self.state.move_cursor(0, -1)
            return True

        elif key == curses.KEY_DOWN:
            self.state.move_cursor(1, 0)
            return True

        elif key == curses.KEY_UP:
            self.state.move_cursor(-1, 0)
            return True

        elif key == curses.KEY_RIGHT:
            self.state.move_cursor(0, 1)
            return True

        elif key in [ord(str(i)) for i in range(1, 10)]:
            value = key - ord('0')
            self.state.set_value(self.state.cursor_row, self.state.cursor_col, value)
            return True

        elif key in [ord('x'), ord('X'), curses.KEY_DC, curses.KEY_BACKSPACE, 127]:
            self.state.set_value(self.state.cursor_row, self.state.cursor_col, None)
            return True

        elif key == ord('u'):
            self.state.undo()
            return True

        elif key == 18:
            self.state.redo()
            return True

        elif key in [ord('H'), ord('h') | curses.A_ALTCHARSET]:
            self.state.get_hint()
            return True

        elif key == ord('c'):
            self.renderer.toggle_conflicts()
            return True

        elif key == ord('n'):
            self.renderer.toggle_candidates()
            return True

        elif key == ord('p'):
            if self.state.paused:
                self.state.resume()
            else:
                self.state.pause()
            return True

        return False

    def _handle_command_mode(self, key: int) -> bool:
        if key == 27:
            self.command_mode = False
            self.command_buffer = ""
            return True

        elif key in [curses.KEY_ENTER, 10, 13]:
            self._execute_command()
            self.command_mode = False
            self.command_buffer = ""
            return True

        elif key in [curses.KEY_BACKSPACE, 127, 8]:
            if len(self.command_buffer) > 1:
                self.command_buffer = self.command_buffer[:-1]
            else:
                self.command_mode = False
                self.command_buffer = ""
            return True

        elif 32 <= key <= 126:
            self.command_buffer += chr(key)
            return True

        return False

    def _execute_command(self):
        cmd = self.command_buffer.strip()

        if cmd in [':q', ':quit']:
            self.running = False

        elif cmd in [':w', ':write']:
            self._save_game()

        elif cmd in [':wq', ':x']:
            self._save_game()
            self.running = False

        elif cmd == ':hint':
            self.state.get_hint()

        elif cmd == ':undo':
            self.state.undo()

        elif cmd == ':redo':
            self.state.redo()

    def _save_game(self):
        try:
            self.state.current.save_compact('~save')
        except Exception as _:
            pass

    def get_command_buffer(self) -> str:
        return self.command_buffer if self.command_mode else ""

    def is_running(self) -> bool:
        return self.running