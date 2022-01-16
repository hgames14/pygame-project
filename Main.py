import pygame
import os
import sys
import random
import sqlite3
class Game:

    def load_image(self, name, colorkey=-1):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            screen = pygame.display.set_mode(self.size)
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            screen = pygame.display.set_mode(self.size)
            image = image.convert_alpha()
        return image

    def astro_move(self):
        self.astro.rect.y += self.astro_speed / self.fps
        self.render(self.screen)

    def create_astro(self):
        self.Astro = pygame.sprite.Group()
        self.astro = pygame.sprite.Sprite()
        self.astro.image = self.load_image("astro1.png")
        self.astro.image = pygame.transform.scale(self.astro.image, (75, 75))
        self.astro.rect = self.astro.image.get_rect()
        self.astro.rect.x = random.randint(0, 725)
        self.astro.rect.y = 25
        self.astro_speed = 200
        self.Astro.add(self.astro)
        self.Astro.draw(self.screen)

    def player_init(self):
        self.Player = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite()
        self.player.image = self.load_image("ufo.png")
        self.player.image = pygame.transform.scale(self.player.image, (150, 75))
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = 400
        self.player.rect.y = 800
        self.Player.add(self.player)
        self.screen.blit(self.bg, (0, 0))
        self.Player.draw(self.screen)

    def render(self, screen):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.Player.draw(self.screen)
        self.Astro.draw(self.screen)


    def move_right(self, screen, player, velocity):
        self.player.rect.x += velocity / self.fps
        if self.player.rect.x > 850:
            self.player.rect.x = 850

        self.direction = "RIGHT"
        self.render(self.screen)

    def move_left(self, screen, player, velocity):
        self.player.rect.x -= velocity / self.fps
        if self.player.rect.x < 0:
            self.player.rect.x = 0

        self.direction = "LEFT"
        self.render(self.screen)

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(1)
                    print(self.direction)
                    if self.direction == "RIGHT":
                        self.move_right(self.screen, self.Player, self.player_speed * 50)
                    if self.direction == "LEFT":
                        self.move_left(self.screen, self.Player, self.player_speed * 50)
                if event.type == pygame.QUIT:
                    running = False
            sp = pygame.key.get_pressed()
            if sp[pygame.K_RIGHT]:
                self.move_right(self.screen, self.Player, self.player_speed)
            if sp[pygame.K_LEFT]:
                self.move_left(self.screen, self.Player, self.player_speed)
            if sp[pygame.K_UP]:
                self.pause()
            if sp[pygame.K_DOWN]:
                self.unpause()
            self.astro_move()
            self.clock.tick(self.fps)
            pygame.display.flip()

    def pause(self):
        self.player_speed = 0

    def unpause(self):
        self.player_speed = 200

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.player_speed = 200
        self.size = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load("data/space.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 1000))
        self.screen.blit(self.bg, (0, 0))
        self.create_astro()
        self.player_init()
        self.play()
session = Game()