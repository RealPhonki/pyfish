# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# standard
from typing import Tuple, TypeAlias, Self
from dataclasses import dataclass

# project
from src.core.bitboard import Bitboard
from src.core.piece import Piece
from src.core import squares

UInt4: TypeAlias = int

class InvalidFENError(Exception):
    """ Represents an invalid fen string input. """

class CastlingRights(UInt4):
    """ Represents the castling rights for a player with a 4 bit integer.
    The bits represent the following information
    - Bit 0: King-side castling for white
    - Bit 1: Queen-side castling for white
    - Bit 2: King-side castling for black
    - Bit 3: Queen-side castling for black
    """
    
    MASKS = {
        "K": 0b1000,
        "Q": 0b0100,
        "k": 0b0010,
        "q": 0b0001
    }
    
    def __new__(cls, value: int) -> None:
        cls._validate(value)
        return super().__new__(cls, value)

    @classmethod
    def _validate(cls, value: int):
        if not (isinstance(value, int) and 0 <= value <= 15):
            error = f"Castling rights must be an integer between 0 and 15, got '{value}'"
            raise ValueError(error)
        
    def __repr__(self) -> str:
        return f"CastlingRights({self.__str__()})"
        
    def __str__(self) -> str:
        text = ""
        for symbol, mask in self.MASKS.items():
            if self & mask != 0:
                text += symbol
        if text == "":
            text = "-"
        return text
    
    @classmethod
    def from_text(cls, text: str) -> Self:
        if text == "-":
            return cls(0)
        out = 0
        for symbol, mask in cls.MASKS.items():
            if symbol in text:
                out |= mask
        return cls(out)
        
    @property
    def white_king_side(self) -> bool:
        return self & 0x1
    
    @property
    def white_queen_side(self) -> bool:
        return self & 0x2
    
    @property
    def black_king_side(self) -> bool:
        return self & 0x4
    
    @property
    def black_queen_side(self) -> bool:
        return self & 0x8

@dataclass(frozen=True)
class Board:
    """ Represents a board state using bitboards.
    A bitboard is a 64-bit unsigned integer where each bit represents a piece location. There
    are 12 bitboards, where each bitboard contains the locations of their respective pieces.
    
    The turn is represented by a boolean. True indicates white to play, False indicates
    black to play.
    
    The castling rights are represented by a 4-bit integer where each bit represents a castling
    right. The bits following this format KQkq
    """
    
    bitboards: Tuple[Bitboard, ...]
    turn: bool
    castling_rights: UInt4
    
    def __repr__(self) -> str:
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
        
        output += "\n+" + "---+"*8 + "\n"
        output += '  ' + '   '.join('abcdefgh')
        return output
    
    def __str__(self) -> str:
        return self.__repr__()
    
    @classmethod
    def from_fen(cls, fen: str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> Self:
        """ Generates a board object from a fen string

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
                bitboards[piece_type] |= squares.MASK[square]
                column += 1
        
        return cls(bitboards, turn, castling_rights)