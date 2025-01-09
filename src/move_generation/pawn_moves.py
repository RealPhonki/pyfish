# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error

# standard
from typing import List

# project
from src.core.bitboard import Bitboard
from src.core.piece import Piece
from src.core.board import Board
from src.core.move import Move, Flags

from src.core import squares

class PawnMoves:
    """ Handles all legal pawn move generation for a given board state """
    @staticmethod
    def _white_get_quiet(board: Board) -> List[Move]:
        legal_moves = []
        
        # get all empty squares
        occupied = board.get_occupied()
        empty = ~occupied
        
        # get all the white pawns on the board, ignore all pawns that will promote
        pawns = board.bitboards[Piece.WHITE_PAWN] & ~squares.MASK_RANK_7
        
        # shift the white pawns bitboard upwards by one tile and destroy those that
        # collide with other pieces, this generates a list of squares that pawns
        # can move to without capturing.
        single_push_targets = (pawns << 8) & empty
        
        # then we loop through each of the pawn targets and generate legal moves
        for square in squares.PAWN_SQUARES:
            if (single_push_targets & Bitboard(1 << square)) != 0:
                legal_moves.append(Move(Flags.QUIET, square - 8, square))
        
        # get all pawns that reached the third rank after moving once, shift them
        # upwards by one tile, and destroy those that collide with other pieces.
        # This generates a list of tiles that pawns can move to with a double
        # pawn push
        double_push_targets = ((single_push_targets & squares.MASK_RANK_3) << 8) & empty
        
        # loop through the fourth rank (the double pawn push rank) and generate legal moves
        for square in squares.RANK_4:
            if (double_push_targets & Bitboard(1 << square)) != 0:
                legal_moves.append(Move(Flags.QUIET, square - 16, square))
        
        return legal_moves
    
    @staticmethod
    def _black_get_quiet(board: Board) -> List[Move]:
        legal_moves = []
        
        # get all empty squares
        occupied = board.get_occupied()
        empty = ~occupied
        
        # get all the black pawns on the board, ignore all pawns that will promote
        pawns = board.bitboards[Piece.BLACK_PAWN] & ~squares.MASK_RANK_2
        
        # shift the black pawns bitboard downwards by one tile and destroy those that
        # collide with other pieces, this generates a list of squares that pawns
        # can move to without capturing.
        single_push_targets = (pawns >> 8) & empty
        
        # then we loop through each of the pawn targets and generate legal moves
        for square in squares.PAWN_SQUARES:
            if (single_push_targets & Bitboard(1 << square)) != 0:
                legal_moves.append(Move(Flags.QUIET, square + 8, square))
        
        # get all pawns that reached the sixth rank after moving once, shift them
        # downwards by one tile, and destroy those that collide with other pieces.
        # This generates a list of tiles that pawns can move to with a double
        # pawn push
        double_push_targets = ((single_push_targets & squares.MASK_RANK_6) >> 8) & empty
        
        # loop through the fifth rank (the double pawn push rank) and generate legal moves
        for square in squares.RANK_5:
            if (double_push_targets & Bitboard(1 << square)) != 0:
                legal_moves.append(Move(Flags.QUIET, square + 16, square))
        
        return legal_moves
    
    @classmethod
    def get(cls, board: Board) -> List[Move]:
        """ Generates all legal pawn moves for a given board state
        reference: https://www.chessprogramming.org/Pawn_Pattern_and_Properties

        Args:
            board (Board): The board state represented with a board object

        Returns:
            List[Move]: A list of legal moves
        """
        if board.turn:
            single_push_moves = cls._white_get_quiet(board)
        else:
            single_push_moves = cls._black_get_quiet(board)
        
        return single_push_moves