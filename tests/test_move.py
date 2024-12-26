# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# third party
import pytest

# project
from src.core.move import Move, Flags, InvalidMoveError

@pytest.mark.parametrize(
    "initial_square",
    [
        -1,
        64,
        100
    ]
)
def test_invalid_initial_square(initial_square: any) -> None:
    with pytest.raises(InvalidMoveError):
        Move(Flags.QUIET, initial_square, 0)

@pytest.mark.parametrize(
    "target_square",
    [
        -1,
        64,
        100
    ]
)
def test_invalid_target_square(target_square: any) -> None:
    with pytest.raises(InvalidMoveError):
        Move(Flags.QUIET, 0, target_square)

@pytest.mark.parametrize(
    "invalid_flag",
    [
        -1,
        16
    ]
)
def test_invalid_flags(invalid_flag: any) -> None:
    with pytest.raises(InvalidMoveError):
        Move(invalid_flag, 0, 0)

@pytest.mark.parametrize(
    "invalid_value",
    [
        -50,
        18446744073709551616,
        "string_input"
    ]
)
def test_type_safety(invalid_value: any) -> None:
    with pytest.raises(InvalidMoveError):
        Move(invalid_value, 0, 0)
    with pytest.raises(InvalidMoveError):
        Move(Flags.QUIET, invalid_value, 0)
    with pytest.raises(InvalidMoveError):
        Move(Flags.QUIET, 0, invalid_value)

@pytest.mark.parametrize(
    "initial_square, expected_value",
    [
        (i, i) for i in range(64)
    ]
)
def test_initial_square_lossless(initial_square: int, expected_value: int) -> None:
    assert Move(Flags.QUIET, initial_square, 0).initial_square == expected_value

@pytest.mark.parametrize(
    "target_square, expected_value",
    [
        (i, i) for i in range(64)
    ]
)
def test_target_square_lossless(target_square: int, expected_value: int) -> None:
    assert Move(Flags.QUIET, 0, target_square).target_square == expected_value

@pytest.mark.parametrize(
    "flag, expected_value",
    [
        (Flags.QUIET,                  Flags.QUIET                 ),
        (Flags.DOUBLE_PAWN_PUSH,       Flags.DOUBLE_PAWN_PUSH      ),
        (Flags.SHORT_CASTLE,           Flags.SHORT_CASTLE          ),
        (Flags.LONG_CASTLE,            Flags.LONG_CASTLE           ),
        (Flags.CAPTURE,                Flags.CAPTURE               ),
        (Flags.EN_PASSANT,             Flags.EN_PASSANT            ),
        (Flags.KNIGHT_PROMOTE,         Flags.KNIGHT_PROMOTE        ),
        (Flags.BISHOP_PROMOTE,         Flags.BISHOP_PROMOTE        ),
        (Flags.ROOK_PROMOTE,           Flags.ROOK_PROMOTE          ),
        (Flags.QUEEN_PROMOTE,          Flags.QUEEN_PROMOTE         ),
        (Flags.KNIGHT_PROMOTE_CAPTURE, Flags.KNIGHT_PROMOTE_CAPTURE),
        (Flags.BISHOP_PROMOTE_CAPTURE, Flags.BISHOP_PROMOTE_CAPTURE),
        (Flags.ROOK_PROMOTE_CAPTURE,   Flags.ROOK_PROMOTE_CAPTURE  ),
        (Flags.QUEEN_PROMOTE_CAPTURE,  Flags.QUEEN_PROMOTE_CAPTURE )
    ]
)
def test_flags_lossless(flag: int, expected_value: int) -> None:
    assert Move(flag, 0, 0).flags == expected_value