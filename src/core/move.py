# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

# standard
from typing import TypeAlias, Self, overload

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
    @overload
    def __init__(self, flags: UInt4, initial_square: UInt6, target_square: UInt6) -> None: ...
    
    def __new__(cls, flags: UInt4, initial_square: UInt6, target_square: UInt6) -> Self:
        # ensure safe types
        cls._validate(flags, 0xF, "Flags")
        cls._validate(initial_square, 0x3F, "Initial square")
        cls._validate(target_square, 0x3F, "Target square")
        
        # initialize
        value = ((flags & 0xf)<<12) | ((initial_square & 0x3f)<<6) | (target_square & 0x3f)
        return np.uint16.__new__(cls, value)
    
    @classmethod
    def _validate(cls, value: int, max_value: int, name: str):
        if not (isinstance(value, int) and 0 <= value <= max_value):
            error = f"{name} must be an integer between 0 and {max_value}, got '{value}'"
            raise InvalidMoveError(error)
    
    def __repr__(self) -> str:
        return f"Move({self.flags}, {self.initial_square}, {self.target_square})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
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
        return (self.flags >> 2) == 0b10
    
    @property
    def is_promotion_capture(self) -> bool:
        return (self.flags >> 2) == 0b11