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
# pylint: disable=super-init-not-called
# pylint: disable=unused-argument

# standard
from typing import Self, NewType

# third-party
import numpy as np

# project
from pieces import Pieces

FenString = NewType("FenString", str)
Bitboards = NewType("Bitboards", np.ndarray)
Turn = NewType("Turn", bool)
CastlingRights = NewType("CastlingRights", int)

# TODO: Add the following stuff
# 12 bitboards for each color (complete)
# 2 bitboards for occupancy (unoptimized)
# game state information
# game history
# zobrist keys
# piece lists

class Board(np.ndarray):
    """
    Args:
        data (str, optional): Must be a fen string
        data (list, optional):
            - board (np.ndarray): The board state in bitboard format
            - turn (bool): True for white, False for black
            - castling_rights (int): The castling rights represented as a 4 bit integer
    
    - The class represents a board state with bitboards
    - For all bitboards, LSB = A1 (Little-Endian Rank-File mapping)
        - reference: https://www.chessprogramming.org/Square_Mapping_Considerations
    - This object is a numpy array of 12 unsigned 64-bit integers which represents
      the board state
    """
    def __new__(cls, data="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> Self:
        if isinstance(data, str):
            bitboards, cls.turn, cls.castling_rights = cls.load_from_fen(data)
        elif isinstance(data, (list, tuple)) and len(data) == 3:
            bitboards, cls.turn, cls.castling_rights = data
        else:
            raise ValueError("Invalid data format")
        
        obj = np.asarray(bitboards, dtype=np.uint64).view(cls)
        return obj
    
    def __init__(self, data = None | FenString | list[Bitboards, Turn, CastlingRights]) -> None:
        self.update_bitboard_info()
    
    def __repr__(self) -> str:
        """ Displays the board state """
        output = ""
        
        for row in range(8):
            output += "\n+" + "---+"*8 + "\n"
            output += "| "
            for tile in range(7, -1, -1):
                for bitboard_index in [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13]:
                    if bin(self[bitboard_index])[2:].rjust(64, '0')[row*8+tile] == '1':
                        output += f'{Pieces.DECODE[bitboard_index]} | '
                        break
                else:
                    output += '. | '
            output += f' {8-row}'
        output += "\n+" + "---+"*8 + "\n"
        output += '  ' + '   '.join('abcdefgh')
        return output

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def load_from_fen(fen: str) -> list[list[np.uint64], bool, int]:
        """ Converts a FEN string into a list of bitboards

        Args:
            fen (str): A FEN string representing a board position

        Returns:
            bitboard: A list of 12 bitboards
            turn: The current turn
            castling_rights: The current castling rights
        """
        
        # initilize an empty board
        bitboards = np.zeros(16, dtype=np.uint64)
        
        # parse the FEN string
        fen_data = fen.split(' ')
        fen_board = fen.split(' ')[0]
        turn = True if fen_data[1] == "w" else False
        castling_rights = int("".join(["1" if char != "-" else "0" for char in fen_data[2]]), 2)
        
        column = 0
        row = 7
        for character in fen_board:
            if character == '/': # move to the next row
                column = 0
                row -= 1
            elif character.isdigit(): # skip empty squares
                column += int(character)
            else: # place the piece on the corresponding bitboard
                piece_index = Pieces.ENCODE[character]
                square_index = column + row * 8
                bitboards[piece_index] |= 1 << square_index
                column += 1
        
        return bitboards, turn, castling_rights

    @staticmethod
    def display_bitboard(bitboard: np.uint64) -> None:
        """ Displays the given bitboard to the CLI
        Args:
            bitboard (np.uint64): The 64 bit board to display
        """
        bitboard = bin(bitboard)[2:].rjust(64, '0')
        for row in range(8):
            for tile in range(7, -1, -1):
                print(f'{bitboard[row*8+tile]} ', end='')
            print(f'| {8-row}')
        print('----------------+')
        print('a b c d e f g h')

    def update_bitboard_info(self) -> None:
        """ Updates bitboard info (all pieces data) """
        self[Pieces.ALL_WHITE] = \
            self[Pieces.WHITE | Pieces.KING] | \
            self[Pieces.WHITE | Pieces.QUEEN] | \
            self[Pieces.WHITE | Pieces.ROOK] | \
            self[Pieces.WHITE | Pieces.BISHOP] | \
            self[Pieces.WHITE | Pieces.KNIGHT] | \
            self[Pieces.WHITE | Pieces.PAWN]
        
        self[Pieces.ALL_BLACK] = \
            self[Pieces.BLACK | Pieces.KING] | \
            self[Pieces.BLACK | Pieces.QUEEN] | \
            self[Pieces.BLACK | Pieces.ROOK] | \
            self[Pieces.BLACK | Pieces.BISHOP] | \
            self[Pieces.BLACK | Pieces.KNIGHT] | \
            self[Pieces.BLACK | Pieces.PAWN]
        
        self[Pieces.OCCUPIED] = self[Pieces.ALL_WHITE] | self[Pieces.ALL_BLACK]
        self[Pieces.EMPTY] = ~self[Pieces.OCCUPIED]

    def deepcopy(self) -> Self:
        """ Returns a copy of this board instance

        Returns:
            Self: A new copy of the board instance
        """
        return Board((self, self.turn, self.castling_rights))
