import pygame
import os
import sys
import random
import sqlite3
WHITE = (255, 255, 255)
player_image = "ufo.png"


def get_record():
    con = sqlite3.connect("records.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * from Record""").fetchall()
    result = str(result[0][0])
    print(result)
    cur.close()
    con.commit()
    return result


def set_record(score):
    con = sqlite3.connect("records.db")
    cur = con.cursor()
    edit = cur.execute("""UPDATE Record set record = ?""", (score, ))
    cur.close()
    con.commit()


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        screen = pygame.display.set_mode((1000, 1000))
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        screen = pygame.display.set_mode(self.size)
        image = image.convert_alpha()
    return image


class Game:
    def game_over(self):
        print(1)
        if Game.score >= int(get_record()):
            set_record(Game.score)
        self.running = False
        end = EndScreen()

    def update_text(self):
        self.score_text_str = "Score: " + str(self.score)
        self.life_text_str = "Lifes: " + str(self.lifes)
        self.score_text = self.font.render(self.score_text_str, 1, WHITE)
        self.life_text = self.font.render(self.life_text_str, 1, WHITE)

    def astro_move(self):
        self.astro.rect.y += self.astro_speed / self.fps
        self.render(self.screen)

    def check_collide(self):
        if pygame.sprite.collide_mask(self.player, self.astro):
            return True

    def create_new_astro(self):
        self.Astro.remove(self.astro)
        self.create_astro()

    def set_speed(self, speed):
        self.player_speed = speed
        if speed == 500:
            self.counter = 10

    def create_astro(self):
        self.Astro = pygame.sprite.Group()
        self.astro = pygame.sprite.Sprite()
        self.heal = False
        self.bomb = False
        self.speed = False
        if Game.score >= 15:
            a = random.choice([1, 2, 3] + [0] * 17)
            if a == 1:
                self.heal = True
                self.astro.image = load_image("heal.png")
            if a == 0:
                self.astro.image = load_image("astro1.png")
            if a == 2:
                self.bomb = True
                self.astro.image = load_image("bomb.png")
            if a == 3:
                self.speed = True
                self.astro.image = load_image("speed.png")
            self.astro.image = pygame.transform.scale(self.astro.image, (75, 75))
            self.astro.rect = self.astro.image.get_rect()
            self.astro.rect.x = random.randint(0, 725)
            self.astro.rect.y = 25
        else:
            self.astro.image = load_image("astro1.png")
            self.astro.image = pygame.transform.scale(self.astro.image, (75, 75))
            self.astro.rect = self.astro.image.get_rect()
            self.astro.rect.x = random.randint(0, 725)
            self.astro.rect.y = 25
        self.astro_mask = pygame.mask.from_surface(self.astro.image)
        self.Astro.add(self.astro)
        self.Astro.draw(self.screen)

    def player_init(self):
        global player_image
        self.Player = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite()
        self.player.image = load_image(player_image)
        self.player.image = pygame.transform.scale(self.player.image, (150, 75))
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = 400
        self.player.rect.y = 800
        self.Player.add(self.player)
        self.player_mask = pygame.mask.from_surface(self.player.image)
        self.screen.blit(self.bg, (0, 0))
        self.Player.draw(self.screen)

    def render(self, screen):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.Player.draw(self.screen)
        self.Astro.draw(self.screen)
        self.screen.blit(self.life_text, (25, 25))
        self.screen.blit(self.score_text, (875, 25))

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
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(1)
                    print(self.direction)
                    if self.direction == "RIGHT":
                        self.move_right(self.screen, self.Player, 10000)
                    if self.direction == "LEFT":
                        self.move_left(self.screen, self.Player, 10000)
                if event.type == pygame.KEYDOWN:
                    sp = pygame.key.get_pressed()
                    if sp[pygame.K_UP] and self.unpaused:
                        self.pause()
                    if sp[pygame.K_DOWN] and self.paused:
                        self.unpause()
                if event.type == pygame.QUIT:
                    self.running = False
            sp = pygame.key.get_pressed()
            if sp[pygame.K_RIGHT]:
                self.move_right(self.screen, self.Player, self.player_speed)
            if sp[pygame.K_LEFT]:
                self.move_left(self.screen, self.Player, self.player_speed)
            if self.astro.rect.y > 1000 and not self.check_collide():
                if not self.heal and not self.bomb and not self.speed:
                    self.lifes -= 1
                if self.lifes == 0:
                    self.game_over()
                self.create_astro()
                self.update_text()
                self.astro_speed -= 50
                self.counter -= 1
                if self.counter == 0:
                    self.set_speed(200)
            if self.check_collide():
                if self.heal:
                    pygame.mixer.music.load("Sounds/heal.mp3")
                    self.lifes += 1
                elif self.bomb:
                    pygame.mixer.music.load("Sounds/bomb.mp3")
                    self.lifes -= 1
                    if self.lifes == 0:
                        self.game_over()
                elif self.speed:
                    pygame.mixer.music.load("Sounds/speed.mp3")
                    self.set_speed(500)
                else:
                    pygame.mixer.music.load("Sounds/catch.mp3")
                    Game.score += 1
                self.astro_speed += 20
                if self.astro_speed > 1700:
                    self.astro_speed = 1700
                print(self.astro_speed)
                self.update_text()
                self.create_new_astro()
                self.counter -= 1
                if self.counter == 0:
                    self.set_speed(200)
                pygame.mixer.music.play(0)
            self.astro_move()
            self.clock.tick(self.fps)
            pygame.display.flip()

    def pause(self):
        self.unpaused = False
        self.paused = True
        self.player_speed = 0
        self.last_astro_speed = self.astro_speed
        self.astro_speed = 0

    def unpause(self):
        self.unpaused = True
        self.paused = False
        self.player_speed = 200
        self.astro_speed = self.last_astro_speed

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("microsofttaile", 24)
        self.lifes = 3
        Game.score = 0
        self.score_text_str = "Score: " + str(Game.score)
        self.life_text_str = "Lifes: " + str(self.lifes)
        self.score_text = self.font.render(self.score_text_str, 1, WHITE)
        self.life_text = self.font.render(self.life_text_str, 1, WHITE)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.counter = -1
        self.player_speed = 200
        self.direction = None
        self.astro_speed = 200
        self.size = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load("data/space.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 1000))
        self.unpaused = True
        self.paused = False
        self.screen.blit(self.bg, (0, 0))
        self.create_astro()
        self.player_init()


class Main:
    def __init__(self):
        pygame.init()
        print(player_image)
        self.record = get_record()
        self.size = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load("data/bg.png")
        pygame.font.init()
        self.font = pygame.font.SysFont("microsofttaile", 24)
        self.startsign = self.font.render("Start", 1, WHITE)
        self.record_text = "Your record: " + get_record()
        self.recordsign = self.font.render(self.record_text, 1, WHITE)
        self.start_button = pygame.draw.rect(self.screen, WHITE, (400, 600, 200, 50), 5)
        self.shop = self.font.render("Skins", 1, WHITE)
        self.render()

    def render(self):
        self.working = True
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 400 <= pygame.mouse.get_pos()[0] <= 600 and 600 <= pygame.mouse.get_pos()[1] <= 650:
                        self.working = False
                        session = Game()
                        session.play()
                    if 25 <= pygame.mouse.get_pos()[0] <= 225 and 25 <= pygame.mouse.get_pos()[1] <= 75:
                        self.working = False
                        shop = Shop()
                if event.type == pygame.QUIT:
                    self.working = False
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, WHITE, (25, 25, 200, 50), 5)
            self.screen.blit(self.shop, (90, 35))
            self.start_button = pygame.draw.rect(self.screen, WHITE, (400, 600, 200, 50), 5)
            self.screen.blit(self.recordsign, (425, 660))
            self.screen.blit(self.startsign, (475, 610))
            pygame.display.flip()


