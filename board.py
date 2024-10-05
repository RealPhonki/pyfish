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
    BLACK_KING = 6
    BLACK_QUEEN = 7
    BLACK_ROOK = 8
    BLACK_BISHOP = 9
    BLACK_KNIGHT = 10
    BLACK_PAWN = 11
    
    SYMBOL_FROM_INDEX = {
        0: "K", 1: "Q", 2: "R", 3: "B", 4: "N", 5: "P",
        6: "k", 7: "q", 8: "r", 9: "b", 10: "n", 11: "p"
    }
    
    INDEX_FROM_SYMBOL = {
        "K": 0, "Q": 1, "R": 2, "B": 3, "N":  4, "P":  5,
        "k": 6, "q": 7, "r": 8, "b": 9, "n": 10, "p": 11
    }

class Board():
    """ The class represents a board state with bitboards
    - For all bitboards, LSB = A1 (aka Little-Endian Rank-File mapping)
        reference: https://www.chessprogramming.org/Square_Mapping_Considerations
    - The bitboards attribute is a numpy array of 12 unsigned 64-bit integers which
      represents the board state
    """
    
    BITMASK64 = np.uint64((1 << 64) - 1)
    
    def __init__(
            self,
            fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            ) -> None:
        self.bitboards, self.turn, self.castling_rights = self.load_from_fen(fen_string)
    
    def get(self, index: int) -> int:
        """ Returns the piece encoding for a given index

        Args:
            index (int): The index

        Returns:
            int: The piece encoding
        """
        for index, bitboard in enumerate(self.bitboards):
            if ((bitboard >> np.uint64(index)) & np.uint64(1)) != 0:
                return index
        return None
    
    def place(self, index: int, piece_encoding: int) -> None:
        """ Adds a piece at the given index to the specified bitboard

        Args:
            index (int): The index
            piece_encoding (int): The piece encoding
        """
        self.bitboards[piece_encoding] |= np.uint64(1) << np.uint64(index)
    
    def destroy(self, index: int) -> None:
        """ Destroys a piece at a given index

        Args:
            index (int): The index
        """
        mask = ~(np.uint64(1) << np.uint64(index)) & self.BITMASK64
        self.bitboards = self.bitboards & mask
    
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
        bitboards = np.zeros(12, dtype=np.uint64)
        
        # parse the FEN stringa
        fen_data = fen.split(' ')
        fen_board = fen.split(' ')[0]
        turn = True if fen_data[1] == "w" else False
        castling_rights = int("".join(["1" if char != "-" else "0" for char in fen_data[2]]), 2)
        
        column = 0
        row = 7
        for symbol in fen_board:
            if symbol == '/': # move to the next row
                column = 0
                row -= 1
            elif symbol.isdigit(): # skip empty squares
                column += int(symbol)
            else: # place the piece on the corresponding bitboard
                piece_index = Pieces.INDEX_FROM_SYMBOL[symbol]
                square_index = column + row * 8
                bitboards[piece_index] = bitboards[piece_index] | 1 << square_index
                column += 1
        
        return bitboards, turn, castling_rights
    
    def __repr__(self) -> str:
        """ Displays the given board to the CLI

        Args:
            board (list[np.uint64]): A list of bitboards
        """
        output = ""
        
        for row in range(8):
            output += "\n+" + "---+"*8 + "\n"
            output += "| "
            for tile in range(7, -1, -1):
                for bitboard_index in range(len(self.bitboards)):
                    if bin(self.bitboards[bitboard_index])[2:].rjust(64, '0')[row*8+tile] == '1':
                        output += f'{Pieces.SYMBOL_FROM_INDEX[bitboard_index]} | '
                        break
                else:
                    output += '. | '
            output += f' {8-row}'
        output += "\n+" + "---+"*8 + "\n"
        output += '  ' + '   '.join('abcdefgh') + "\n"
        return output

if __name__ == '__main__':
    test_board = Board()
    test_board.destroy(12)
    print(test_board)