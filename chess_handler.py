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
from board import Board, Pieces
from move import Move

class ChessHandler:
    """ This class implements the rules of chess.
    """
    @staticmethod
    def make_move(move: Move, board: Board) -> Board:
        """ Plays a move on a board and returns a new board.
        - This function assumes that the move is legal

        Args:
            move (np.uint16): Information is at the top of the class
            bitboards (list[np.uint64]): A list of 12 bitboards

        Returns:
            list[np.uint64]: A list of 12 bitboards
        """
        if move.is_king_castle:
            if board.turn: # white to play
                # destroy squares e1, f1, g1 and h1 and place rook and king
                board.bitboards &= ~np.uint64(0xF0)
                board.bitboards[Pieces.WHITE_ROOK] |= np.uint64(1 << 5)
                board.bitboards[Pieces.WHITE_KING] = np.uint64(1 << 6)
            else:
                # destroy squares e8, f8, g8 and h8 and place rook and king
                board.bitboards &= ~np.uint64(15 << 60)
                board.bitboards[Pieces.BLACK_ROOK] |= np.uint64(1 << 61)
                board.bitboards[Pieces.BLACK_KING] = np.uint64(1 << 62)

        elif move.is_queen_castle:
            if board.turn:
                # destroy squares a1, b1, c1 and d1
                board.bitboards &= ~np.uint64(15)
                board.bitboards[Pieces.WHITE_KING] = np.uint64(1 << 2)
                board.bitboards[Pieces.WHITE_ROOK] |= np.uint64(1 << 3)
            else:
                board.bitboards &= ~np.uint64(15 << 56)
                board.bitboards[Pieces.BLACK_KING] = np.uint64(1 << 58)
                board.bitboards[Pieces.BLACK_ROOK] |= np.uint64(1 << 59)
        
        else:
            piece = board.get(move.initial_square)
            board.destroy(move.initial_square)
            if move.is_capture:
                board.destroy(move.target_square)
            if move.is_en_passant:
                board.destroy(move.target_square - 8)
            if move.is_promotion:
                if board.turn:
                    if (move.flags & 3) == 0:
                        board.place(move.target_square, Pieces.WHITE_KNIGHT)
                    if (move.flags & 3) == 1:
                        board.place(move.target_square, Pieces.WHITE_BISHOP)
                    if (move.flags & 3) == 2:
                        board.place(move.target_square, Pieces.WHITE_ROOK)
                    if (move.flags & 3) == 3:
                        board.place(move.target_square, Pieces.WHITE_QUEEN)
                else:
                    if (move.flags & 3) == 0:
                        board.place(move.target_square, Pieces.BLACK_KNIGHT)
                    if (move.flags & 3) == 1:
                        board.place(move.target_square, Pieces.BLACK_BISHOP)
                    if (move.flags & 3) == 2:
                        board.place(move.target_square, Pieces.BLACK_ROOK)
                    if (move.flags & 3) == 3:
                        board.place(move.target_square, Pieces.BLACK_QUEEN)
            else:
                board.place(move.target_square, piece)
    
        # increment turn
        board.turn = not board.turn
        
        return board