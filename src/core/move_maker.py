# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=line-too-long

# project
from src.core.squares import BB_MASK
from src.core.piece import Piece
from src.core.board import Board
from src.core.move import Move
from src.core import squares

# TODO: change piece encodings to make this code less redundant.

class MoveMaker:
    """
    Performs chess moves on board objects
    Reference: https://www.chessprogramming.org/Move_Generation
    """
    @staticmethod
    def quiet(board: Board, move: Move) -> Board:
        """ Performs a quiet move on the board.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        
        piece_type = new_board.get_piece(move.initial_square)
        bitboards[piece_type] ^= BB_MASK[move.initial_square] | BB_MASK[move.target_square]
        
        return new_board

    @staticmethod
    def capture(board: Board, move: Move) -> Board:
        """ Performs a quiet move on the board.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        
        piece_type = new_board.get_piece(move.initial_square)
        piece_to_capture = new_board.get_piece(move.target_square)
        bitboards[piece_type] ^= BB_MASK[move.initial_square] | BB_MASK[move.target_square]
        bitboards[piece_to_capture] &= ~BB_MASK[move.target_square]
        
        return new_board
    
    @staticmethod
    def short_castle(board: Board) -> Board:
        """ Performs a short castling move on the board.

        Args:
            board (Board): The board to operate on.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        
        if new_board.turn:
            bitboards[Piece.WHITE_KING] = squares.MASK_G1
            bitboards[Piece.WHITE_ROOK] ^= squares.MASK_H1 | squares.MASK_F1
        else:
            bitboards[Piece.BLACK_KING] = squares.MASK_G8
            bitboards[Piece.BLACK_ROOK] ^= squares.MASK_H8 | squares.MASK_F8
        
        return new_board
    
    @staticmethod
    def long_castle(board: Board) -> Board:
        """ Performs a long castling move on the board.

        Args:
            board (Board): The board to operate on.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        
        if new_board.turn:
            bitboards[Piece.WHITE_KING] = squares.MASK_C1
            bitboards[Piece.WHITE_ROOK] ^= squares.MASK_A1 | squares.MASK_D1
        else:
            bitboards[Piece.BLACK_KING] = squares.MASK_C8
            bitboards[Piece.BLACK_ROOK] ^= squares.MASK_A8 | squares.MASK_D8
        
        return new_board
    
    @staticmethod
    def en_passant(board: Board, move: Move) -> Board:
        """ Performs an en passant move on the board.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        
        if new_board.turn:
            bitboards[Piece.WHITE_PAWN] ^= BB_MASK[move.initial_square] | BB_MASK[move.target_square]
            bitboards[Piece.BLACK_PAWN] &= ~BB_MASK[move.target_square - 8]
        else:
            bitboards[Piece.BLACK_PAWN] ^= BB_MASK[move.initial_square] | BB_MASK[move.target_square]
            bitboards[Piece.WHITE_PAWN] &= ~BB_MASK[move.target_square + 8]
        
        return new_board
    
    @staticmethod
    def promotion(board: Board, move: Move) -> Board:
        """ Performs a promotion move on the board.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        promotion_encoding = move.flags & 3
        
        if new_board.turn:
            bitboards[Piece.WHITE_PAWN] &= ~BB_MASK[move.initial_square]
            if promotion_encoding == 0:
                bitboards[Piece.WHITE_KNIGHT] |= BB_MASK[move.target_square]
            elif promotion_encoding == 1:
                bitboards[Piece.WHITE_BISHOP] |= BB_MASK[move.target_square]
            elif promotion_encoding == 2:
                bitboards[Piece.WHITE_ROOK] |= BB_MASK[move.target_square]
            elif promotion_encoding == 3:
                bitboards[Piece.WHITE_QUEEN] |= BB_MASK[move.target_square]
        else:
            bitboards[Piece.BLACK_PAWN] &= ~BB_MASK[move.initial_square]
            if promotion_encoding == 0:
                bitboards[Piece.BLACK_KNIGHT] |= BB_MASK[move.target_square]
            elif promotion_encoding == 1:
                bitboards[Piece.BLACK_BISHOP] |= BB_MASK[move.target_square]
            elif promotion_encoding == 2:
                bitboards[Piece.BLACK_ROOK] |= BB_MASK[move.target_square]
            elif promotion_encoding == 3:
                bitboards[Piece.BLACK_QUEEN] |= BB_MASK[move.target_square]
        
        return new_board
    
    @staticmethod
    def promotion_capture(board: Board, move: Move) -> Board:
        """ Performs a promotion move on the board.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        new_board = board.copy()
        bitboards = new_board.bitboards
        promotion_encoding = move.flags & 3
        piece_to_capture = new_board.get_piece(move.target_square)
        
        bitboards[piece_to_capture] &= ~BB_MASK[move.target_square]
        
        if new_board.turn:
            bitboards[Piece.WHITE_PAWN] &= ~BB_MASK[move.initial_square]
            if promotion_encoding == 0:
                bitboards[Piece.WHITE_KNIGHT] |= BB_MASK[move.target_square]
            elif promotion_encoding == 1:
                bitboards[Piece.WHITE_BISHOP] |= BB_MASK[move.target_square]
            elif promotion_encoding == 2:
                bitboards[Piece.WHITE_ROOK] |= BB_MASK[move.target_square]
            elif promotion_encoding == 3:
                bitboards[Piece.WHITE_QUEEN] |= BB_MASK[move.target_square]
        else:
            bitboards[Piece.BLACK_PAWN] &= ~BB_MASK[move.initial_square]
            if promotion_encoding == 0:
                bitboards[Piece.BLACK_KNIGHT] |= BB_MASK[move.target_square]
            elif promotion_encoding == 1:
                bitboards[Piece.BLACK_BISHOP] |= BB_MASK[move.target_square]
            elif promotion_encoding == 2:
                bitboards[Piece.BLACK_ROOK] |= BB_MASK[move.target_square]
            elif promotion_encoding == 3:
                bitboards[Piece.BLACK_QUEEN] |= BB_MASK[move.target_square]
        
        return new_board