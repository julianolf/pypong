from random import randint

import pygame

TITLE = 'PyPONG'
WIDTH, HEIGHT = 800, 600
WIN_SIZE = (WIDTH, HEIGHT)
BLOCK = 20
HALF_BLOCK = BLOCK / 2
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TOP = 0
BOTTOM = HEIGHT
MID_WIDTH = WIDTH / 2


class Paddle(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((HALF_BLOCK, BLOCK * 4))
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
        position = (WIDTH - BLOCK * 2, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)


class Player(Paddle):
    def __init__(self, *args, **kwargs):
        position = (BLOCK * 2, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)

    def update(self):
        _, y = pygame.mouse.get_pos()
        bottom = HEIGHT - self.rect.height
        self.rect.y = bottom if y > bottom else y
        super().update()


class Ball(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((BLOCK, BLOCK))
        image.fill(BLACK)
        image.set_colorkey(BLACK)
        pygame.draw.circle(image, WHITE, (HALF_BLOCK, HALF_BLOCK), HALF_BLOCK)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (MID_WIDTH, HEIGHT / 2)
        self.radius = HALF_BLOCK
        self.velocity = pygame.Vector2(randint(6, 9), randint(-8, 8))

    def update(self):
        if self.rect.x <= 0 or self.rect.x >= (WIDTH - self.rect.width):
            self.velocity.x *= -1
        if self.rect.y <= TOP or self.rect.y >= (BOTTOM - self.rect.height):
            self.velocity.y *= -1

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def bounce(self):
        self.velocity.x += randint(-2, 2)
        self.velocity.x *= -1
        self.velocity.y = randint(-8, 8)


class Net(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((2, HEIGHT))
        image.fill(BLACK)
        image.set_colorkey(BLACK)
        points = tuple(range(0, HEIGHT, 10))
        coords = ((points[i], points[i + 1]) for i in range(len(points) - 1))
        for i, coord in enumerate(coords):
            if i % 2 != 0:
                start, end = coord
                pygame.draw.line(image, WHITE, (0, start), (0, end), 2)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.midtop = (MID_WIDTH, 0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()

    def reset(self):
        self.sprites.empty()
        self.paddles.empty()
        self.net = Net((self.sprites,))
        self.player = Player((self.sprites, self.paddles))
        self.cpu = Cpu((self.sprites, self.paddles))
        self.ball = Ball((self.sprites,))
        self.running = True

    def update(self):
        self.sprites.update()

        if pygame.sprite.spritecollide(
            self.ball,
            self.paddles,
            False,
            pygame.sprite.collide_rect_ratio(0.85),
        ):
            self.ball.bounce()

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
