import curses
from package.Game import Game
from time import sleep


def main(stdscr):
    a = Game(stdscr)
    a.play()
    sleep(3)

if __name__ == '__main__':
    curses.wrapper(main)
    curses.echo()