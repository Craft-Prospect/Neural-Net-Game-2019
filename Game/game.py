"""Satellite game where user competes against CPU to capture events while avoid clouds"""
import os
import time
import sys

from sprites import *
from helper import *

import menu
import instructions
import runGame
import highscore
import demo
import keyboard
import keypress
import stateChange
import spriteFunc
import drawing
import updateGame
import updateIns
import updateKeyboard
import updateMenu
import splash
import levels
import pygame

#Main window
class MyGame(drawing.Mixin, keypress.Mixin, stateChange.Mixin, spriteFunc.Mixin, levels.Mixin, splash.Mixin, updateGame.Mixin, updateIns.Mixin, updateKeyboard.Mixin, menu.Mixin, instructions.Mixin, demo.Mixin, runGame.Mixin,keyboard.Mixin,highscore.Mixin,updateMenu.Mixin, arcade.Window):
    #Initalise game variables and window
    def __init__(self, width, height,test):

        # Call the parent class initialise to window
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold the sprite lists
        self.fire_list=None
        self.clouds_list = None

        self.Test = test

        self.fire_data = None
        self.cloud_damage = CLOUD_DAMAGE

        # Set up the player info
        self.player_sprite = None

        #Set up CPU sprite
        self.cpu_sprite = None

        #Background sprites
        self.background_list = None
        self.background_even = None
        self.background_odd = None
        self.background_index = 0
        self.final_background = False
        self.background = None

        #For screenshot timings
        self.frame = 800
        self.frame_count = 0
        self.picture = 0

        #Game state
        self.current_state = STATE

        #Instruction pages
        self.instructions = []

        #Setup background textures
        texture = arcade.load_texture("images/menu.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_1.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/about.png")
        self.instructions.append(texture)
        #Menu buttons
        self.buttons = None
        self.start_button = None
        self.inst_button = None

        #Currently selected buttons
        self.selected = None

        #Pointer into button list
        self.selected_index = None

        #Sprite to show which button is selected
        self.pointer_list = None
        self.pointer = None

        self.player_score = None

        #Keyboard values
        self.key_list = None

        self.source = SOURCE[0]
        self.NNDir = NNDir

        self.update_count = 0

        # Get a list of all the game controllers that are plugged in
        self.joysticks = arcade.get_joysticks()

        # If we have a game controller plugged in, grab it and
        # make an instance variable out of it.
        if self.joysticks:
            self.joystick = self.joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            self.joystick = None


        self.setup_splash()

        if not self.Test:
            self.lvl_up =  pygame.mixer.Sound("Music/sounds/lvlup.wav")
            self.player_sound = pygame.mixer.Sound("Music/sounds/Ching.wav")
            self.cpu_sound =  pygame.mixer.Sound("Music/sounds/beep.wav")
        else:
            self.player_sound = None
            self.cpu_sound = None

        self.clouds_limit = 3

        self.SOURCE = SOURCE


    def update(self, delta_time):

        if self.current_state == START_PAGE:
            if self.joysticks:
                self.startMenu_update()
            

        elif self.current_state == GAME_PAGE:
            self.game_update()

        elif self.current_state == ENTER_NAME:
            self.keyboard_update()

        else:
            self.ins_update()
