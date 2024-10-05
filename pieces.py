# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

class Pieces:
    """
    Pieces are represented with 4 bits.
    - 1 bit for the color
    - 3 bits for the type
    """
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5
    WHITE = 0
    BLACK = 8
    
    DECODE = {
        0: "K", 1: "Q",  2: "R",  3: "B",  4: "N",  5: "P",
        8: "k", 9: "q", 10: "r", 11: "b", 12: "n", 13: "p"
    }
    
    ENCODE = {
        "K": 0, "Q": 1, "R":  2, "B":  3, "N":  4, "P":  5,
        "k": 8, "q": 9, "r": 10, "b": 11, "n": 12, "p": 13
    }