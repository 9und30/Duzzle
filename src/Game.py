import asyncio, sys
import pygame as pg
pg.init()

from .Objects.Area import Area


class Game:
    def __init__(self, WIDTH, HEIGHT, TITLE, FPS) -> None:
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TITLE = TITLE
        self.FPS = FPS
        self.BACKGROUND_COLOR = (20, 0, 44)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load('assets/image/dice/roll.png'))
        self.clock = pg.time.Clock()
        self.running = True

        self.area = Area(self.screen)

    async def run(self) -> None:
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.draw()
            self.update()

            self.clock.tick(self.FPS)

            await asyncio.sleep(0)
            pg.display.update()


    def draw(self) -> None:
        self.screen.fill(self.BACKGROUND_COLOR)

        self.area.draw()

    def update(self) -> None:
        self.area.update()