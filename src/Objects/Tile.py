import pygame as pg

class Tile:
    def __init__(self, screen, area, tile_num, color, rotated) -> None:
        self.screen = screen
        self.TILE_WIDTH = 36
        self.TILE_HEIGHT = 36
        self.TILE = color
        self.TILE_NUM = tile_num
        self.x = 0
        self.y = 0
        self.rotated = rotated
        self.has_been_centered = False
        self.dragging = False
        self.area = area
        self.used = False

    def draw(self) -> None:
        if not self.used and self.x != 0 and self.y != 0:
            for tile in range(self.TILE_NUM):
                if not self.rotated:
                    self.screen.blit(self.TILE, (self.x + (tile * (self.TILE_WIDTH + 7)), self.y))
                else:
                    self.screen.blit(self.TILE, (self.x, self.y + (tile * (self.TILE_HEIGHT + 7))))

    def update(self) -> None:
        if not self.used:
            if not self.rotated:
                tile_rect = pg.Rect(self.x, self.y, (self.TILE_NUM * (self.TILE_WIDTH + 7)), self.TILE_HEIGHT)
            else:
                tile_rect = pg.Rect(self.x, self.y, self.TILE_WIDTH, (self.TILE_NUM * (self.TILE_HEIGHT + 7)))
            # center when making tile appear
            if not self.has_been_centered:
                self.x = pg.display.get_surface().get_size()[0]/2 - tile_rect.width/2
                self.y = pg.display.get_surface().get_size()[1]/1.25 - tile_rect.height/2
                self.has_been_centered = True
            self.mouse_colliding = tile_rect.collidepoint(pg.mouse.get_pos())
            self.mouse_down = pg.mouse.get_pressed(num_buttons=3)[0]
            if self.mouse_down and self.mouse_colliding:
                self.dragging = True
            if not self.mouse_down:
                self.dragging = False
                self.area.get_tile_collision(tile_rect, self.TILE_NUM)
            if self.dragging:
                self.area.reset_collision_checks()
                if not self.rotated:
                    self.x, self.y = (pg.mouse.get_pos()[0] - (self.TILE_NUM * (self.TILE_WIDTH/2 + (7//3)))), (pg.mouse.get_pos()[1] - self.TILE_HEIGHT/2)
                else:
                    self.x, self.y = (pg.mouse.get_pos()[0] - self.TILE_WIDTH/2), (pg.mouse.get_pos()[1] - (self.TILE_NUM * (self.TILE_HEIGHT/2 + (7//3))))