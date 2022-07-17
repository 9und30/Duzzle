import pygame as pg
from .TileImages import *

from .Tile import Tile
from .Dice import Dice
from ..GameOver import GameOver

import random
import sys

class Area:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.TILE_WIDTH = 36
        self.TILE_HEIGHT = 36
        self.TOP_OFFSET = 24
        self.TILE_MARGIN = 7

        self.score = 0
        # load font
        self.font = pg.font.Font('assets/font/BalsamiqSans-Bold.ttf', 48)
        self.score_text = self.font.render(str(self.score), True, (32, 25, 63))
        self.plop = pg.mixer.Sound('assets/sound/plop.ogg')
        self.full_plop = pg.mixer.Sound('assets/sound/full_plop.ogg')
        self.full_plop.set_volume(0.1)
        pg.mixer.music.load('assets/sound/music.ogg')
        pg.mixer.music.play(-1)

        self.TILES = [EMPTY_TILE, GREY_TILE, BEIGE_TILE, ORANGE_TILE, PINK_TILE, GREEN_TILE, RED_TILE]
        self.tile = None
        self.curr_color = None
        self.area = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.tile_collision_check_count = 0
        self.to_be_filled = set([])

        self.roll_dice()

        self.sound_on = True
        self.sound_mute_pressable = True
        self.music_on = True
        self.music_mute_pressable = True

        self.is_game_over = False
        self.game_over = GameOver(self.screen, self.score, self.restart_game)

    def init_tile(self, num) -> None:
        rotated = bool(random.randint(0, 1))
        self.curr_color = num
        self.tile = Tile(self.screen, self, self.curr_color, self.TILES[self.curr_color], rotated)
        if not self.check_if_possible():
            self.is_game_over = True
            self.game_over.score = self.score

    def draw(self) -> None:
        self.screen.blit(self.score_text, (90 - self.score_text.get_width()//2, (pg.display.get_surface().get_size()[1]//2) - (self.score_text.get_height()//2) ))
        for row in range(len(self.area)):
            for col in range(len(self.area[row])):
                if self.area[row][col] == 0:
                    self.screen.blit(EMPTY_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 1:
                    self.screen.blit(GREY_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 2:
                    self.screen.blit(BEIGE_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 3:
                    self.screen.blit(ORANGE_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 4:
                    self.screen.blit(PINK_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 5:
                    self.screen.blit(GREEN_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))
                if self.area[row][col] == 6:
                    self.screen.blit(RED_TILE, (((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN))))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN))))

        if self.tile:
            self.tile.draw()

        self.screen.blit(SOUND_MUTE, (pg.display.get_surface().get_size()[0] - SOUND_MUTE.get_width() - SOUND_MUTE.get_width()//2, (pg.display.get_surface().get_size()[1]//2) - (SOUND_MUTE.get_height()*1.25)))
        self.screen.blit(MUSIC_MUTE, (pg.display.get_surface().get_size()[0] - MUSIC_MUTE.get_width() - MUSIC_MUTE.get_width()//2, (pg.display.get_surface().get_size()[1]//2) + (MUSIC_MUTE.get_height()*0.25)))

        self.dice.draw()


        if self.is_game_over:
            self.game_over.draw()
        
    def update(self) -> None:
        self.score_text = self.font.render(str(self.score), True, (32, 25, 63))

        # mute buttons
        self.sound_mute_btn_rect = pg.Rect(pg.display.get_surface().get_size()[0] - SOUND_MUTE.get_width() - SOUND_MUTE.get_width()//2, (pg.display.get_surface().get_size()[1]//2) - (SOUND_MUTE.get_height()*1.25), SOUND_MUTE.get_width(), SOUND_MUTE.get_height())
        self.music_mute_btn_rect = pg.Rect(pg.display.get_surface().get_size()[0] - MUSIC_MUTE.get_width() - MUSIC_MUTE.get_width()//2, (pg.display.get_surface().get_size()[1]//2) + (SOUND_MUTE.get_height()*0.25), MUSIC_MUTE.get_width(), MUSIC_MUTE.get_height())
        if self.sound_mute_btn_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
            if self.sound_mute_pressable:
                if self.sound_on:
                    self.sound_on = False
                else:
                    self.sound_on = True
                self.make_pressable(self.sound_mute_pressable)
        if self.music_mute_btn_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
            if self.music_mute_pressable:
                if self.music_on:
                    self.music_on = False
                else:
                    self.music_on = True
                self.make_pressable(self.music_mute_pressable)

        # play music if music is on
        if self.music_on:
            if not pg.mixer.music.get_busy():
                pg.mixer.music.unpause()
        else:
            if pg.mixer.music.get_busy():
                pg.mixer.music.pause()

        if not self.is_game_over:
            if self.tile:
                self.tile.update()
                self.dice.update(self.sound_on, self.tile.used)
            else:
                self.dice.update(self.sound_on)
        
            self.check_for_row_fullness()
            self.check_for_col_fullness()
        else:
            self.game_over.update()

    def restart_game(self):
        self.score = 0
        self.reset_area()
        self.tile.used = True
        self.is_game_over = False

    def make_pressable(self, btn) -> None:
        if btn == self.sound_mute_pressable:
            self.sound_mute_pressable = False
            pg.time.wait(500)
            self.sound_mute_pressable = True
        elif btn == self.music_mute_pressable:
            self.music_mute_pressable = False
            pg.time.wait(500)
            self.music_mute_pressable = True

    def get_tile_collision(self, rect, tile_num) -> None:
        for row in range(len(self.area)):
            for col in range(len(self.area[row])):
                if self.area[row][col] == 0:
                    tile_rect = pg.Rect((col * (self.TILE_WIDTH + self.TILE_MARGIN)) + ((pg.display.get_surface().get_size()[0] - len(self.area[0]*(self.TILE_WIDTH+self.TILE_MARGIN)))/2), self.TOP_OFFSET + (row * (self.TILE_WIDTH + self.TILE_MARGIN)), self.TILE_WIDTH, self.TILE_HEIGHT)
                    if tile_rect.colliderect(rect):
                        # stick tile to nearest empty tile (collision of middle of tile will be considered)
                        if ((tile_rect.left + self.TILE_WIDTH/2) > rect.left and (tile_rect.left + self.TILE_WIDTH/2) < rect.right) and ((tile_rect.top + self.TILE_HEIGHT/2) > rect.top and (tile_rect.top + self.TILE_HEIGHT/2) < rect.bottom):
                            # turn empty tile into filled tile
                            self.to_be_filled.add((row, col))
                            self.tile_collision_check_count += 1
                            if self.tile_collision_check_count == tile_num and len(self.to_be_filled) == tile_num:
                                for tile in self.to_be_filled:
                                    self.area[tile[0]][tile[1]] = self.curr_color
                                    self.score += 1
                                self.reset_collision_checks()
                                self.tile.used = True
                                if self.sound_on:
                                    pg.mixer.Sound.play(self.plop)

    def reset_collision_checks(self) -> None:
        self.tile_collision_check_count = 0
        self.to_be_filled.clear()

    def check_for_row_fullness(self) -> None:
        # loops through each row and checks if theres no 0s in it
        for row in self.area:
            if 0 not in row:
                for i in range(len(row)):
                    row[i] = 0
                    if self.sound_on:
                        pg.mixer.Sound.play(self.full_plop)

    def check_for_col_fullness(self) -> None:
        # idk copilot did this and it works dont ask me why and how
        for col in range(len(self.area[0])):
            col_list = []
            for row in self.area:
                col_list.append(row[col])
            if 0 not in col_list:
                for i in range(len(col_list)):
                    self.area[i][col] = 0
                    pg.mixer.Sound.play(self.full_plop)

    # ATTENTION: reading this code may give you a seizure but it works and i dont know why and how i just kind of hacked it together
    # I finally got the idea after a 15 minute nap
    # Not even copilot could figure out how to make this work so dont even question it lol
    def check_if_possible(self) -> None:
        if not self.tile.rotated:
            row_count = 0
            max_row_count = 0
            for i, row in enumerate(self.area):
                for j, tile in enumerate(row):
                    if tile == 0:
                        row_count += 1
                        if row_count > max_row_count:
                            max_row_count = row_count
                    else:
                        if row_count > max_row_count:
                            max_row_count = row_count
                        row_count = 0
                row_count = 0
            if max_row_count >= self.tile.TILE_NUM:
                return True
            else:
                return False
        if self.tile.rotated:
            col_count = 0
            max_col_count = 0
            cols = [[], [], [], [], [], [], [], [], [], []]
            for i, row in enumerate(self.area):
                for j, tile in enumerate(row):
                    cols[j].append(tile)
            for col in cols:
                for tile in col:
                    if tile == 0:
                        col_count += 1
                        if col_count > max_col_count:
                            max_col_count = col_count
                    else:
                        if col_count > max_col_count:
                            max_col_count = col_count
                        col_count = 0
                col_count = 0
            if max_col_count >= self.tile.TILE_NUM:
                return True
            else:
                return False

    def roll_dice(self) -> None:
        self.dice = Dice(self.screen, self.init_tile)

    def reset_area(self) -> None:
        self.area = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]