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

class MoveMaker:
    """
    Performs chess moves on board objects
    Reference: https://www.chessprogramming.org/Move_Generation
    
    Example usage:
    test_board = Board.from_fen()
    test_move = Move(Flags.QUIET, squares.E2, squares.E4)
    test_board = MoveMaker.push(test_move)
    """
    white_promotion = {
        0: Piece.WHITE_KNIGHT,
        1: Piece.WHITE_BISHOP,
        2: Piece.WHITE_ROOK,
        3: Piece.WHITE_QUEEN
    }
    
    black_promotion = {
        0: Piece.BLACK_KNIGHT,
        1: Piece.BLACK_BISHOP,
        2: Piece.BLACK_ROOK,
        3: Piece.BLACK_QUEEN
    }
    
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
        
        # move the piece with xor
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
        
        # move the piece with xor
        bitboards[piece_type] ^= BB_MASK[move.initial_square] | BB_MASK[move.target_square]
        
        # destroy the piece at the target square
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
    
    @classmethod
    def promotion(cls, board: Board, move: Move) -> Board:
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
            # delete initial pawn
            bitboards[Piece.WHITE_PAWN] &= ~BB_MASK[move.initial_square]
            
            # add promoted piece
            bitboards[cls.white_promotion[promotion_encoding]] |= BB_MASK[move.target_square]
        else:
            # delete initial pawn
            bitboards[Piece.BLACK_PAWN] &= ~BB_MASK[move.initial_square]
            
            # add promoted piece
            bitboards[cls.black_promotion[promotion_encoding]] |= BB_MASK[move.target_square]
        
        return new_board
    
    @classmethod
    def promotion_capture(cls, board: Board, move: Move) -> Board:
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
        
        # delete target square
        bitboards[piece_to_capture] &= ~BB_MASK[move.target_square]
        
        if new_board.turn:
            # delete initial pawn
            bitboards[Piece.WHITE_PAWN] &= ~BB_MASK[move.initial_square]
            
            # add promoted piece
            bitboards[cls.white_promotion[promotion_encoding]] |= BB_MASK[move.target_square]
        else:
            # delete initial pawn
            bitboards[Piece.BLACK_PAWN] &= ~BB_MASK[move.initial_square]
            
            # add promoted piece
            bitboards[cls.black_promotion[promotion_encoding]] |= BB_MASK[move.target_square]
        
        return new_board
    
    @classmethod
    def push(cls, board: Board, move: Move) -> Board:
        """ Plays a move on the board
        Please note that this function does not check if the flags on the move
        are correct, please ensure that the flags and the move data are legal
        for the given board state.

        Args:
            board (Board): The board to operate on.
            move (Move): The move data.

        Returns:
            Board: The resultant board object.
        """
        if move.is_quiet or move.is_double_pawn_push:
            return cls.quiet(board, move)
        elif move.is_capture:
            return cls.capture(board, move)
        elif move.is_short_castle:
            return cls.short_castle(board)
        elif move.is_long_castle:
            return cls.long_castle(board)
        elif move.is_promotion:
            return cls.promotion(board, move)
        elif move.is_promotion_capture:
            return cls.promotion_capture(board, move)
        elif move.is_en_passant:
            return cls.en_passant(board, move)