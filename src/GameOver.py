import pygame as pg

class GameOver:
    def __init__(self, screen, score, restart_game) -> None:
        self.screen = screen
        self.score = score
        self.restart_game = restart_game
        self.background = pg.image.load('assets/image/background.png')
        self.game_over_font = pg.font.Font('assets/font/BalsamiqSans-Bold.ttf', 88)
        self.score_font = pg.font.Font('assets/font/BalsamiqSans-Bold.ttf', 64)
        self.game_over_text = self.game_over_font.render('Game Over', True, (255, 255, 255))
        self.score_text = self.score_font.render(str(score), True, (255, 255, 255))
        self.retry_btn = pg.image.load('assets/image/retry.png')

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.game_over_text, ((pg.display.get_surface().get_size()[0]//2)-(self.game_over_text.get_width()//2), (pg.display.get_surface().get_size()[1]//4)-(self.game_over_text.get_height()//2)))
        self.screen.blit(self.score_text, ((pg.display.get_surface().get_size()[0]//2)-(self.score_text.get_width()//2), (pg.display.get_surface().get_size()[1]//2)-(self.score_text.get_height()//2)))
        self.screen.blit(self.retry_btn, ((pg.display.get_surface().get_size()[0]//2)-(self.retry_btn.get_width()//2), (pg.display.get_surface().get_size()[1]//2)+(self.retry_btn.get_height()//2)))

    def update(self):
        self.score_text = self.score_font.render('Your score: ' + str(self.score), True, (255, 255, 255))
        retry_btn_rect = pg.Rect((pg.display.get_surface().get_size()[0]//2)-(self.retry_btn.get_width()//2), (pg.display.get_surface().get_size()[1]//2)+(self.retry_btn.get_height()//2), self.retry_btn.get_width(), self.retry_btn.get_height())
        if retry_btn_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
            self.restart_game()