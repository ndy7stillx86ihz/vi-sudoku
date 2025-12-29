# vi-sudoku

Sudoku CLI game with user interactions based on Vim

```
═════════════════════════════════════
║ 3 │ 5 │ . ║ . │ 6 │ . ║ . │ . │ . ║
-------------------------------------
║ 6 │ . │ 9 ║ . │ . │ . ║ . │ . │ . ║
-------------------------------------
║ . │ 4 │ . ║ . │ 2 │ 1 ║ 6 │ 3 │ . ║
═════════════════════════════════════
║ 1 │ 8 │ . ║ 9 │ . │ . ║ 4 │ . │ 6 ║
-------------------------------------
║ . │ . │ 3 ║ 8 │ 5 │ . ║ . │ 9 │ . ║
-------------------------------------
║ 4 │ . │ 5 ║ . │ 1 │ . ║ 3 │ 8 │ . ║
═════════════════════════════════════
║ 8 │ 3 │ . ║ . │ . │ 6 ║ 7 │ 2 │ . ║
-------------------------------------
║ . │ 1 │ . ║ 4 │ 7 │ . ║ . │ . │ . ║
-------------------------------------
║ . │ . │ . ║ 2 │ 8 │ . ║ 9 │ 1 │ . ║
═════════════════════════════════════
```

## Installation

### Download Pre-built Binary (Recommended)

Download the latest release for your platform from the [Releases page](../../releases):
- **Linux**: `vi-sudoku-linux-amd64`
- **macOS**: `vi-sudoku-macos-amd64`
- **Windows**: `vi-sudoku-windows-amd64.exe`

Make it executable (Linux/macOS):
```sh
chmod +x vi-sudoku-*
./vi-sudoku-*
```

### Run from Source

1. `git clone` this repo and `cd` into the folder

2. install [uv](https://docs.astral.sh/uv/getting-started/installation/)

3. run it

```sh
uv run main.py
```

## Building from Source

To build an executable binary:

1. Install dependencies:
```sh
pip install pyinstaller
```

2. Build the binary:
```sh
pyinstaller vi-sudoku.spec --clean
```

The binary will be available in the `dist/` directory.

## Releases

Releases are automatically created when a new version tag is pushed. The CI/CD pipeline builds binaries for Linux, macOS, and Windows, and attaches them to the GitHub release.

To create a new release:
```sh
git tag v0.1.0
git push origin v0.1.0
```