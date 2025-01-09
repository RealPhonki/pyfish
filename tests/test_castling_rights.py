# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# third party
import pytest

# project
from src.core.castling_rights import CastlingRights

@pytest.mark.parametrize(
    "castling_rights, expected_output",
    [
        (CastlingRights(0b0000), CastlingRights(0b0000)),
        (CastlingRights(0b1111), CastlingRights(0b0011)),
        (CastlingRights(0b1001), CastlingRights(0b0001)),
        (CastlingRights(0b1011), CastlingRights(0b0011)),
    ]
)
def test_disable_white(castling_rights: CastlingRights, expected_output: CastlingRights) -> None:
    assert castling_rights.disable_white() == expected_output

@pytest.mark.parametrize(
    "castling_rights, expected_output",
    [
        (CastlingRights(0b0000), CastlingRights(0b0000)),
        (CastlingRights(0b1111), CastlingRights(0b1100)),
        (CastlingRights(0b1001), CastlingRights(0b1000)),
        (CastlingRights(0b1011), CastlingRights(0b1000)),
    ]
)
def test_disable_black(castling_rights: CastlingRights, expected_output: CastlingRights) -> None:
    assert castling_rights.disable_black() == expected_output