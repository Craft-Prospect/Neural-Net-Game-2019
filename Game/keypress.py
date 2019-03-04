from sprites import *
from helper import *

class Mixin:
    #Player controls
    def on_key_press(self, key, modifiers):
        if self.current_state == GAME_PAGE:
            if self.player_sprite.active:
                self.player_keyboard(key)

        elif self.current_state == START_PAGE:
            self.menu_keyboard(key)

        elif self.current_state == ENTER_NAME:
            self.enter_keyboard(key)

    def player_keyboard(self,key):
        """Pressing arrow keys """
        if key == arcade.key.UP:
            self.player_sprite.change_y = self.player_sprite.speed
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -self.player_sprite.speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.player_sprite.speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.player_sprite.speed

        #PLayer attempts to capture
        elif key == arcade.key.SPACE:
            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.fire_list)
            # Loop through each colliding sprite, remove it, and add to the player_score.
            for fire in hit_list:
                fire.kill()
                self.player_sprite.score += 100

    def menu_keyboard(self,key):
        if key == arcade.key.SPACE:
            self.selected_index = (self.selected_index+1)%2
            self.selected = self.buttons[self.selected_index]
            self.pointer.center_y = self.selected.center_y

    def enter_keyboard(key):
        # 65293 value for **ENTER**
        if key == 65293:
            add_high_score(self.name,self.player_score)
            self.current_state = HIGH_SCORE_PAGE

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


    #Allows for continouse update
    def on_key_release(self, key, modifiers):
        if self.current_state == GAME_PAGE:
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_x = 0



    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

        # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen
        print(button)
        if self.current_state == ENTER_NAME:
            character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

            for Key in character_hit_list:
                if Key.character == ';':
                    add_high_score(self.name)
                    self.current_state = HIGH_SCORE_PAGE

                if Key.character == '-':
                    self.name = self.name[0:-1]

                elif len(self.name) <= 3:self.name.append(Key.character.upper())

        if self.current_state == GAME_PAGE:
            self.check_fire_collison(self.player_sprite)
