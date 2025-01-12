# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=no-member

# third party
import pygame as pg

# project
from src.core.board import Board
from src.core.move import Move
from src.core.move_maker import MoveMaker

from src.renderer.board_renderer import BoardRenderer
from src.renderer.mouse import Mouse

# TODO: Make orientation change with each move if the mode is player v player

class App:
    """ Is the highest level wrapper for the program"""
    def __init__(
        self,
        white: callable,
        black: callable,
        position: str,
        screen_size: pg.Vector2,
        orientation: bool
    ) -> None:
        # reference
        self.white = white
        self.black = black
        
        # constants
        self.FPS = 20
        self.RES = self.WIDTH, self.HEIGHT = screen_size
        self.TILE_SIZE = (min(screen_size) * 0.95) // 8
        
        # attributes
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        
        self.orientation = orientation
        self.last_move = None
        
        # subclass initialization
        self.board = Board.from_fen(position)
        self.board_renderer = BoardRenderer(
            self.screen,
            self.orientation,
            self.board,
            pg.Vector2(self.WIDTH // 2, self.HEIGHT // 2),
            self.TILE_SIZE
        )
    
        self.mouse = Mouse(self.board, self.board_renderer)
        self.mouse.on_request_move(self.play_move)
        
        self.board_renderer.refresh(self.board, self.mouse)
        pg.display.update()
    
    def play_move(self, move: Move) -> None:
        """ Plays a given move on the board

        Args:
            move (Move): The move to play
        """
        self.board = MoveMaker.push(self.board, move)
        self.mouse.save_last_move_square(move.target_square)
        self.board_renderer.refresh(self.board, self.mouse)
        self.mouse.update_board_state(self.board)
        
        pg.display.update()
    
    def handle_events(self) -> None:
        """ Loops through all pygame events. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse.click()
                self.board_renderer.refresh(self.board, self.mouse)
                pg.display.update()
    
    def run(self) -> None:
        """ Is the main loop for the program """
        while True:
            self.handle_events()

            pg.display.set_caption("Pyfish")
            self.clock.tick(self.FPS)