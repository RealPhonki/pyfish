# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate

import numpy as np

class ChessHandler:
    """ This class implements the rules of chess.
    - For all bitboards, LSB = A1 (aka Little-Endian Rank-File mapping)
        reference: https://www.chessprogramming.org/Square_Mapping_Considerations
    - Moves are represented as "BitUCI" (uint16) which is an adapted form of UCI:
        - 6 bits for the initial square
        - 6 bits for the target square
    """
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
        
        # map FEN piece symbols to their corresponding bitboard index
        INDEX_FROM_SYMBOL = {
            "K": 0, "Q": 1, "R": 2, "B": 3, "N":  4, "P":  5,
            "k": 6, "q": 7, "r": 8, "b": 9, "n": 10, "p": 11
        }
        
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
                piece_index = INDEX_FROM_SYMBOL[symbol]
                square_index = column + row * 8
                bitboards[piece_index] = bitboards[piece_index] | 1 << square_index
                column += 1
        
        return bitboards
    
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
    
    @staticmethod
    def display_board(bitboards: list[np.uint64]) -> None:
        """ Displays the given board to the CLI

        Args:
            board (list[np.uint64]): A list of bitboards
        """
        SYMBOL_FROM_INDEX = {
            0: "K", 1: "Q", 2: "R", 3: "B", 4: "N", 5: "P",
            6: "k", 7: "q", 8: "r", 9: "b", 10: "n", 11: "p"
        }
        
        for row in range(8):
            print("\n+" + "---+"*8)
            print("| ", end='')
            for tile in range(7, -1, -1):
                for bitboard_index in range(len(bitboards)):
                    if bin(bitboards[bitboard_index])[2:].rjust(64, '0')[row*8+tile] == '1':
                        print(f'{SYMBOL_FROM_INDEX[bitboard_index]} | ', end='')
                        break
                else:
                    print('. | ', end='')
            print(f' {8-row}', end='')
        print("\n+" + "---+"*8)
        print('  ' + '   '.join('abcdefgh'))
        
if __name__ == '__main__':
    chess_handler = ChessHandler()
    
    board = chess_handler.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    chess_handler.display_board(board)
