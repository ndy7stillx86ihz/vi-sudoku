from dataclasses import dataclass

from src.consts import Difficulty


@dataclass
class DifficultyScore:
    branch_score: float
    total_score: float
    steps: int
    max_candidates: int
    empty_cells: int
    difficulty: Difficulty
