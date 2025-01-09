# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# NOTE: This file is tested separately from Perft because
# the pseudo-legal generator and the true-legal generator
# to make debugging easier.

# standard
from typing import List

# third party
import pytest

# project
from src.move_generation.pawn_moves import PawnMoves

from src.core.board import Board
from src.core.move import Move

@pytest.mark.parametrize(
    "fen, expected_moves",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            [
                Move(0,  8, 16), Move(0,  9, 17), Move(0, 10, 18), Move(0, 11, 19),
                Move(0, 12, 20), Move(0, 13, 21), Move(0, 14, 22), Move(0, 15, 23),
                Move(0,  8, 24), Move(0,  9, 25), Move(0, 10, 26), Move(0, 11, 27),
                Move(0, 12, 28), Move(0, 13, 29), Move(0, 14, 30), Move(0, 15, 31)
            ]
        )
    ]
)
def test_white_get_quiet(fen: str, expected_moves: List[Move]) -> None:
    test_board = Board.from_fen(fen)
    generated_moves = PawnMoves.get(test_board)
    assert generated_moves == expected_moves
    
@pytest.mark.parametrize(
    "fen, expected_moves",
    [
        (
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            [
                Move(0, 48, 40), Move(0, 49, 41), Move(0, 50, 42), Move(0, 51, 43),
                Move(0, 52, 44), Move(0, 53, 45), Move(0, 54, 46), Move(0, 55, 47),
                Move(0, 48, 32), Move(0, 49, 33), Move(0, 50, 34), Move(0, 51, 35),
                Move(0, 52, 36), Move(0, 53, 37), Move(0, 54, 38), Move(0, 55, 39)
            ]
        )
    ]
)
def test_black_get_quiet(fen: str, expected_moves: List[Move]) -> None:
    test_board = Board.from_fen(fen)
    generated_moves = PawnMoves.get(test_board)
    assert generated_moves == expected_moves