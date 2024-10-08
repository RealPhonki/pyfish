# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=import-error  

# third-party
import numpy as np

# project
from board import Board

class BitMaster:
    """ Handles bitwise operations regarding ulongs """
    @staticmethod
    def get(board: Board, bit_index: int) -> int:
        """ Returns the piece encoding for a given bit index

        Args:
            board (Board): The board to operate on
            bit_index (int): The bit_index of the tile

        Returns:
            int: The piece encoding
        """
        for bitboard_index, bitboard in enumerate(board):
            if ((bitboard >> np.uint64(bit_index)) & 1) != 0:
                return bitboard_index
        return None
    
    @staticmethod
    def place(board: Board, bit_index: int, piece_encoding: int) -> None:
        """ Adds a piece at the given index to the specified bitboard

        Args:
            board (Board): The board to operate on
            bit_index (int): The index of the tile
            piece_encoding (int): The piece encoding
        """
        
        board[piece_encoding] |= np.uint64(1) << np.uint64(bit_index)
    
    @staticmethod
    def destroy(board: Board, bit_index: int) -> None:
        """ Destroys a piece at a given index

        Args:
            board (Board): The board to operate on
            bit_index (int): The index of the tile
        """
        board &= ~(np.uint64(1) << np.uint64(bit_index))
        
    @staticmethod
    def shift_vertical(bitboard: np.uint64, shift: int, downward: bool) -> np.uint64:
        """ Shifts a given bitboard vertically

        Args:
            bitboard (np.uint64): The bitboard to shift
            shift (int): The amount of tiles to shift vertically
            upwards (bool): The direction of the shift (upwards or downwards)

        Returns:
            np.uint64: The shifted bitboard
        """
        if downward:
            return bitboard >> np.uint64(8*shift)
        else:
            return bitboard << np.uint64(8*shift)