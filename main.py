import sys, logging, open_color, arcade, os, random, math

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])


logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
SCREEN_TITLE = "alien invasion"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,150)
BULLET_DAMAGE = 50
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100



class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/spaceShips_007.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
        

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an alien enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/shipGreen_manned.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):

    def __init__(self, width, height, title):

        
        super().__init__(width, height, title)

        self.set_mouse_visible(False)

        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0



    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 800
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy) 

    def update(self, delta_time):
        self.bullet_list.update()

        for e in self.enemy_list:

            damage = arcade.check_for_collision_with_list(e, self.bullet_list) # check for collision
            for d in damage:                            
                e.hp = e.hp - d.damage                  
                d.kill ()
                if e.hp < 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE  
            

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)     #fire a bullet
                  

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

