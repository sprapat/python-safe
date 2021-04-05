#My high score is 99
#use curses
import curses
from time import sleep
from random import choice
from datetime import datetime, timedelta
from collections import namedtuple

class Display:
    def __init__(self,stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
    
    def create_border(self):
        [self.addstr(y,0,'#') for y in range(11)]
        [self.addstr(y,10,'#') for y in range(11)]
        [self.addstr(0,x,'#') for x in range(11)]
        [self.addstr(10,x,'#') for x in range(11)]

    def create_lanes(self):
        [self.addstr(y,x,'|') for x in range(2,9,2) for y in range(1,8,2)]
        [self.addstr(y+1,x,'|') for x in range(2,9,2) for y in range(1,8,2)]

    def display_character(self,x):
        self.addstr(9,x,'P')

    def clear_character(self,x):
        self.addstr(9,x,' ')

    def refresh(self):
        self.stdscr.refresh()

    def get_key(self):
        try:
            return self.stdscr.getkey(11,0)
        except Exception:
            pass

    def clear(self,y,x):
        self.addstr(y,x,' ')

    def display_obs(self,y,x):
        self.addstr(y,x,'A')

    def addstr(self,y,x,text):
        self.stdscr.addstr(y,x,text)
        self.refresh()

    def display_string_formula(self,word,y,x = 0):
        [self.addstr(y,index+x,letter) for index,letter in enumerate(word)]

    def display_you_lose(self):
        self.display_string_formula('You lose, good day sir!',12)

    def display_this_is_score(self):
        self.display_string_formula('Your score is:',4,12)
        
    def display_score(self,score):
        self.addstr(4,13+len('Your score is:'),str(score))

    def display_result(self,result):
        [self.addstr(5,index+12,letter) for index,letter in enumerate(str(result))]

    def display_level(self,level):
        self.display_string_formula('Your level is:',5,12)
        self.addstr(5,13+len('Your level is:'),str(level))


class Character:
    def __init__(self,display):
        self.display = display
        self.display.display_character(5)
        self.current_x = 5

    def move(self):
        key_pressed = self.display.get_key()
        if key_pressed in ['KEY_LEFT', 'KEY_RIGHT']:
            self.display.clear_character(self.current_x)
            if (key_pressed == 'KEY_LEFT') and (self.current_x-2 != -1):
                 self.current_x -= 2
            if (key_pressed == 'KEY_RIGHT') and (self.current_x+2 != 11):
                self.current_x += 2

    def display_character(self):
        self.display.display_character(self.current_x)

    def get_current_x(self):
        return self.current_x


class Obstacle:
    ALL = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    X_CHOICE = [1,3,5,7,9]

    def __init__(self, display, game, score):
        self.list = []
        self.score = score
        self.game = game
        self.display = display
        [self.get_speed_list(0.6 - self.score/10) if self.score <= 5 else self.get_speed_list(0.09 - (self.score - 6)/100) if self.score <= 14 else self.get_speed_list(0.01, 0.09 - (self.score - 24)/100) if self.score <= 23 else self.get_speed_list(0.01, 0.09 - (self.score - 24)/100) if self.score <= 33 else self.get_speed_list(0.01,0.01)]
        self.last_timestamp = datetime.now()
        speed_timedelta = [timedelta(seconds = int(i)+0.1) for i in self.list]
        self.obs_lane = choice(self.X_CHOICE)
        self.speed = choice(speed_timedelta)
        self.current_y = 0
            
    def move(self):
        if not (datetime.now()-self.last_timestamp < self.speed):
            self.last_timestamp = datetime.now()
            if self.current_y != 9:
                self.display.display_obs(self.current_y+1,self.obs_lane)
                self.current_y+=1
            elif self.current_y == 9:
                self.display.clear_character(self.obs_lane)
                self.game.remove_from_obs_list(self)
                self.game.add_score()

    def is_hit(self, character):
        return (self.obs_lane == character.get_current_x()) and (self.current_y == 9)

    def add_to_obs_position_list(self):
        [self.game.add_to_obs_position_list(self.current_y,self.obs_lane) if self.current_y > 0 else '']

    def update_score(self,new_score):
        self.score = new_score

    def get_speed_list(self,min,max = 1):
        for element in self.ALL:
            if not element < min and not element > max:
                self.list.append(element)

class Game:
    def __init__(self,stdscr):
        self.Point = namedtuple('Point', ['y', 'x'])
        self.display = Display(stdscr)
        self.obs_list = []
        self.current = []
        self.score = 0
        self.obs_position = []
        #Set the self.space_position to have all posible position using list comprehension.
        self.space_position = [self.Point(y,x) for y in range(1,10) for x in range(1,11,2)]
        self.remove = []
        self.level = 0
        self.cool_down_timedelta = timedelta(seconds = 0.4)

    def create_new_obs(self):
        if not (datetime.now()-self.last_timestamp < self.cool_down_timedelta):
            new_obs = Obstacle(self.display, self, self.level)
            self.obs_list.append(new_obs)
            self.last_timestamp = datetime.now()

    def setup_board(self):
        self.display.create_border()
        self.display.create_lanes()
        self.character = Character(self.display)
        self.display.display_this_is_score()

    def update_display(self):
        self.display_all_obs()
        self.character.display_character()

    def play(self):
        self.last_timestamp = datetime.now()
        self.setup_board()
        while not self.is_hit():
            self.update_level()
            self.display.display_level(self.level)
            self.display_score()
            self.character.move()
            #create new obstacle
            [self.create_new_obs() if len(self.obs_list) <= self.level+4 else '']
            #move all obstacle if the time hasn't arrive yet, the move will be skipped
            [obs.move() for obs in self.obs_list]
            #add to the list to display
            [obs.add_to_obs_position_list() for obs in self.obs_list]
            [obs.update_score(self.level) for obs in self.obs_list]
            #Display both the obstacle and the character. Display empty space every lane sqaure else.
            self.update_display()
            #Display "You lose, good day sir!"
        self.display.display_you_lose()
        sleep(2)

    def update_level(self):
        self.level = self.score//10

    def add_score(self):
        self.score += 1

    def display_score(self):
        self.display.display_score(self.score)

    def is_hit(self):
        for obs in self.obs_list: 
            if obs.is_hit(self.character): return True
        return False

    def remove_from_obs_list(self,element):
        self.obs_list.remove(element)

    def add_to_obs_position_list(self,y,x):
        self.obs_position.append(self.Point(y,x))

    def display_all_obs(self):
        #Check which position is occuppied by obs by turning both lists into sets
        obs_position_set = set(self.obs_position)
        space_position_set = set(self.space_position)
        #Check which element is in both sets. Then put them into the variable 'result'
        result = obs_position_set & space_position_set
        #Remove 'result' from 'self.space_position'
        self.space_position = [a for a in self.space_position if a not in result]
        #Remove character position from 'self.space_position'
        self.space_position = [a for a in self.space_position if not self.is_hit() and a != self.Point(9,self.character.get_current_x())]
        #display obs and space
        self.display_obs()
        self.display_space()

    def display_obs(self):
        [self.display.display_obs(item.y,item.x) for item in self.obs_position]
        self.obs_position = []

    def display_space(self):
        [self.display.clear(item.y,item.x) for item in self.space_position]
        #Reset the self.space_position to have all posible position using list comprehension
        self.space_position = [self.Point(y,x) for y in range(1,10) for x in range(1,11,2)]

def main(stdscr):
    a = Game(stdscr)
    a.play()
curses.wrapper(main)
