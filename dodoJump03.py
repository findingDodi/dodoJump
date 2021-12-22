import pygame
import conf


class TestGame:

    def __init__(self):
        self.screen = None
        self.game_is_running = True
        self.last_event = None
        self.dodo_position_y = conf.SCREEN_SIZE[1] - 20
        self.dodo_min_position_y = conf.SCREEN_SIZE[1] - 40
        self.dodo_max_position_y = conf.SCREEN_SIZE[1] - 20
        self.time_passed = 0
        self.air_time = 0
        self.dodo_is_grounded = True

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
        self.background_streets2 = pygame.image.load('./assets/images/04_streets.png')
        self.background_streets_rect2 = self.background_streets2.get_rect()

        self.background_sky_rect2[0] = self.background_sky_rect1[2]
        self.background_clouds_rect2[0] = self.background_clouds_rect1[2]
        self.background_buildings_rect2[0] = self.background_buildings_rect1[2]
        self.background_streets_rect2[0] = self.background_streets_rect1[2]

        self.background_rect = pygame.Rect(0, 0, conf.SCREEN_SIZE[0], conf.SCREEN_SIZE[1])

    def draw_dodo(self):
        box_color = (245, 101, 44)
        pygame.draw.rect(self.screen, box_color, (10, self.dodo_position_y, 20, 20))

    def dodo_control(self, event):
        if event.key == pygame.K_UP and self.dodo_is_grounded:
            self.last_event = pygame.K_UP

    def jump(self):
        if self.last_event == pygame.K_UP:
            if self.dodo_position_y > self.dodo_min_position_y:
                self.dodo_position_y -= 20
                self.dodo_is_grounded = False
                self.last_event = None

        if self.air_time > 1000:
            if self.dodo_position_y < self.dodo_max_position_y:
                self.dodo_position_y += 20
                self.dodo_is_grounded = True
                self.air_time = 0

    def scroll_image(self):

        self.background_sky_rect1[0] -= int(self.time_passed * 0.05)
        self.background_sky_rect2[0] -= int(self.time_passed * 0.05)

        self.background_clouds_rect1[0] -= int(self.time_passed * 0.15)
        self.background_clouds_rect2[0] -= int(self.time_passed * 0.15)

        self.background_buildings_rect1[0] -= int(self.time_passed * 0.15)
        self.background_buildings_rect2[0] -= int(self.time_passed * 0.15)

        self.background_streets_rect1[0] -= int(self.time_passed * 0.2)
        self.background_streets_rect2[0] -= int(self.time_passed * 0.2)

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

    def run_game(self):
        screen_width = conf.SCREEN_SIZE[0]
        screen_height = conf.SCREEN_SIZE[1]

        pygame.init()
        pygame.display.set_caption("Dodo Jump")
        self.screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
        clock = pygame.time.Clock()
        self.game_is_running = True

        while self.game_is_running:
            # limit framespeed to 30fps
            self.time_passed = clock.tick(25)
            print(self.time_passed)
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

            self.scroll_image()
            self.border_patrol()

            self.jump()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_is_running = False
                    else:
                        self.dodo_control(event)

            self.draw_dodo()
            # final draw
            pygame.display.flip()


my_game = TestGame()
my_game.run_game()
