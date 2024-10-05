# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from typing import Self, overload, NewType

import numpy as np

from move import Move
from pieces import Pieces

FenString = NewType("FenString", str)
Bitboards = NewType("Bitboards", np.ndarray)
Turn = NewType("Turn", bool)
CastlingRights = NewType("CastlingRights", int)

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
    - This object is immutable
    """
    @overload
    def __new__(cls, data = None | FenString | list[Bitboards, Turn, CastlingRights]) -> Self: ...
    
    def __new__(cls, data="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> Self:
        if isinstance(data, str):
            bitboards, cls.turn, cls.castling_rights = cls.load_from_fen(data)
        elif isinstance(data, (list, tuple)) and len(data) == 3:
            bitboards, cls.turn, cls.castling_rights = data
        else:
            raise ValueError("Invalid data format")
    
        obj = np.asarray(bitboards, dtype=np.uint64).view(cls)
        return obj
    
    def __repr__(self) -> str:
        """ Displays the board state """
        output = ""
        
        for row in range(8):
            output += "\n+" + "---+"*8 + "\n"
            output += "| "
            for tile in range(7, -1, -1):
                for bitboard_index in range(len(self)):
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
    
    def __setattr__(self, name, value) -> AttributeError:
        """ Make the object immutable

        Args:
            name (_type_): The name of the attribute
            value (_type_): The value of the attribute

        Raises:
            AttributeError: The error since the object is immutable
        """
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify attribute '{name}'")
        super().__setattr__(name, value)

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

    def display_bitboard(self, piece: int | str) -> None:
        """ Displays the given bitboard to the CLI
        Args:
            bitboard (np.uint64): The 64 bit board to display
        """
        if isinstance(piece, str):
            piece = Pieces.ENCODE[piece]
        bitboard = bin(self[piece])[2:].rjust(64, '0')
        for row in range(8):
            for tile in range(7, -1, -1):
                print(f'{bitboard[row*8+tile]} ', end='')
            print(f'| {8-row}')
        print('----------------+')
        print('a b c d e f g h')

    def get(self, tile_index: int) -> int:
        """ Returns the piece encoding for a given index

        Args:
            tile_index (int): The index of the tile

        Returns:
            int: The piece encoding
        """
        for index, bitboard in enumerate(self):
            if ((bitboard >> np.uint64(tile_index)) & 1) != 0:
                return index
        return None
    
    def place(self, tile_index: int, piece_encoding: int) -> None:
        """ Adds a piece at the given index to the specified bitboard

        Args:
            tile_index (int): The index of the tile
            piece_encoding (int): The piece encoding
        """
        self[piece_encoding] |= np.uint64(1) << np.uint64(tile_index)
    
    def destroy(self, tile_index: int) -> None:
        """ Destroys a piece at a given index

        Args:
            tile_index (int): The index of the tile
        """
        self &= ~(np.uint64(1) << np.uint64(tile_index))

    def quiet(self, move: Move) -> Self:
        """ Performs a quiet move

        Returns:
            Self: A copy of the board with the quiet move applied
        """
        new_board = Board((self, self.turn, self.castling_rights))
        piece = new_board.get(move.initial_square)
        new_board.destroy(move.initial_square)
        new_board.place(move.target_square, piece)
        return new_board

    def short_castle(self) -> Self:
        """ Performs a short-castle

        Returns:
            Self: A copy of the board with the short-castle applied
        """
        # choose side and color
        row = 0 if self.turn else 7
        color = Pieces.WHITE if self.turn else Pieces.BLACK
        
        new_board = Board((self, self.turn, self.castling_rights))
        new_board &= ~np.uint64(15 << (4 + row*8))
        new_board[color | Pieces.ROOK] |= np.uint64(1 << (5 + row*8))
        new_board[color | Pieces.KING]  = np.uint64(1 << (6 + row*8))
        return new_board
    
    def long_castle(self) -> Self:
        """ Performs a long-castle

        Returns:
            Self: A copy of the board with the long-castle applied
        """
        row = 0 if self.turn else 7
        color = Pieces.WHITE if self.turn else Pieces.black
        
        new_board = Board((self, self.turn, self.castling_rights))
        new_board &= ~np.uint64(15 << (row*8))
        new_board[color | Pieces.KING] = np.uint64(1 << (2 + row*8))
        new_board[color | Pieces.ROOK] |= np.uint64(1 << (3 + row*8))
        return new_board
    
    def capture(self, move: Move) -> Self:
        """ Performs a capture move

        Returns:
            Self: A copy of the board with the capture move applied
        """
        new_board = Board((self, self.turn, self.castling_rights))
        piece = new_board.get(move.initial_square)
        new_board.destroy(move.initial_square)
        new_board.destroy(move.target_square)
        new_board.place(move.target_square, piece)
        return new_board
    
    def en_passant(self, move: Move) -> Self:
        """ Performs an en passant capture

        Returns:
            Self: A copy of the board with the en passant capture applied
        """
        new_board = Board((self, self.turn, self.castling_rights))
        piece = new_board.get(move.initial_square)
        new_board.destroy(move.initial_square)
        new_board.destroy(move.target_square - 8)
        new_board.place(move.target_square, piece)
        return new_board
    
    def promotion(self, move: Move) -> Self:
        """ Performs a promotion move

        Returns:
            Self: A copy of the board with the promotion move applied
        """
        color = Pieces.WHITE if self.turn else Pieces.BLACK
        piece = [Pieces.KNIGHT, Pieces.BISHOP, Pieces.ROOK, Pieces.QUEEN][move.flags & 3]
        
        new_board = Board((self, self.turn, self.castling_rights))
        new_board.destroy(move.initial_square)
        new_board.place(move.target_square, color | piece)
        return new_board
    
    def promotion_capture(self, move: Move) -> Self:
        """ Performs a promotion-capture move

        Returns:
            Self: A copy of the board with the promotion move applied
        """
        color = Pieces.WHITE if self.turn else Pieces.BLACK
        piece = [Pieces.KNIGHT, Pieces.BISHOP, Pieces.ROOK, Pieces.QUEEN][move.flags & 3]
        
        new_board = Board((self, self.turn, self.castling_rights))
        new_board.destroy(move.initial_square)
        new_board.destroy(move.target_square)
        new_board.place(move.target_square, color | piece)
        return new_board
    
    def make_move(self, move: Move) -> Self:
        """ Plays a given move

        Args:
            move (Move): the move to play

        Returns:
            Self: A copy of the board with the move applied
        """
        if move.is_quiet or move.is_double_pawn_push:
            return self.quiet(move)
        elif move.is_short_castle:
            return self.short_castle()
        elif move.is_long_castle:
            return self.long_castle()
        elif move.is_en_passant:
            return self.en_passant(move)
        elif move.is_promotion:
            return self.promotion(move)
        elif move.is_capture:
            return self.capture(move)
        else:
            raise ValueError(f"Invalid move data: {move}")