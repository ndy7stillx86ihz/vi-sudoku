#!/bin/bash
# Build script for vi-sudoku binary

set -e

echo "Installing PyInstaller if not already installed..."
pip install --quiet pyinstaller

echo "Building vi-sudoku binary..."
pyinstaller vi-sudoku.spec --clean

echo ""
echo "Build complete! Binary is available at: dist/vi-sudoku"
echo ""
echo "To test the binary, run:"
echo "  ./dist/vi-sudoku"
