# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# standard
from typing import List

# third party
import pytest

# project
from src.core.bitboard import Bitboard
from src.core.board import Board

@pytest.mark.parametrize(
    "fen, expected_bitboards",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            [
                Bitboard(65280),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(71776119061217280),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976)
            ]
        ),
        (
            "r1bq1b1r/ppp3pp/4k3/3np3/1nB5/2N2Q2/PPPP1PPP/R1B2RK1 b - - 5 9",
            [
                Bitboard(61184),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(33),
                Bitboard(2097152),
                Bitboard(64),
                Bitboard(56013589084897280),
                Bitboard(34393292800),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(17592186044416)
            ]
        )
    ]
)
def test_from_fen(fen: str, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    for piece_type, bitboard in enumerate(test_board.bitboards):
        assert bitboard == expected_bitboards[piece_type]