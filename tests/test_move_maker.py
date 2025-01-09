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
from src.core.move_maker import MoveMaker
from src.core.bitboard import Bitboard
from src.core.board import Board
from src.core.move import Move, Flags
from src.core import squares

@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            Move(Flags.QUIET, squares.E2, squares.E4),
            [
                Bitboard(268496640),
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
            "r1bq1b1r/ppp2kpp/2n5/3np3/2B5/5Q2/PPPP1PPP/RNB1K2R b KQ - 1 7",
            Move(Flags.QUIET, squares.F7, squares.E6),
            [
                Bitboard(61184),
                Bitboard(2),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(2097152),
                Bitboard(16),
                Bitboard(56013589084897280),
                Bitboard(4432406249472),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(17592186044416)
            ]
        )
    ]
)
def test_quiet(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards
    
@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            Move(Flags.CAPTURE, squares.E4, squares.D5),
            [
                Bitboard(34359799552),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532032),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976)
            ]
        ),
        (
            "r1bqkb1r/ppp2ppp/2n2n2/3Pp1N1/2B5/8/PPPP1PPP/RNBQK2R b KQkq - 0 5",
            Move(Flags.CAPTURE, squares.F6, squares.D5),
            [
                Bitboard(61184),
                Bitboard(274877906946),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(65020788339638272),
                Bitboard(4432406249472),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976)
            ]
        )
    ]
)
def test_capture(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards

@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
            Move(Flags.SHORT_CASTLE, squares.NONE, squares.NONE),
            [
                Bitboard(268496640),
                Bitboard(2097154),
                Bitboard(8589934596),
                Bitboard(33),
                Bitboard(8),
                Bitboard(64),
                Bitboard(67272588153323520),
                Bitboard(39582418599936),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976)
            ]
        ),
        (
            "r1bqk2r/ppppbppp/3n4/1B2R3/8/2N5/PPPP1PPP/R1BQ2K1 b kq - 0 8",
            Move(Flags.SHORT_CASTLE, squares.NONE, squares.NONE),
            [
                Bitboard(61184),
                Bitboard(262144),
                Bitboard(8589934596),
                Bitboard(68719476737),
                Bitboard(8),
                Bitboard(64),
                Bitboard(67272519433846784),
                Bitboard(8796093022208),
                Bitboard(292733975779082240),
                Bitboard(2377900603251621888),
                Bitboard(576460752303423488),
                Bitboard(4611686018427387904)
            ]
        )
    ]
)
def test_short_castle(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards
    
@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "rnb1kbnr/ppp2ppp/3p1q2/4p3/3PP3/2N2Q2/PPP2PPP/R3KBNR w KQkq - 2 6",
            Move(Flags.LONG_CASTLE, squares.NONE, squares.NONE),
            [
                Bitboard(402712320),
                Bitboard(262208),
                Bitboard(32),
                Bitboard(136),
                Bitboard(2097152),
                Bitboard(4),
                Bitboard(65029584432660480),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(35184372088832),
                Bitboard(1152921504606846976)
            ]
        ),
        (
            "r3kbnr/ppp2ppp/2npbQ2/4p3/3PP3/2N2N2/PPP2PPP/2KR1B1R b kq - 2 8",
            Move(Flags.LONG_CASTLE, squares.NONE, squares.NONE),
            [
                Bitboard(402712320),
                Bitboard(2359296),
                Bitboard(32),
                Bitboard(136),
                Bitboard(35184372088832),
                Bitboard(4),
                Bitboard(65029584432660480),
                Bitboard(4611690416473899008),
                Bitboard(2305860601399738368),
                Bitboard(9799832789158199296),
                Bitboard(0),
                Bitboard(288230376151711744)
            ]
        )
    ]
)
def test_long_castle(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards

@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "r1bqkbnr/ppppp1pp/2n5/4Pp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3",
            Move(Flags.EN_PASSANT, squares.E5, squares.F6),
            [
                Bitboard(35184372150016),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(62768919806476288),
                Bitboard(4611690416473899008),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976)
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2PpP3/5N2/PP1P1PPP/RNBQKB1R b KQkq c3 0 3",
            Move(Flags.EN_PASSANT, squares.D4, squares.C3),
            [
                Bitboard(268495616),
                Bitboard(2097154),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247794176),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        )
    ]
)
def test_en_passant(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards

@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.QUEEN_PROMOTE, squares.B7, squares.B8),
            [
                Bitboard(61184),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(144115188075855880),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.ROOK_PROMOTE, squares.B7, squares.B8),
            [
                Bitboard(61184),
                Bitboard(66),
                Bitboard(36),
                Bitboard(144115188075856001),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.BISHOP_PROMOTE, squares.B7, squares.B8),
            [
                Bitboard(61184),
                Bitboard(66),
                Bitboard(144115188075855908),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.KNIGHT_PROMOTE, squares.B7, squares.B8),
            [
                Bitboard(61184),
                Bitboard(144115188075855938),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.QUEEN_PROMOTE, squares.G2, squares.G1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532032),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423552),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.ROOK_PROMOTE, squares.G2, squares.G1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532032),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703808),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.BISHOP_PROMOTE, squares.G2, squares.G1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532032),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405760),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.KNIGHT_PROMOTE, squares.G2, squares.G1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532032),
                Bitboard(4755801206503243840),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        )
    ]
)
def test_promotion(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards

@pytest.mark.parametrize(
    "fen, move, expected_bitboards",
    [
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.QUEEN_PROMOTE_CAPTURE, squares.B7, squares.A8),
            [
                Bitboard(72057594037989120),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9223372036854775808),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.ROOK_PROMOTE_CAPTURE, squares.B7, squares.A8),
            [
                Bitboard(72057594037989120),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9223372036854775808),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.BISHOP_PROMOTE_CAPTURE, squares.B7, squares.A8),
            [
                Bitboard(72057594037989120),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9223372036854775808),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "r2qkbnr/pP2pppp/n7/8/6b1/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            Move(Flags.KNIGHT_PROMOTE_CAPTURE, squares.B7, squares.A8),
            [
                Bitboard(72057594037989120),
                Bitboard(66),
                Bitboard(36),
                Bitboard(129),
                Bitboard(8),
                Bitboard(16),
                Bitboard(67835469387268096),
                Bitboard(4611687117939015680),
                Bitboard(2305843010287435776),
                Bitboard(9223372036854775808),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.QUEEN_PROMOTE_CAPTURE, squares.G2, squares.H1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(1),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532160),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.ROOK_PROMOTE_CAPTURE, squares.G2, squares.H1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(1),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532160),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.BISHOP_PROMOTE_CAPTURE, squares.G2, squares.H1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(1),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532160),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        ),
        (
            "rnbqkbnr/ppp1pppp/8/8/2B5/2N5/PPPP1PpP/R1BQK2R b KQkq - 0 5",
            Move(Flags.KNIGHT_PROMOTE_CAPTURE, squares.G2, squares.H1),
            [
                Bitboard(44800),
                Bitboard(262144),
                Bitboard(67108868),
                Bitboard(1),
                Bitboard(8),
                Bitboard(16),
                Bitboard(69524319247532160),
                Bitboard(4755801206503243776),
                Bitboard(2594073385365405696),
                Bitboard(9295429630892703744),
                Bitboard(576460752303423488),
                Bitboard(1152921504606846976),
            ]
        )
    ]
)
def test_promotion_capture(fen: str, move: Move, expected_bitboards: List[Bitboard]) -> None:
    test_board = Board.from_fen(fen)
    test_board = MoveMaker.push(test_board, move)
    assert test_board.bitboards == expected_bitboards