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
    def display_bitboard(bitboard: np.uint64) -> None:
        """ Displays the given bitboard to the CLI

        Args:
            bitboard (np.uint64): the 64 bit board to display
        """
        bitboard = bin(bitboard)[2:].rjust(64, '0')
        for row in range(8):
            for tile in range(7, -1, -1):
                print(f'{bitboard[row*8+tile]} ', end='')
            print(f'| {8-row}')
        print('----------------+')
        print('a b c d e f g h')
    
    @staticmethod
    def display_board(board: list[np.uint64]) -> None:
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
                for bitboard_index in range(len(board)):
                    if bin(board[bitboard_index])[2:].rjust(64, '0')[row*8+tile] == '1':
                        print(f'{SYMBOL_FROM_INDEX[bitboard_index]} | ', end='')
                        break
                else:
                    print('. | ', end='')
            print(f' {8-row}', end='')
        print("\n+" + "---+"*8)
        print('  ' + '   '.join('abcdefgh'))
        
if __name__ == '__main__':
    test_board = np.array([
        np.uint64(0x0000000000000010), #K
        np.uint64(0x0000000000000008), #Q
        np.uint64(0x0000000000000081), #R
        np.uint64(0x0000000000000024), #B
        np.uint64(0x0000000000000042), #N
        np.uint64(0x000000000000FF00), #P
        np.uint64(0x1000000000000000), #k
        np.uint64(0x0800000000000008), #q
        np.uint64(0x8100000000000081), #r
        np.uint64(0x2400000000000024), #b
        np.uint64(0x4200000000000042), #n
        np.uint64(0x00FF000000000000)  #p
    ], dtype=np.uint64)
    
    chess_handler = ChessHandler()
    chess_handler.display_board(test_board)