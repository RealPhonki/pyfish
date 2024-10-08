# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=expression-not-assigned
# pylint: disable=missing-function-docstring

# standard
from typing import overload

# third party
import numpy as np

class Flags:
    """ Assigns names to the different encodings for move types """
    QUIET                  = 0b0000
    DOUBLE_PAWN_PUSH       = 0b0001
    SHORT_CASTLE           = 0b0010
    LONG_CASTLE            = 0b0011
    CAPTURE                = 0b0100
    EN_PASSANT             = 0b0101
    KNIGHT_PROMOTE         = 0b1000
    BISHOP_PROMOTE         = 0b1001
    ROOK_PROMOTE           = 0b1010
    QUEEN_PROMOTE          = 0b1011
    KNIGHT_PROMOTE_CAPTURE = 0b1100
    BISHOP_PROMOTE_CAPTURE = 0b1101
    ROOK_PROMOTE_CAPTURE   = 0b1110
    QUEEN_PROMOTE_CAPTURE  = 0b1111

class Move(np.uint16):
    """ Represents a chess move with a 16 bit unsigned integer
    - 4 bits for move type (information below)
    - 6 bits for the initial square
    - 6 bits for the target square
    reference: https://www.chessprogramming.org/Encoding_Moves
    """
    
    @overload
    def __new__(cls, flags: int, initial_square: int, target_square: int) -> None: ...
    
    def __new__(cls, flags: int, initial_square: int, target_square: int) -> None:
        value = ((flags & 0xf)<<12) | ((initial_square & 0x3f)<<6) | (target_square & 0x3f)
        return np.uint16.__new__(cls, value)
    
    @property
    def flags(self) -> int:
        return (self >> 12) & 0xf
    
    @property
    def initial_square(self) -> int:
        return (self >> 6) & 0x3f
    
    @property
    def target_square(self) -> int:
        return self & 0x3f
    
    @property
    def is_quiet(self) -> bool:
        return self.flags == Flags.QUIET
    
    @property
    def is_double_pawn_push(self) -> bool:
        return self.flags == Flags.DOUBLE_PAWN_PUSH
    
    @property
    def is_short_castle(self) -> bool:
        return self.flags == Flags.KING_CASTLE
    
    @property
    def is_long_castle(self) -> bool:
        return self.flags == Flags.QUEEN_CASTLE
    
    @property
    def is_capture(self) -> bool:
        return self.flags & Flags.CAPTURE != 0
    
    @property
    def is_en_passant(self) -> bool:
        return self.flags == Flags.EN_PASSANT
    
    @property
    def is_promotion(self) -> bool:
        return (self.flags >> 3) != 0