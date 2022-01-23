import pygame
import conf
import random
import time


class TestGame:

    # Funktion zur Initialisierung der Instanzvariablen aka Constructor
    def __init__(self):
        self.screen = None
        self.game_is_running = True
        self.last_event = None
        self.dodo_position_x = 20
        self.dodo_position_y = conf.SCREEN_SIZE[1] - 20
        self.dodo_min_position_y = conf.SCREEN_SIZE[1] - 40
        self.dodo_max_position_y = conf.SCREEN_SIZE[1] - 20
        self.time_passed = 0
        self.air_time = 0
        self.dodo_is_grounded = True
        self.score = 0
        self.game_stopped = False
        self.time = 0
        self.time_game_start = 0
        self.highscore = 0

        self.background_sky1 = pygame.image.load('./assets/images/01_sky.png')
        self.background_sky_rect1 = self.background_sky1.get_rect()
        self.background_sky2 = pygame.image.load('./assets/images/01_sky.png')
        self.background_sky_rect2 = self.background_sky2.get_rect()

        self.background_clouds1 = pygame.image.load('./assets/images/02_clouds.png')
        self.background_clouds_rect1 = self.background_clouds1.get_rect()
        self.background_clouds2 = pygame.image.load('./assets/images/02_clouds.png')
        self.background_clouds_rect2 = self.background_clouds2.get_rect()

        self.background_buildings1 = pygame.image.load('./assets/images/03_buildings.png')
        self.background_buildings_rect1 = self.background_buildings1.get_rect()
        self.background_buildings2 = pygame.image.load('./assets/images/03_buildings.png')
        self.background_buildings_rect2 = self.background_buildings2.get_rect()

        self.background_streets1 = pygame.image.load('./assets/images/04_streets.png')
        self.background_streets_rect1 = self.background_streets1.get_rect()
        self.background_streets_rect1[1] = conf.SCREEN_SIZE[1] - self.background_streets_rect1[3]
        self.background_streets2 = pygame.image.load('./assets/images/04_streets.png')
        self.background_streets_rect2 = self.background_streets2.get_rect()
        self.background_streets_rect2[1] = conf.SCREEN_SIZE[1] - self.background_streets_rect2[3]

        self.background_sky_rect2[0] = self.background_sky_rect1[2]
        self.background_clouds_rect2[0] = self.background_clouds_rect1[2]
        self.background_buildings_rect2[0] = self.background_buildings_rect1[2]
        self.background_streets_rect2[0] = self.background_streets_rect1[2]

        self.dodo = pygame.image.load('./assets/images/dodo.png')
        self.dodo_rect = self.dodo.get_rect()
        self.dodo_rect[1] = conf.SCREEN_SIZE[1] - self.dodo_rect[3]
        self.dodo_rect[0] = self.dodo_position_x

        self.trashcan = pygame.image.load('./assets/images/trashcan_small.png')
        self.trashcan_rect = self.trashcan.get_rect()
        self.trashcan_rect[0] = conf.SCREEN_SIZE[1] - 20
        self.trashcan_rect[1] = conf.SCREEN_SIZE[1] - (self.trashcan_rect[3] * 1.5)

        self.trashcan2 = pygame.image.load('./assets/images/trashcan_small.png')
        self.trashcan_rect2 = self.trashcan2.get_rect()
        self.trashcan_rect2[0] = conf.SCREEN_SIZE[1] + 1000
        self.trashcan_rect2[1] = conf.SCREEN_SIZE[1] - (self.trashcan_rect2[3] * 1.5)

        self.background_rect = pygame.Rect(0, 0, conf.SCREEN_SIZE[0], conf.SCREEN_SIZE[1])

    # Funktion, die eine Box malt
    def draw_box(self):
        box_color = (245, 101, 44)
        pygame.draw.rect(self.screen, box_color, (self.dodo_position_x, self.dodo_position_y, 20, 20))

    # Funktion, die das aktuelle Event als letztes Event abspeichert
    def dodo_control(self, event):
        if event.key == pygame.K_UP and self.dodo_is_grounded:
            self.last_event = pygame.K_UP

    # Funktion, die ein Objekt springen und automatisch wieder zu Boden kommen lässt
    def jump(self):
        if self.last_event == pygame.K_UP:
            if self.dodo_position_y > self.dodo_min_position_y:
                self.dodo_position_y -= self.dodo_rect[3]
                self.dodo_rect[1] -= self.dodo_rect[3]
                self.dodo_is_grounded = False
                self.last_event = None

        if self.air_time > 1000:
            if self.dodo_position_y < self.dodo_max_position_y:
                self.dodo_position_y += self.dodo_rect[3]
                self.dodo_rect[1] += self.dodo_rect[3]
                self.dodo_is_grounded = True
                self.air_time = 0

    # Funktion, die die Hintergründe in verschiedenen Tempos nach links verschiebt
    def scroll_image(self):

        self.background_sky_rect1[0] -= int(self.time_passed * 0.05)
        self.background_sky_rect2[0] -= int(self.time_passed * 0.05)

        self.background_clouds_rect1[0] -= int(self.time_passed * 0.15)
        self.background_clouds_rect2[0] -= int(self.time_passed * 0.15)

        self.background_buildings_rect1[0] -= int(self.time_passed * 0.15)
        self.background_buildings_rect2[0] -= int(self.time_passed * 0.15)

        self.background_streets_rect1[0] -= int(self.time_passed * 0.2)
        self.background_streets_rect2[0] -= int(self.time_passed * 0.2)

        self.trashcan_rect[0] -= int(self.time_passed * 0.2)
        self.trashcan_rect2[0] -= int(self.time_passed * 0.2)

    # Funktion, die checkt, welche Hintergründe wieder hinten angefügt werden müssen, um den Parallax Effekt zu erhalten
    def border_patrol(self):

        if self.background_sky_rect1[0] <= -self.background_sky_rect1[2]:
            self.background_sky_rect1[0] = self.background_sky_rect2[0] + self.background_sky_rect2[2]
        elif self.background_sky_rect2[0] <= -self.background_sky_rect2[2]:
            self.background_sky_rect2[0] = self.background_sky_rect1[0] + self.background_sky_rect1[2]

        if self.background_clouds_rect1[0] <= -self.background_clouds_rect1[2]:
            self.background_clouds_rect1[0] = self.background_clouds_rect2[0] + self.background_clouds_rect2[2]
        elif self.background_clouds_rect2[0] <= -self.background_clouds_rect2[2]:
            self.background_clouds_rect2[0] = self.background_clouds_rect1[0] + self.background_clouds_rect1[2]

        if self.background_buildings_rect1[0] <= -self.background_buildings_rect1[2]:
            self.background_buildings_rect1[0] = self.background_buildings_rect2[0] + self.background_buildings_rect2[2]
        elif self.background_buildings_rect2[0] <= -self.background_buildings_rect2[2]:
            self.background_buildings_rect2[0] = self.background_buildings_rect1[0] + self.background_buildings_rect1[2]

        if self.background_streets_rect1[0] <= -self.background_streets_rect1[2]:
            self.background_streets_rect1[0] = self.background_streets_rect2[0] + self.background_streets_rect2[2]
        elif self.background_streets_rect2[0] <= -self.background_streets_rect2[2]:
            self.background_streets_rect2[0] = self.background_streets_rect1[0] + self.background_streets_rect1[2]

    # Funktion, die die Mülltonnen zufällig positioniert
    def random_position_trashcans(self):
        if self.trashcan_rect[0] <= -conf.SCREEN_SIZE[0]:
            self.trashcan_rect[0] = conf.SCREEN_SIZE[0] + random.randrange(1, conf.SCREEN_SIZE[0], 200)
        if self.trashcan_rect2[0] <= -conf.SCREEN_SIZE[0]:
            self.trashcan_rect2[0] = conf.SCREEN_SIZE[0] + random.randrange(1, conf.SCREEN_SIZE[0], 200)

    # Funktion, die auf Kollision zwischen Dodo und Mülltonne prüft und das Spiel beendet
    def collide_patrol(self):
        if self.dodo_rect.colliderect(self.trashcan_rect) or self.dodo_rect.colliderect(self.trashcan_rect2):
            self.game_stopped = True

    def draw_game_over_screen(self):
        if self.game_stopped == True:
            font = pygame.font.SysFont('ComicNeue-Regular', 40)
            font_color = (255, 255, 255)
            font_position = ((conf.SCREEN_SIZE[0] / 2 - 90), conf.SCREEN_SIZE[1] / 2 - 30)
            font_position2 = ((conf.SCREEN_SIZE[0] / 2 - 160), conf.SCREEN_SIZE[1] / 2 + 10)
            font_position3 = ((conf.SCREEN_SIZE[0] / 2 - 140), conf.SCREEN_SIZE[1] / 2 + 50)
            font_position4 = ((conf.SCREEN_SIZE[0] / 2 - 160), conf.SCREEN_SIZE[1] / 2 + 90)
            font_position5 = ((conf.SCREEN_SIZE[0] / 2 - 240), conf.SCREEN_SIZE[1] / 2 + 130)
            self.screen.fill((55, 55, 55), self.background_rect)
            self.screen.blit(font.render('GAME OVER', True, font_color), font_position)
            self.screen.blit(font.render('PRESS R TO RESTART', True, font_color), font_position2)
            self.screen.blit(font.render('YOUR SCORE: ' + str(self.score), True, font_color), font_position3)
            self.screen.blit(font.render('YOUR HIGHSCORE: ' + str(self.highscore), True, font_color), font_position4)
            if self.score > self.highscore:
                self.screen.blit(font.render('YOU SCORED A NEW HIGHSCORE!', True, font_color), font_position5)

    def calculate_score(self):
        self.time = time.time()
        self.score = self.time - self.time_game_start
        self.score = "{:.2f}".format(round(self.score, 2))
        self.score = float(self.score)

    def show_score(self):
        font = pygame.font.SysFont('ComicNeue', 40)
        font_color = (50, 50, 50)
        font_position = (10, 10)
        self.screen.blit(font.render(str(self.score), True, font_color), font_position)

    def check_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

    def restart_game(self):
        if self.game_stopped == True:
            self.trashcan_rect[0] = conf.SCREEN_SIZE[1] - 20
            self.trashcan_rect2[0] = conf.SCREEN_SIZE[1] + 1000
            self.game_stopped = False
            self.time_game_start = time.time()

    # Hauptfunktion, in der das Spiel läuft
    def run_game(self):
        screen_width = conf.SCREEN_SIZE[0]
        screen_height = conf.SCREEN_SIZE[1]

        pygame.init()
        pygame.display.set_caption("Dodo Jump")
        self.screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
        clock = pygame.time.Clock()
        self.game_is_running = True
        self.time_game_start = time.time()

        while self.game_is_running:
            # limit framespeed to 30fps
            self.time_passed = clock.tick(25)
            #print(self.time_passed)
            if not self.dodo_is_grounded:
                self.air_time += self.time_passed

            self.screen.fill((55, 55, 55), self.background_rect)

            self.screen.blit(self.background_sky1, self.background_sky_rect1)
            self.screen.blit(self.background_sky2, self.background_sky_rect2)

            self.screen.blit(self.background_clouds1, self.background_clouds_rect1)
            self.screen.blit(self.background_clouds2, self.background_clouds_rect2)

            self.screen.blit(self.background_buildings1, self.background_buildings_rect1)
            self.screen.blit(self.background_buildings2, self.background_buildings_rect2)

            self.screen.blit(self.background_streets1, self.background_streets_rect1)
            self.screen.blit(self.background_streets2, self.background_streets_rect2)

            self.screen.blit(self.dodo, self.dodo_rect)
            self.screen.blit(self.trashcan, self.trashcan_rect)
            self.screen.blit(self.trashcan2, self.trashcan_rect2)

            if self.game_stopped == False:
                self.calculate_score()
                self.show_score()
                self.scroll_image()
                self.border_patrol()
                self.collide_patrol()
                self.random_position_trashcans()
                self.jump()
            else:
                self.draw_game_over_screen()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_is_running = False
                    elif event.key == pygame.K_r:
                        self.check_highscore()
                        self.restart_game()
                    else:
                        self.dodo_control(event)

            #self.draw_box()
            # final draw
            pygame.display.flip()


my_game = TestGame()
my_game.run_game()