class EndScreen:
    def __init__(self):
        pygame.init()
        self.size = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load("data/end_bg.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 1000))
        pygame.font.init()
        self.font = pygame.font.SysFont("microsofttaile", 24)
        self.go_to_menu = self.font.render("Go to menu", 1, WHITE)
        self.replay = self.font.render("Play again", 1, WHITE)
        self.current_score_text = "Score: " + str(Game.score)
        self.record_text = "Record: " + get_record()
        self.current_score = self.font.render(self.current_score_text, 1, WHITE)
        self.record = self.font.render(self.record_text, 1, WHITE)
        self.replay_button = pygame.draw.rect(self.screen, WHITE, (100, 200, 25, 50), 1)
        self.render()

    def render(self):
        self.working = True
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 100 <= pygame.mouse.get_pos()[0] <= 400 and 200 <= pygame.mouse.get_pos()[1] <= 275:
                        self.working = False
                        session = Game()
                        session.play()
                    if 100 <= pygame.mouse.get_pos()[0] <= 400 and 400 <= pygame.mouse.get_pos()[1] <= 475:
                        self.working = False
                        main = Main()
            self.screen.blit(self.bg, (0, 0))
            self.replay_button = pygame.draw.rect(self.screen, WHITE, (100, 200, 300, 75), 1)
            self.go_to_menu_button = pygame.draw.rect(self.screen, WHITE, (100, 400, 300, 75), 1)
            self.screen.blit(self.replay, (175, 225))
            self.screen.blit(self.go_to_menu, (175, 425))
            self.screen.blit(self.record, (100, 150))
            self.screen.blit(self.current_score, (100, 100))
            pygame.display.flip()


class Shop:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.size = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load("data/space.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 1000))
        self.ufo = load_image("ufo.png")
        self.ufo1 = load_image("ufo1.png")
        self.ufo2 = load_image("ufo2.png")
        self.ufo = pygame.transform.scale(self.ufo, (150, 75))
        self.ufo1 = pygame.transform.scale(self.ufo1, (150, 75))
        self.ufo2 = pygame.transform.scale(self.ufo2, (150, 75))
        self.font = pygame.font.SysFont("microsofttaile", 24)
        self.back = self.font.render("Back", 1, WHITE)
        self.render()

    def render(self):
        global player_image
        self.working = True
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 25 <= pygame.mouse.get_pos()[0] <= 175 and 25 <= pygame.mouse.get_pos()[1] <= 75:
                        self.working = False
                        main = Main()
                    if 25 <= pygame.mouse.get_pos()[0] <= 225 and 125 <= pygame.mouse.get_pos()[1] <= 250:
                        player_image = "ufo.png"
                    if 225 <= pygame.mouse.get_pos()[0] <= 425 and 125 <= pygame.mouse.get_pos()[1] <= 250:
                        player_image = "ufo1.png"
                    if 425 <= pygame.mouse.get_pos()[0] <= 625 and 125 <= pygame.mouse.get_pos()[1] <= 250:
                        player_image = "ufo2.png"
                    print(player_image)
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.back, (75, 35))
            if player_image == "ufo.png":
                pygame.draw.rect(self.screen, WHITE, (25, 125, 200, 125), 2)
            if player_image == "ufo1.png":
                pygame.draw.rect(self.screen, WHITE, (225, 125, 200, 125), 2)
            if player_image == "ufo2.png":
                pygame.draw.rect(self.screen, WHITE, (425, 125, 200, 125), 2)
            pygame.draw.rect(self.screen, WHITE, (25, 25, 150, 50), 2)
            self.screen.blit(self.ufo, (50, 150))
            self.screen.blit(self.ufo1, (250, 150))
            self.screen.blit(self.ufo2, (450, 150))
            pygame.display.flip()


main = Main()
