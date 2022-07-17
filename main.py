import asyncio
import src.Game as Game

def main():
    asyncio.run(Game.Game(800, 600, 'Duzzle', 60).run())

if __name__ == '__main__':
    main()