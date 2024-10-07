# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

# this file is a temporary interface for the chess program

import os
import pyfish_handler as pf

def encode_uci(move: str, flags: int) -> pf.Move:
    """ Converts UCI format to an encoded Move object

    Args:
        move (str): A given move in UCI format

    Returns:
        Move: A move object
    """
    LETTERS_TO_SYMBOLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    initial_square = LETTERS_TO_SYMBOLS[move[0]] + 8 * (int(move[1]) - 1)
    target_square = LETTERS_TO_SYMBOLS[move[2]] + 8 * (int(move[3]) - 1)
    return pf.Move(flags, initial_square, target_square)

def main():
    """ A basic interface for testing """
    board = pf.Board()
    
    while True:
        os.system("clear")
        print(board)
        print("-" * 33)
        print("0  | Quiet  Move")
        print("1  | Double Pawn Push")
        print("2  | Short Castle")
        print("3  | Long Castle")
        print("4  | Capture")
        print("5  | En Passant")
        print("8  | Knight Promotion")
        print("7  | Bishop Promotion")
        print("9  | Rook Promotion")
        print("10 | Queen Promotion")
        print("11 | Knight Promotion Capture")
        print("12 | Bishop Promotion Capture")
        print("13 | Rook Promotion Capture")
        print("14 | Queen Promotion Capture")
        print("-" * 33)
        flags = int(input("Flags > "))
        move = encode_uci(input("Move > "), flags)
        board = board.make_move(move)
    
if __name__ == '__main__':
    main()