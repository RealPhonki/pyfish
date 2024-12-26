# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

# standard
from typing import TypeAlias, Self

# third party
import numpy as np

UInt4: TypeAlias = int
UInt6: TypeAlias = int

class InvalidMoveError(Exception):
    """ Represents an invalid input to the Move class """

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
    
    Args:
        flags (int): 4-bit flag representing the type of move.
        initial_square (int): 6-bit value for the starting square (0-63).
        target_square (int): 6-bit value for the target square (0-63).
    
    reference: https://www.chessprogramming.org/Encoding_Moves
    """
    
    def __new__(cls, flags: UInt4, initial_square: UInt6, target_square: UInt6) -> Self:
        # ensure safe types
        if not 0 <= flags <= 0xF:
            error_message = f"Flags must be a 4-bit integer (0-15), got {flags}"
            raise InvalidMoveError(error_message)
        if not 0 <= initial_square <= 0x3F:
            error_message = f"Initial square must be a 6-bit integer (0-63), got {initial_square}"
            raise InvalidMoveError(error_message)
        if not 0 <= target_square <= 0x3F:
            error_message = f"Target square must be a 6-bit integer (0-63), got {target_square}"
            raise InvalidMoveError(error_message)
        
        # initialize
        value = ((flags & 0xf)<<12) | ((initial_square & 0x3f)<<6) | (target_square & 0x3f)
        return np.uint16.__new__(cls, value)
    
    def __repr__(self) -> str:
        return f"Move({self.flags}, {self.initial_square}, {self.target_square})"
    
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
        return self.flags == Flags.SHORT_CASTLE
    
    @property
    def is_long_castle(self) -> bool:
        return self.flags == Flags.LONG_CASTLE
    
    @property
    def is_capture(self) -> bool:
        return self.flags & Flags.CAPTURE != 0
    
    @property
    def is_en_passant(self) -> bool:
        return self.flags == Flags.EN_PASSANT
    
    @property
    def is_promotion(self) -> bool:
        return (self.flags >> 3) != 0