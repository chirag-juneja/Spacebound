import pygame
from random import randint
from spacebound.sprites.enemy import Enemy
from spacebound.sprites.enemy_ray import EnemyRay
from spacebound.sprites.meteor import Meteor
import spacebound.globals as gl


class Level:
    def __init__(self, enemy_type="enemy", n_enemy=3):
        self.enemy_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.cooldown = 1000
        self.last_live_enemy = pygame.time.get_ticks()
        self.enemy_count = 0
        self.n_enemy = n_enemy
        self.isactive = True
        self.enemy_type = enemy_type

    def create_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.last_live_enemy > self.cooldown:
            if self.enemy_type == "enemy":
                enemy = Enemy()
            elif self.enemy_type == "enemy_ray":
                enemy = EnemyRay()
            self.enemy_group.add(enemy)
            self.enemy_count += 1
            if self.enemy_count > self.n_enemy:
                self.isactive = False

    def update(self, player):
        if not len(self.enemy_group):
            self.create_enemy()
        else:
            self.last_live_enemy = pygame.time.get_ticks()

        target = player.x, gl.window_height * 0.4
        self.enemy_group.update(target, self.meteor_group)

    def enemy_event(self):
        pass

    def meteor_event(self):
        meteors = [Meteor() for i in range(randint(0, 2))]
        self.meteor_group.add(meteors)
