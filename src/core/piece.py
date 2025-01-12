# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error

# standard
from typing import TypeAlias, List, Union

NoneIndex: TypeAlias = any

class CustomList(list):
    """ This class needs to be created since occasionally empty tiles are indexed and
    the Piece class needs to return something.

    """
    def __init__(self, elements: list, none_index: NoneIndex) -> None:
        self.none_index = none_index
        super().__init__(elements)
    
    def __getitem__(self, index: Union[int, None]) -> NoneIndex:
        if index is None:
            return self.none_index
        return super().__getitem__(index)

class Piece:
    """
    Since the Board class stores a list of bitboards that represent the pieces,
    this class simply contains a list of named bitboard indices.
    """
    PieceType: TypeAlias = int
    WHITE_PAWN:   PieceType = 0
    WHITE_KNIGHT: PieceType = 1
    WHITE_BISHOP: PieceType = 2
    WHITE_ROOK:   PieceType = 3
    WHITE_QUEEN:  PieceType = 4
    WHITE_KING:   PieceType = 5
    BLACK_PAWN:   PieceType = 6
    BLACK_KNIGHT: PieceType = 7
    BLACK_BISHOP: PieceType = 8
    BLACK_ROOK:   PieceType = 9
    BLACK_QUEEN:  PieceType = 10
    BLACK_KING:   PieceType = 11
    TYPES: List[PieceType] = list(range(12))
    SYMBOL = CustomList(["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"], ".")