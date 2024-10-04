# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

import os
from chess_handler import ChessHandler
from board import Board
from move import Move

def coordinate_to_butterfly(x: int, y: int) -> int:
    """ Converts a coordinate to butterfly coordinates

        Args:
            x (int): The x coordinate
            y (int): The y coordinate

        Returns:
            int: The butterfly coordinate (a number from 0 to 63)
        """
    return y * 8 + x
    
def encode_uci(move: str) -> Move:
    """ Converts UCI format to an encoded Move object

    Args:
        move (str): A given move in UCI format

    Returns:
        Move: A move object
    """
    LETTERS_TO_SYMBOLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    initial_square = LETTERS_TO_SYMBOLS[move[0]] + 8 * (int(move[1]) - 1)
    target_square = LETTERS_TO_SYMBOLS[move[2]] + 8 * (int(move[3]) - 1)
    return Move(0, initial_square, target_square)

def main():
    """ A basic interface for testing """
    chess_handler = ChessHandler()
    board = Board()
    
    while True:
        os.system("clear")
        print(board)
        user_input = input("> ")
        chess_handler.make_move(encode_uci(user_input), board)
    
if __name__ == '__main__':
    main()