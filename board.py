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
    """ Assigns piece names to the different bitboard indices """
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
    """
    def __init__(self, fen_string: str) -> None:
        self.bitboards = self.load_from_fen(fen_string)
    
    def __getitem__(self, index: int) -> np.uint64:
        return self.bitboards[index]
    
    @staticmethod
    def load_from_fen(fen: str) -> list[np.uint64]:
        """ Converts a FEN string into a list of bitboards

        Args:
            fen (str): A FEN string representing a board position

        Returns:
            list[np.uint64]: A list of 12 bitboards
        """
        
        # initilize an empty board
        bitboards = np.zeros(12, dtype=np.uint64)
        
        # parse the FEN string for the part that contains board data
        fen_board = fen.split(' ')[0]
        
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
        
        return bitboards
    
    def display_bitboard(self, bitboard_index: int) -> None:
        """ Displays the given bitboard to the CLI

        Args:
            bitboard (np.uint64): The 64 bit board to display
        """
        bitboard = bin(self.bitboards[bitboard_index])[2:].rjust(64, '0')
        for row in range(8):
            for tile in range(7, -1, -1):
                print(f'{bitboard[row*8+tile]} ', end='')
            print(f'| {8-row}')
        print('----------------+')
        print('a b c d e f g h')
    
    def __str__(self) -> str:
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
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(board)
    board.display_bitboard(0)