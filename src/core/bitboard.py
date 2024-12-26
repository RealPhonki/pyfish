# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error

# standard
from typing import Self

# third party
import numpy as np

class Bitboard(np.uint64):
    """
    Stores positional data for a single piece type with a 64-bit unsigned integer.
    Each bit in the integer represents the location of a single piece.
    """
    def __new__(cls, value: int) -> None:
        return np.uint64.__new__(cls, value)
    
    def __repr__(self) -> str:
        output = ""
        bitboard = bin(self)[2:].rjust(64, '0')
        for row in range(8):
            for tile in range(7, -1, -1):
                output += f'{bitboard[row*8+tile]} '
            output += f'| {8-row}\n'
        output += '----------------+\n'
        output += 'a b c d e f g h\n'
        return output
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __or__(self, other: int) -> Self:
        return Bitboard(super() | other)
    
    def __and__(self, other: int) -> Self:
        return Bitboard(super() & other)
    
    def get_bit(self, square: int) -> int:
        """ Returns the bit value at a given square

        Args:
            square (int): The location of the bit to retrieve

        Returns:
            int: The value of the bit at the given index
        """
        return (self >> np.uint64(square)) & 1