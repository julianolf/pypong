import pygame

TITLE = 'PyPONG'
WIDTH, HEIGHT = 800, 600
WIN_SIZE = (WIDTH, HEIGHT)
BLOCK = 30
HALF_BLOCK = BLOCK // 2
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TOP = BLOCK
BOTTOM = HEIGHT - BLOCK


class Paddle(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((BLOCK, BLOCK * 3))
        image.fill(WHITE)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        if self.rect.y < TOP:
            self.rect.y = TOP
        elif self.rect.y > (BOTTOM - self.rect.height):
            self.rect.y = BOTTOM - self.rect.height


class Cpu(Paddle):
    def __init__(self, *args, **kwargs):
        position = (HALF_BLOCK, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)


class Player(Paddle):
    def __init__(self, *args, **kwargs):
        position = (WIDTH - HALF_BLOCK, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)

    def update(self):
        _, y = pygame.mouse.get_pos()
        bottom = HEIGHT - self.rect.height
        self.rect.y = bottom if y > bottom else y
        super().update()


class Wall(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((WIDTH, BLOCK))
        image.fill(WHITE)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = position


class Ball(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((BLOCK, BLOCK))
        pygame.draw.circle(image, WHITE, (HALF_BLOCK, HALF_BLOCK), HALF_BLOCK)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.radius = HALF_BLOCK


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()

    def reset(self):
        self.sprites.empty()
        self.player = Player((self.sprites,))
        self.cpu = Cpu((self.sprites,))
        self.wall_top = Wall((0, 0), (self.sprites,))
        self.wall_bottom = Wall((0, BOTTOM), (self.sprites,))
        self.ball = Ball((self.sprites,))
        self.running = True

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def loop(self):
        while self.running:
            self.clock.tick(FPS)
            self.update()
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

    def run(self):
        self.reset()
        self.loop()
        pygame.quit()


def main():
    Game().run()


if __name__ == '__main__':
    main()
