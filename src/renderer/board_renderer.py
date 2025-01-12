# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=line-too-long

# standard
from __future__ import annotations
from typing import TYPE_CHECKING

# third party
import pygame as pg

# project
from src.core.squares import WHITE
from src.core.board import Board

if TYPE_CHECKING:
    from src.renderer.mouse import Mouse

class BoardRenderer:
    """ Handles game state rendering """
    
    def __init__(
        self,
        screen: pg.Surface,
        orientation: bool,
        board: Board,
        center: pg.Vector2,
        tile_size: int
    ) -> None:
        # reference
        self.screen = screen
        self.orientation = orientation
        self.board = board
        
        # constants
        self.TILE_SIZE = tile_size
        self.BACKGROUND = self._load_background()
        self.POSITION = center - self.BACKGROUND.get_rect().center
        self.SPRITES = [
            pg.transform.smoothscale(
                pg.image.load(f"assets/pieces/{i}.png").convert_alpha(),
                (self.TILE_SIZE, self.TILE_SIZE)
            ) for i in range(12)
        ]
        
        # attributes
        self.pieces = self._load_pieces()
        
    def _load_background(self) -> pg.Surface:
        """ Returns a surface with a checkboard pattern

        Returns:
            pg.Surface: The surface with the checkboard pattern
        """
        surface = pg.Surface((self.TILE_SIZE * 8, self.TILE_SIZE * 8), pg.SRCALPHA)
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    color = (238,238,210)
                else:
                    color = (118,150,86)
                pg.draw.rect(surface, color, (
                    x * self.TILE_SIZE,
                    y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE,
                ))
        return surface

    def _load_pieces(self) -> pg.Surface:
        """ Returns a surface with the pieces blitted onto it

        Returns:
            pg.Surface: The surface with the pieces blitted onto it
        """
        surface = pg.Surface((self.TILE_SIZE * 8, self.TILE_SIZE * 8), pg.SRCALPHA)
        for y in range(8):
            for x in range(8):
                if self.orientation == WHITE:
                    piece = self.board.get_piece(x + (7 - y) * 8)
                else:
                    piece = self.board.get_piece((7 - x) + y * 8)
                if piece is None:
                    continue
                surface.blit(self.SPRITES[piece], (x * self.TILE_SIZE, y * self.TILE_SIZE))
        return surface
    
    def refresh(self, board: Board, mouse: Mouse) -> None:
        """ Refreshes the board """
        self.board = board
        self.pieces = self._load_pieces()
        self.render()
        
        print(mouse.last_move_square, mouse.selected_square)
        
        if mouse.last_move_square is not None:
            if self.orientation:
                pg.draw.rect(self.screen, (255, 255, 0), (
                    int(mouse.last_move_square % 8 * self.TILE_SIZE) + self.POSITION.x,
                    int((7 - mouse.last_move_square // 8) * self.TILE_SIZE) + self.POSITION.y,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                ), int(self.TILE_SIZE * 0.04))
            else:
                pg.draw.rect(self.screen, (255, 255, 0), (
                    int((7 - mouse.last_move_square % 8) * self.TILE_SIZE) + self.POSITION.x,
                    int(mouse.last_move_square // 8 * self.TILE_SIZE) + self.POSITION.y,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                ), int(self.TILE_SIZE * 0.04))
        
        if mouse.selected_square is not None:
            if self.orientation:
                pg.draw.rect(self.screen, (255, 255, 255), (
                    int(mouse.selected_square % 8 * self.TILE_SIZE) + self.POSITION.x,
                    int((7 - mouse.selected_square // 8) * self.TILE_SIZE) + self.POSITION.y,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                ), int(self.TILE_SIZE * 0.04))
            else:
                pg.draw.rect(self.screen, (255, 255, 255), (
                    int((7 - mouse.selected_square % 8) * self.TILE_SIZE) + self.POSITION.x,
                    int(mouse.selected_square // 8 * self.TILE_SIZE) + self.POSITION.y,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                ), int(self.TILE_SIZE * 0.04))
    
    def render(self) -> None:
        """ Renders the chessboard to the screen """
        self.screen.blit(self.BACKGROUND, self.POSITION)
        self.screen.blit(self.pieces, self.POSITION)