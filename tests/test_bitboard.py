# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# third party
import pytest

# project
from src.core.bitboard import Bitboard

@pytest.mark.parametrize(
    "invalid_value",
    [
        -50,
        18446744073709551616,
        "string_input"
    ]
)
def test_type_safety(invalid_value: any) -> None:
    with pytest.raises(Exception):
        Bitboard(invalid_value)

@pytest.mark.parametrize(
    "bitboard, square, expected_value",
    [
        (Bitboard(0), 0, 0),
        (Bitboard(1), 0, 1),
        (Bitboard(1), 1, 0)
    ]
)
def test_get_bit(bitboard: Bitboard, square: int, expected_value: int) -> None:
    assert bitboard.get_bit(square) == expected_value