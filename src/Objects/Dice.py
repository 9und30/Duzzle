import pygame as pg
from .DiceImages import *

import random

class Dice:
    def __init__(self, screen, init_tile):
        self.screen = screen
        self.rolling = False
        self.MAX_ROLLS = 10
        self.roll_count = 0
        self.dice_images = [DICE_1, DICE_2, DICE_3, DICE_4, DICE_5, DICE_6]
        self.dice_image = None
        self.auto_roll = False

        self.roll_sound = pg.mixer.Sound('assets/sound/roll.ogg')

        self.init_tile = init_tile
        self.tile_used = True

    def draw(self):
        if not self.rolling:
            if self.tile_used and not self.auto_roll:
                self.screen.blit(ROLL, (pg.display.get_surface().get_size()[0]/2 - DICE_WIDTH/2 + DICE_WIDTH, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT)))
                self.screen.blit(AUTO, (pg.display.get_surface().get_size()[0]/2 - DICE_WIDTH/2 - DICE_WIDTH, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT)))
        if self.auto_roll:
            self.screen.blit(AUTO, (DICE_WIDTH//2, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT)))

        if self.roll_count and self.rolling:
            self.screen.blit(BACKGROUND, (0, 0))
            self.screen.blit(self.dice_images[self.rolled - 1], (pg.display.get_surface().get_size()[0]/2 - DICE_WIDTH/2, pg.display.get_surface().get_size()[1]/2 - DICE_HEIGHT/2))

    def update(self, sound_on, tile_used=True):
        roll_btn_rect = pg.Rect(pg.display.get_surface().get_size()[0]/2 - DICE_WIDTH/2 + DICE_WIDTH, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT), DICE_WIDTH, DICE_HEIGHT)
        if not self.auto_roll:
            auto_btn_rect = pg.Rect(pg.display.get_surface().get_size()[0]/2 - DICE_WIDTH/2 - DICE_WIDTH, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT), DICE_WIDTH, DICE_HEIGHT)
        else:
            auto_btn_rect = pg.Rect(DICE_WIDTH//2, pg.display.get_surface().get_size()[1] - DICE_HEIGHT - (0.33 * DICE_HEIGHT), DICE_WIDTH, DICE_HEIGHT)
        self.tile_used = tile_used
        if self.rolling:
            self.roll_animation(sound_on)
        else:
            if self.tile_used:
                if not self.auto_roll:
                    if roll_btn_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
                        self.rolling = True
                else:
                    self.rolling = True
        if auto_btn_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
            if not self.auto_roll and self.tile_used:
                self.auto_roll = True
            else:
                self.auto_roll = False
            
    def roll_animation(self, sound_on):
        # roll the dice and get the rolled number
        self.rolled = random.randint(1, 6)
        self.roll_count += 1
        if sound_on:
            if self.roll_count > 2:
                pg.mixer.Sound(self.roll_sound).play()
        if self.roll_count == self.MAX_ROLLS:
            self.rolling = False
            self.roll_count = 0
            self.rolled = random.randint(1, 6)
            self.init_tile(self.rolled)            
        pg.time.wait(100)