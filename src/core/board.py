# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# standard
from typing import TypeAlias, Tuple, Self
from dataclasses import dataclass

# third party
import numpy as np

# project
from src.core.castling_rights import CastlingRights
from src.core.bitboard import Bitboard
from src.core.piece import Piece
from src.core.squares import BB_MASK

Board: TypeAlias = Tuple[np.ndarray[Bitboard], bool, CastlingRights]

class InvalidFENError(Exception):
    """ Represents an invalid fen string input. """

@dataclass
class Board:
    """
    Contains methods for generating, handling, and displaying bitboards.
    
    The bitboards attribute is a fixed array of 12 64-bit unsigned integers. Each integer
    represents the locations of pieces on the board.
    
    The turn attribute is a boolean where True indicates white-to-play and False indicates
    black-to-play.
    
    The castling_rights attribute is a 4-bit integer where each bit represents a castling right.
    """
    bitboards: np.ndarray[Bitboard]
    turn: bool
    castling_rights: CastlingRights
    
    def __repr__(self) -> str:
        return f"Board(..., {self.turn}, {self.castling_rights})"
    
    def __str__(self) -> str:
        output = ""
        for row in range(7, -1, -1):
            output += "\n+" + "---+"*8 + "\n"
            output += "| "
            for tile in range(8):
                square = row * 8 + tile
                for piece_type, bitboard in enumerate(self.bitboards):
                    if bitboard.get_bit(square):
                        output += f'{Piece.SYMBOL[piece_type]} | '
                        break
                else:
                    output += '  | '
            output += str(row + 1)
        
        output += "\n+" + "---+"*8 + "\n"
        output += '  ' + '   '.join('abcdefgh')
        return output
    
    @classmethod
    def from_fen(cls, fen: str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> Self:
        """ Generates bitboard data from a fen string

        Args:
            fen (str, optional): The position of the board in fen notation.
            Defaults to the starting position.

        Returns:
            Self: The board object
        """
        if not isinstance(fen, str):
            raise InvalidFENError(f"FEN must be of type string. Got '{fen}'")
        
        # initialize a list of empty bitboards
        bitboards = [Bitboard(0) for _ in range(12)]
        
        # parse FEN
        fen_data = fen.split(' ')
        fen_board = fen_data[0]
        turn = fen_data[1] == "w"
        castling_rights = CastlingRights.from_text(fen_data[2])

        column = 0
        row = 7
        for character in fen_board:
            if character == "/": # move to the next row
                column = 0
                row -= 1
            elif character.isdigit(): # skip empty square
                column += int(character)
            else: # place the piece on the corresponding bitboard
                piece_type = Piece.SYMBOL.index(character)
                square = column + row * 8
                bitboards[piece_type] |= BB_MASK[square]
                column += 1
        
        return cls(bitboards, turn, castling_rights)
    
    def get_piece(self, square: int) -> int:
        """ Returns the piece that is at a given square

        Args:
            square (int): The square to check

        Returns:
            int: The piece type (the index of which bitboard contains the piece)
        """
        for piece_type, bitboard in enumerate(self.bitboards):
            if bitboard.get_bit(square):
                return piece_type
        return None
    
    def copy(self) -> Self:
        return Board(self.bitboards.copy(), self.turn, self.castling_rights)