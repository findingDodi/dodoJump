import pygame
import pygame.sprite

import conf


class ParallaxSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/images/background.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.STEP = 9
        self.MARGIN = 12
        self.xstep = self.STEP
        self.ystep = 0
        self.dizzy = 0
        self.degrees = 0
        self.direction = 'left'

    def update(self):
        if self.degrees:
            self._spin()
        else:
            self._move()

    def _move(self):
        newpos = self.rect.move((self.xstep, self.ystep))
        '''
        if self.direction == 'right' and self.rect.right > self.area.right - self.MARGIN:
            self.xstep = 0
            self.ystep = self.STEP
            self.direction = 'down'

        if self.direction == 'down' and self.rect.bottom > self.area.bottom - self.MARGIN:
            self.xstep = -self.STEP
            self.ystep = 0
            self.direction = 'left'

        if self.direction == 'left' and self.rect.left < self.area.left + self.MARGIN:
            self.xstep = 0
            self.ystep = -self.STEP
            self.direction = 'up'

        if self.direction == 'up' and self.rect.top < self.area.top + self.MARGIN:
            self.xstep = self.STEP
            self.ystep = 0
            self.direction = 'right'
        '''

        self.xstep = -self.STEP
        self.rect = newpos


    def _spin(self):
        pass


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

        #print(self.air_time)
        if self.air_time > 1000:
            if self.dodo_position_y < self.dodo_max_position_y:
                self.dodo_position_y += 20
                self.dodo_is_grounded = True
                self.air_time = 0

    def run_game(self):
        SCREENWIDTH = conf.SCREEN_SIZE[0]
        SCREENHEIGHT = conf.SCREEN_SIZE[1]

        pygame.init()
        pygame.display.set_caption("Dodo Jump")
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
        clock = pygame.time.Clock()
        self.game_is_running = True

        background = ParallaxSprite()
        backgroundSprite = pygame.sprite.RenderPlain(background)

        while self.game_is_running:
            # limit framespeed to 30fps
            self.time_passed = clock.tick(30)
            if not self.dodo_is_grounded:
                self.air_time += self.time_passed

            self.screen.fill((55, 55, 55), self.background_rect)
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

            backgroundSprite.update()
            backgroundSprite.draw(self.screen)

            # final draw
            pygame.display.flip()


my_game = TestGame()
my_game.run_game()
