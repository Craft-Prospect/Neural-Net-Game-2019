#Onscreen Keyboard
import arcade
import os
import glob
import time
import sys

#Scaling for sprites
SPRITE_SCALING_POINTER = 1
SPRITE_SCALING_KEY = 1

#Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Variables used for joystick movement
MOVEMENT_SPEED = 3
DEAD_ZONE = 0.02



#Class for each Key contains it's 'Character'
class Key(arcade.Sprite):
    character = ""
    
        

        
        
class MyGame(arcade.Window):
    
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        # If you have sprite lists, you should create them here,
        # Variables that will hold sprite lists
        self.pointer_list = None
        self.key_list = None
        # and set them to None
 
         # Get a list of all the game controllers that are plugged in
        joysticks = arcade.get_joysticks()

        # If we have a game controller plugged in, grab it and
        # make an instance variable out of it.
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            print("There are no Joysticks")
            self.joystick = None

          

          

    def setup(self):



        #String taking input
        self.name = []

        #Boolean for CapsLock toggle
        self.caps_on = False

        #Character list tracking variable
        self.key_position = 0

        #Check variable for joystick
        self.check = 0
        self.check_y = 0


        #Sprite lists
        self.pointer_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        
        #Set up pointer
        # Set up the player
        self.pointer_sprite = arcade.Sprite('keyboard_images/icons8-unchecked-checkbox-filled-50.png', SPRITE_SCALING_POINTER)
        self.pointer_sprite.center_x = 50
        self.pointer_sprite.center_y = 200
        self.pointer_list.append(self.pointer_sprite)

        #Setup Delete button
        self.key_sprite = Key('keyboard_images/icons8-clear-symbol-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 500
        self.key_sprite.center_y = 150
        self.key_sprite.character = '-'  # use '-' as identifier for backspace
        self.key_list.append(self.key_sprite)

        #Setup Delete button
        self.key_sprite = Key('keyboard_images/icons8-enter-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 400
        self.key_sprite.center_y = 100
        self.key_sprite.character = ';'  # use ';' as identifier for backspace
        self.key_list.append(self.key_sprite)

        #Setup keys
        x = 0
        y = 0
        count = 0
        #for filename in os.listdir('keyboard_images/characters'):
        #Loops through file containing characters and adds creates a 'Key' object for each character
        for filename in sorted(glob.glob('keyboard_images/characters/*.png')):
            if filename.endswith(".png"):
                if count == 10:
                    x = 0
                    y = -50
                if count == 19:
                    x = 0
                    y = -100
                    
                    
                self.key_sprite = Key(filename, SPRITE_SCALING_KEY)
                self.key_sprite.center_x = 50 + x
                self.key_sprite.center_y = 200 + y
                self.key_sprite.character = filename[29]
                

                count += 1
                
                x+=50
                self.key_list.append(self.key_sprite)

        

            

    def on_draw(self):

        arcade.start_render()

        #Print question:
        arcade.draw_text("Enter player name?",50,500,arcade.color.BLACK,20)

        #Prints input text
        arcade.draw_text(''.join(self.name),350,350, arcade.color.BLACK, 40)

        
        
        # Call draw() on all your sprite lists below
        self.pointer_list.draw()
        self.key_list.draw()



    def update(self, deltatime):
       
        
        if self.joystick:
            
           # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.joystick.x) < DEAD_ZONE:
                self.pointer_sprite.change_x = 0
                self.check = 0

            elif self.check == 0:
                #Joystick movement to the right update position
                if self.joystick.x == 1:
                    self.pointer_sprite.change_x +=50
                #Joystick movement to the left update postion
                else:
                    self.pointer_sprite.change_x -= 50 
                self.check = 1

                time.sleep(0.2)

            #if statements to ensure pointer always on the keyboard // Replace with case statement?
            if self.pointer_sprite._position[0] >500:
                self.pointer_sprite._position[0] = 50

            if self.pointer_sprite._position[0] <50:
                self.pointer_sprite._position[0] = 500

            if self.pointer_sprite._position[0] > 400 and self.pointer_sprite._position[1] == 100:
                self.pointer_sprite._position[0] = 50

            if self.pointer_sprite._position[0] <50 and self.pointer_sprite._position[1] == 100:
                self.pointer_sprite._position[0] = 400
            
            
                
                

            # Set a "dead zone" to prevent drive from a centered joystick
            # Movement value must be greater than dead zone for movement to be registered by the joystick 
            if abs(self.joystick.y) < DEAD_ZONE:
                self.pointer_sprite.change_y = 0
                self.check_y = 0

            elif self.check_y == 0:
                if self.joystick.y == -1:
                    self.pointer_sprite.change_y +=50
                else:
                    self.pointer_sprite.change_y -= 50 
                self.check_y = 1
                time.sleep(0.2)

            #Scroll back if sprite is moving off the keyboard
            if self.pointer_sprite._position[1] > 200:
                self.pointer_sprite._position[1] = 100

            if self.pointer_sprite._position[1] <100:
                self.pointer_sprite._position[1] = 200    

        

        self.pointer_sprite.update()

        

    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

        # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen 
        character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

        for Key in character_hit_list:

            if Key.character == ';':
                MyGame.endForm(self)

            if Key.character == '-':
                self.name = self.name[0:-1]

            elif len(self.name) <= 3:self.name.append(Key.character.upper())
            


    #Keeping unused joystick functions for testing
    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))


    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y)) 



    def endForm(self):
        print("Form has ended")


    #On key press parse value of key being pressed and add to the string being output
    def on_key_press(self, key, modifiers):

            
            
             # 65293 value for **ENTER**
            if key == 65293:
                MyGame.endForm(self)
                    
            #If value over 2^16 is selected as it causes a crash
            if key> 65536:
                return

            #Value for shift instead of printing value return
            elif key == 65506:
                return

            #Value for caps key, boolean turned on and off if selected
            elif key == 65509:
                self.caps_on = not self.caps_on
                return 
            
            #Value for delete key
            elif key == 65288:
                self.name = self.name[0:-1]

            #If caps is on append in upper case otherwise in lowercase z
            elif len(self.name) <= 3:

                if self.caps_on:
                    self.name.append(chr(key).upper())
        
                else:
                    self.name.append(chr(key))
    

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()
    sys.exit()


if __name__ == "__main__":
    main()