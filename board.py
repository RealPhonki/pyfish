# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

import numpy as np

class Pieces:
    """ Assigns piece names to the different piece encodings (bitboard indices) """
    WHITE_KING = 0
    WHITE_QUEEN = 1
    WHITE_ROOK = 2
    WHITE_BISHOP = 3
    WHITE_KNIGHT = 4
    WHITE_PAWN = 5
    BLACK_KING = 9
    BLACK_QUEEN = 10
    BLACK_ROOK = 11
    BLACK_BISHOP = 12
    BLACK_KNIGHT = 13
    BLACK_PAWN = 14
    
    DECODE = {
        0: "K",  1: "Q",  2: "R",  3: "B",  4: "N",  5: "P",
        9: "k", 10: "q", 11: "r", 12: "b", 13: "n", 14: "p"
    }
    
    ENCODE = {
        "K": 0, "Q":  1, "R":  2, "B":  3, "N":  4, "P":  5,
        "k": 9, "q": 10, "r": 11, "b": 12, "n": 13, "p": 14
    }

class Board(np.ndarray):
    """ The class represents a board state with bitboards
    - For all bitboards, LSB = A1 (aka Little-Endian Rank-File mapping)
        reference: https://www.chessprogramming.org/Square_Mapping_Considerations
    - This object is a numpy array of 12 unsigned 64-bit integers which represent
      the board state
    """
    
    BITMASK64 = np.uint64((1 << 64) - 1)
    
    def __new__(cls, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        data, cls.turn, cls.castling_rights = cls.load_from_fen(fen_string)
        obj = np.asarray(data, dtype=np.uint64).view(cls)
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
        output += '  ' + '   '.join('abcdefgh') + "\n"
        return output

    def __str__(self) -> str:
        return self.__repr__()

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
        self &= ~(np.uint64(1) << np.uint64(tile_index)) & self.BITMASK64
    
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

if __name__ == '__main__':
    test_board = Board()
    test_board.destroy(2**8)
    print(test_board)