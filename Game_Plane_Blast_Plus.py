import arcade
import math
from random import randint
from time import time, sleep
import threading
import arcade.key
from arcade.key import SPACE
class Spaceship(arcade.Sprite):
    def __init__(self, w):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png")
        self.width = 48
        self.height = 48
        self.center_x = w//2
        self.center_y = 48
        self.angle = 0
        self.change_angle = 0
        self.bullet_list = []
        self.speed = 5
        self.score = 0
        self.health = 3
    def rotate(self):
        self.angle += self.change_angle * self.speed
    def fire(self):
        self.bullet_list.append(Bullet(self))
class Enemy(arcade.Sprite):
    def __init__(self, w, h, s=2):
        super().__init__(":resources:images/space_shooter/playerShip3_orange.png")
        self.speed = s
        self.center_x = randint(0, w)
        self.center_y = h + h//2
        self.angle = 180
        self.width = 48
        self.height = 48
    def hit_sound(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/explosion1.wav"))
    def move(self):
        self.center_y -= self.speed
class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.speed = 6
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y
    def laser_sound(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/lose4.wav"), 0.3)
    def move(self):
        angle = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle)
        self.center_y += self.speed * math.cos(angle)      
class Game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 600
        super().__init__(self.w, self.h, title="Plane Blast Game")
        self.background_image = arcade.load_texture("picture/background.png")
        self.me = Spaceship(self.w)
        self.enemy = Enemy(self.w, self.h)
        self.enemy_list = []
        self.speed_increment = 0.1
        self.thread = threading.Thread(target=self.add_enemy)
        self.thread.start()
        self.thread_disrupt = False
        self.health_image = arcade.load_texture("picture/heart.png")
    def add_enemy(self):
        while True:
            self.enemy_list.append(Enemy(self.w, self.h))
            for enemy in self.enemy_list:
                enemy.speed += self.speed_increment
            self.speed_increment += 0.2
            sleep(randint(4, 6))
            if self.thread_disrupt:
                break
    def on_draw(self):
        arcade.start_render()
        if self.me.health <= 0:
            arcade.draw_text("Game Over !!! ", self.w//2-200, self.h//2, arcade.color.RED_VIOLET, 20, width=400, align="center")
            self.thread_disrupt = True
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)
            self.me.draw()
            for i in range(len(self.me.bullet_list)):
                self.me.bullet_list[i].draw()
            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()
            for i in range(self.me.health):
                arcade.draw_lrwh_rectangle_textured(10+i*35, 10, 30, 30, self.health_image)
            arcade.draw_text("Score: " + str(self.me.score), self.w-130, 10, arcade.color.LIGHT_PINK, 20, width=200)
    def on_update(self, delta_time):
        self.me.rotate()
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].move()
        for i in range(len(self.enemy_list)):
            self.enemy_list[i].move()
        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(bullet, enemy):
                    enemy.hit_sound()
                    self.me.bullet_list.remove(bullet)
                    self.enemy_list.remove(enemy)
                    self.me.score += 1
        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.me.health -= 1
                self.enemy_list.remove(enemy)
        for bullet in self.me.bullet_list:
            if bullet.center_y > self.height or bullet.center_x < 0 or bullet.center_x > self.width:
                self.me.bullet_list.remove(bullet)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.me.change_angle = 1
        elif key == arcade.key.RIGHT:
            self.me.change_angle = -1
        elif key == arcade.key.ENTER:
            self.me.fire()
            self.me.bullet_list[-1].laser_sound()
        elif arcade.key.SPACE:
            self.me.fire()
            self.me.bullet_list[-1].laser_sound()
    def on_key_release(self, key, modifiers):
        self.me.change_angle = 0
if __name__ == "__main__":
    game = Game()
    arcade.run()