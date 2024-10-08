# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=import-error

# third-party
import numpy as np

# project
from bit_master import BitMaster
from pieces import Pieces
from board import Board
from move import Move

class MoveMaker:
    """ Handles the manipulation of board objects to represent move making
    """
    @staticmethod
    def quiet(board: Board, move: Move) -> Board:
        """ Performs a quiet move

        Args:
            board (Board): The board to operate on
            move (Move): Data regarding the move
        """
        new_board = board.deepcopy()
        piece = BitMaster.get(board, move.initial_square)
        BitMaster.destroy(board, move.initial_square)
        BitMaster.place(board, move.target_square, piece)
        new_board.update_bitboard_info()
        return new_board

    @staticmethod
    def short_castle(board: Board) -> Board:
        """ Performs a short-castle

        Args:
            board (Board): The board to operate on
        """
        # choose side and color
        row = 0 if board.turn else 7
        color = Pieces.WHITE if board.turn else Pieces.BLACK
        
        new_board = board.deepcopy()
        new_board &= ~np.uint64(15 << (4 + row*8))
        new_board[color | Pieces.ROOK] |= np.uint64(1 << (5 + row*8))
        new_board[color | Pieces.KING]  = np.uint64(1 << (6 + row*8))
        new_board.update_bitboard_info()
        return new_board
    
    @staticmethod
    def long_castle(board: Board) -> Board:
        """ Performs a long-castle

        Args:
            board (Board): The board to operate on
        """
        row = 0 if board.turn else 7
        color = Pieces.WHITE if board.turn else Pieces.black
        
        new_board = board.deepcopy()
        new_board &= ~np.uint64(15 << (row*8))
        new_board[color | Pieces.KING] = np.uint64(1 << (2 + row*8))
        new_board[color | Pieces.ROOK] |= np.uint64(1 << (3 + row*8))
        new_board.update_bitboard_info()
        return new_board
    
    @staticmethod
    def capture(board: Board, move: Move) -> Board:
        """ Performs a capture move

        Args:
            board (Board): The board to operate on
        """
        new_board = board.deepcopy()
        piece = BitMaster.get(board, move.initial_square)
        BitMaster.destroy(board, move.initial_square)
        BitMaster.destroy(board, move.target_square)
        BitMaster.place(board, move.target_square, piece)
        new_board.update_bitboard_info()
        return new_board
    
    @staticmethod
    def en_passant(board: Board, move: Move) -> Board:
        """ Performs an en passant capture

        Args:
            board (Board): The board to operate on
        """
        new_board = board.deepcopy()
        piece = BitMaster.get(board, move.initial_square)
        BitMaster.destroy(board, move.initial_square)
        BitMaster.destroy(board, int(move.target_square) + (8 * (-1 if board.turn else 1)))
        BitMaster.place(board, move.target_square, piece)
        new_board.update_bitboard_info()
        return new_board
    
    @staticmethod
    def promotion(board: Board, move: Move) -> Board:
        """ Performs a promotion move

        Args:
            board (Board): The board to operate on
        """
        color = Pieces.WHITE if board.turn else Pieces.BLACK
        piece = [Pieces.KNIGHT, Pieces.BISHOP, Pieces.ROOK, Pieces.QUEEN][move.flags & 3]
        
        new_board = board.deepcopy()
        BitMaster.destroy(board, move.initial_square)
        BitMaster.place(board, move.target_square, color | piece)
        new_board.update_bitboard_info()
        return new_board
    
    @staticmethod
    def promotion_capture(board: Board, move: Move) -> Board:
        """ Performs a promotion-capture move

        Args:
            board (Board): The board to operate on
        """
        color = Pieces.WHITE if board.turn else Pieces.BLACK
        piece = [Pieces.KNIGHT, Pieces.BISHOP, Pieces.ROOK, Pieces.QUEEN][move.flags & 3]
        
        new_board = board.deepcopy()
        BitMaster.destroy(board, move.initial_square)
        BitMaster.destroy(board, move.target_square)
        BitMaster.place(board, move.target_square, color | piece)
        new_board.update_bitboard_info()
        return new_board
    
    def make_move(self, board: Board, move: Move) -> Board:
        """ Plays a given move

        Args:
            move (Move): the move to play

        Returns:
            Self: A copy of the board with the move applied
        """
        if move.is_quiet or move.is_double_pawn_push:
            return self.quiet(board, move)
        elif move.is_short_castle:
            return self.short_castle(board)
        elif move.is_long_castle:
            return self.long_castle(board)
        elif move.is_en_passant:
            return self.en_passant(board, move)
        elif move.is_promotion:
            return self.promotion(board, move)
        elif move.is_capture:
            return self.capture(board, move)
        else:
            raise ValueError(f"Invalid move data: {move}")

if __name__ == '__main__':
    # quiet test
    test_board = Board()
    MoveMaker.quiet(test_board, Move(0, 12, 28))
    #print(test_board)
    
    # long castle test
    test_board = Board("r2qkb1r/ppp1pppp/2n1bn2/6B1/2pP4/2N5/PPQ1PPPP/R3KBNR w KQkq - 6 6")
    MoveMaker.short_castle(test_board)
    #print(test_board)
    
    # short castle test
    test_board = Board("r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    MoveMaker.long_castle(test_board)
    #print(test_board)
    
    # capture test
    test_board = Board("rnbqkb1r/pppp1ppp/8/4P3/3pn3/5N2/PPP2PPP/RNBQKB1R w KQkq - 1 5")
    MoveMaker.capture(test_board, Move(4, 3, 27))
    #print(test_board)
    
    # en passant test
    test_board = Board("rnbqkb1r/ppp2ppp/8/3pP3/3Qn3/5N2/PPP2PPP/RNB1KB1R w KQkq d6 0 6")
    MoveMaker.en_passant(test_board, Move(5, 36, 43))
    #print(test_board)
    
    # promotion test
    test_board = Board("2q2K2/5P1k/5Qpp/p2p4/3P4/P2b2P1/5K1P/1r6 w - - 0 1")
    MoveMaker.promotion_capture(test_board, Move(15, 53, 61))
    print(test_board)