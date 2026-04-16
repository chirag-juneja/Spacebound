import pygame
from pygame import mixer
import spacebound.globals as gl
from .background import Background
from .sprites.player import Player
from .sprites.meteor import Meteor
from .sprites.laser import Laser
from .sprites.enemy import Enemy
from .sprites.health import Health
from .menu import Menu
from .audio import Audio
from .level import Level


class Game:

    def __init__(self):
        pygame.init()
        mixer.init()
        self.create_window()
        self.score_font = pygame.font.Font(gl.font_path, 20)
        self.clock = pygame.time.Clock()
        self.event_counter = 1
        self.audio = Audio()
        self.mode = "menu"
        self.menu = Menu()
        self.n_level = 3
        self.reset()

    def reset(self):
        self.score = 0
        self.level_idx = 0
        # self.levels = [SingleLevel()]
        # self.level = self.levels[0]
        self.level = Level()
        self.load_sprites()
        self.load_level()

    def create_window(self):
        self.screen = pygame.display.set_mode((gl.window_height, gl.window_width))
        pygame.display.set_caption(gl.window_name)

    def load_sprites(self):
        self.player = Player()
        self.health = Health()
        self.background = Background()

        self.health_group = pygame.sprite.Group()
        self.health_group.add(self.health)

        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)

        self.player_laser_group = pygame.sprite.Group()

        self.enemy_laser_group = pygame.sprite.Group()

        self.create_events()

    def load_level(self):
        self.meteor_group = self.level.meteor_group
        self.enemy_group = self.level.enemy_group

    def create_events(self):
        self.METEOR_EVENT = pygame.USEREVENT + self.event_counter
        pygame.time.set_timer(self.METEOR_EVENT, 1000)
        self.event_counter += 1
        self.SCORE_EVENT = pygame.USEREVENT + self.event_counter
        pygame.time.set_timer(self.SCORE_EVENT, 1000)
        self.event_counter += 1
        self.ENEMY_EVENT = pygame.USEREVENT + self.event_counter
        pygame.time.set_timer(self.ENEMY_EVENT, 500)
        self.event_counter += 1

    def change_level(self):
        self.load_level()

    def update(self):
        self.player_group.update()
        self.meteor_group.update()
        self.player_laser_group.update()
        self.enemy_laser_group.update()
        self.health_group.update()
        self.level.update(self.player)
        if not self.level.isactive:
            self.change_level()

    def draw_background(self):
        self.background.draw(self.screen)

    def draw(self):
        self.meteor_group.draw(self.screen)
        self.player_laser_group.draw(self.screen)
        self.enemy_laser_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.health_group.draw(self.screen)
        self.draw_score()

    def fire(self):
        laser = self.player.fire()
        if laser:
            self.audio.laser()
            self.player_laser_group.add(laser)

    def handle_input(self, keys):
        if not len(self.player_group):
            return
        if keys[pygame.K_LEFT]:
            self.player.move(-gl.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(gl.speed, 0)
        if keys[pygame.K_UP]:
            self.player.move(0, -gl.speed)
        if keys[pygame.K_DOWN]:
            self.player.move(0, gl.speed)
        if keys[pygame.K_SPACE]:
            self.fire()

    def collision(self):
        player_collision = pygame.sprite.groupcollide(
            self.player_group, self.meteor_group, False, False
        )
        for player in player_collision:
            player.destory(self.audio)
        player_laser_collisions = pygame.sprite.groupcollide(
            self.player_laser_group, self.meteor_group, False, False
        )
        for laser in player_laser_collisions:
            laser.hit = True
        player_enemy_collision = pygame.sprite.groupcollide(
            self.player_group, self.enemy_laser_group, False, False
        )
        for player in player_enemy_collision:
            player.destory(self.audio)

        enemy_laser_collisions = pygame.sprite.groupcollide(
            self.enemy_laser_group, self.meteor_group, False, False
        )
        for laser in enemy_laser_collisions:
            laser.hit = True
        enemy_collision = pygame.sprite.groupcollide(
            self.enemy_group, self.player_laser_group, False, False
        )
        for enemy in enemy_collision:
            self.score += enemy.destroy(self.audio)
        enemy_collision = pygame.sprite.groupcollide(
            self.enemy_group, self.meteor_group, False, False
        )
        for enemy in enemy_collision:
            self.score += enemy.destroy(self.audio)

    def enemy_fire(self):
        for enemy in self.enemy_group.sprites():
            laser = enemy.fire()
            if laser:
                self.audio.laser()
                self.enemy_laser_group.add(laser)

    def draw_text(self, text, color, x, y):
        img = self.score_font.render(text, True, color)
        w = img.get_width()
        self.screen.blit(img, (x - w // 2, y))

    def update_score(self):
        pass

    def draw_score(self):
        x = int(gl.window_width / 2)
        y = int(gl.window_height * 0.05)
        self.draw_text("Score: " + str(self.score), gl.white, x, y)

    def run(self):
        running = True
        while running:
            self.clock.tick(gl.fps)

            self.draw_background()

            if self.mode == "play":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == self.METEOR_EVENT:
                        self.level.meteor_event()
                    if event.type == self.SCORE_EVENT:
                        self.update_score()
                    # if event.type == self.ENEMY_EVENT:

                self.enemy_fire()

                keys = pygame.key.get_pressed()

                self.handle_input(keys)
                self.collision()
                self.update()
                self.draw()

                if not len(self.player_group):
                    self.mode = "retry"

            if self.mode == "menu":
                running, self.mode = self.menu.main(self.screen)

            if self.mode == "retry":
                running, self.mode = self.menu.retry(self.screen, self.score)
                if self.mode == "play":
                    self.reset()

            if self.mode == "end":
                running, self.mode = self.menu.end(self.screen, self.score)
                if self.mode == "play":
                    self.reset()

            pygame.display.update()

        pygame.quit()
