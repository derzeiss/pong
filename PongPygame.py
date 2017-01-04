import math
import pygame
import random

# TODO Rects only work with int, get float vy to work
# TODO physics on_collide
# TODO scores


class Game:
    # Game window dimensions
    WIDTH = 700
    HEIGHT = 600

    # Keys
    PLAYER_KEYS = {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN
    }

    # Color
    COL_COLORKEY = pygame.Color('magenta')
    COL_PRIMARY = pygame.Color('white')
    COL_SECONDARY = pygame.Color('black')

    # Bar settings
    BAR_WIDTH = 20
    BAR_HEIGHT = 100
    BAR_SPEED = 1

    # Ball settings
    # Acceleration is applied on-hit
    BALL_SIZE = 20
    BALL_SPEED_X_MIN = 1
    BALL_SPEED_Y_MAX = 2
    BALL_ACC = 1.1

    # Points to win a game
    POINTS_TO_WIN = 5

    # Target FPS
    FPS = 60

    # Style settings TODO necessary?
    pygame.font.init()
    FONT = pygame.font.SysFont('Consolas', 24)

    def __init__(self):
        self.components = None
        self.objects = None
        self.sprites = None
        self.subscribers = None

        # pygame props
        self.__running = True
        self.__clock = pygame.time.Clock()
        self.__screen = None
        self.__bg = None

    def run(self):
        self.__init_components()
        self.objects = []
        self.subscribers = []
        self.sprites = pygame.sprite.Group()

        # -- create game objects --
        # helper
        game_width_2 = Game.WIDTH // 2

        # images
        self.__bg = pygame.Surface((Game.WIDTH, Game.HEIGHT))
        self.__bg.fill(Game.COL_SECONDARY)
        draw_dashed_line(self.__bg, Game.COL_PRIMARY, (game_width_2, 0), (game_width_2, Game.HEIGHT), 3, 25)

        image_bar = pygame.Surface((Game.BAR_WIDTH, Game.BAR_HEIGHT))
        image_bar.fill(Game.COL_PRIMARY)

        image_ball = pygame.Surface((Game.BALL_SIZE, Game.BALL_SIZE))
        image_ball.fill(Game.COL_PRIMARY)

        # Components
        bar1_input = PlayerBarInputComponent()
        bar1_physics = BarPhysicsComponent()
        bar1_solidbody = BarSolidBodyComponent()
        bar1_graphics = StaticGraphicsComponent(image_bar)

        bar2_input = PlayerBarInputComponent()
        bar2_physics = BarPhysicsComponent()
        bar2_solidbody = BarSolidBodyComponent()
        bar2_graphics = StaticGraphicsComponent(image_bar)

        ball_physics = BallPhysicsComponent()
        ball_solidbody = BallSolidBodyComponent()
        ball_graphics = StaticGraphicsComponent(image_ball)

        # GameObjects
        bar_y = (Game.HEIGHT - Game.BAR_HEIGHT) // 2

        bar1 = GameObject(self, Game.BAR_WIDTH, bar_y, Game.BAR_WIDTH, Game.BAR_HEIGHT)
        bar1.add_component(bar1_input)
        bar1.add_component(bar1_physics)
        bar1.add_component(bar1_solidbody)
        bar1.add_component(bar1_graphics)

        bar2 = GameObject(self, Game.WIDTH - Game.BAR_WIDTH * 2, bar_y, Game.BAR_WIDTH, Game.BAR_HEIGHT)
        bar2.add_component(bar2_input)
        bar2.add_component(bar2_physics)
        bar2.add_component(bar2_solidbody)
        bar2.add_component(bar2_graphics)

        ball = GameObject(self, 0, 0, Game.BALL_SIZE, Game.BALL_SIZE)
        ball.add_component(ball_physics)
        ball.add_component(ball_solidbody)
        ball.add_component(ball_graphics)
        ball_physics.respawn()

        self.add_object(bar1)
        self.add_object(bar2)
        self.add_object(ball)

        self.__screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.__screen.blit(self.__bg, (0, 0))
        self.update()

    def update(self):
        while self.__running:
            self.__clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.__running = False

            for comp_list in self.components:
                for comp in comp_list:
                    comp.update()

            self.sprites.clear(self.__screen, self.__bg)
            self.sprites.draw(self.__screen)

            pygame.display.flip()

    def add_object(self, obj):
        self.objects.append(obj)
        for comp in obj.components.values():
            self.components[comp.TypeId].append(comp)
            if comp.TypeId == Component.TYPE_GRAPHICS_COMP:
                self.sprites.add(comp)

    def __init_components(self):
        self.components = []
        for n in range(Component.TYPES_AMOUNT):
            self.components.append([])

    def emit(self, event):
        for obj in self.subscribers:
            obj.on_event(event)


class GameObject:
    def __init__(self, game, *args):
        self.game = game
        self.components = {}  # dict for components. Keys are Component.TYPE_...

        if hasattr(args[0], 'x'):
            self.rect = args[0]
        else:
            self.rect = pygame.Rect(*args)

    def add_component(self, comp):
        self.components[comp.TypeId] = comp
        comp.obj = self

    def emit(self, event):
        for comp in self.components.values():
            comp.on_event(event)


class Component:
    TYPES_AMOUNT = 5  # number of different component types
    TYPE_COMP = 0
    TYPE_INPUT_COMP = 1
    TYPE_PHYSICS_COMP = 2
    TYPE_SOLID_BODY_COMP = 3
    TYPE_GRAPHICS_COMP = 4

    TypeId = TYPE_COMP

    def __init__(self):
        self.obj = None

    def update(self):
        pass

    def on_event(self, event):
        pass


class InputComponent(Component):
    TypeId = Component.TYPE_INPUT_COMP


class PlayerBarInputComponent(InputComponent):
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[Game.PLAYER_KEYS['up']]:
            self.obj.emit(Event(Event.MOVE_UP))
        elif keys_pressed[Game.PLAYER_KEYS['down']]:
            self.obj.emit(Event(Event.MOVE_DOWN))
        else:
            self.obj.emit(Event(Event.MOVE_STOP))


class PhysicsComponent(Component):
    TypeId = Component.TYPE_PHYSICS_COMP

    def __init__(self):
        super().__init__()
        self.vx = 0
        self.vy = 0


class BarPhysicsComponent(PhysicsComponent):
    def on_event(self, event):
        if event.type == Event.MOVE_UP:
            self.move_up()
        elif event.type == Event.MOVE_DOWN:
            self.move_down()
        elif event.type == Event.MOVE_STOP:
            self.move_stop()

    def update(self):
        self.obj.rect.top = self.obj.rect.y + self.vy
        if self.obj.rect.top < 0:
            self.obj.rect.top = 0
        elif self.obj.rect.bottom > Game.HEIGHT:
            self.obj.rect.bottom = Game.HEIGHT

    def move_up(self):
        self.vy = -Game.BAR_SPEED

    def move_down(self):
        self.vy = Game.BAR_SPEED

    def move_stop(self):
        self.vy = 0


class BallPhysicsComponent(PhysicsComponent):
    def update(self):
        obj = self.obj
        obj.rect = obj.rect.move(self.vx, self.vy)

        # handle wall collisions
        # top
        if obj.rect.top < 0:
            obj.rect.top = 0
            self.vy *= -1
        # bottom
        elif obj.rect.bottom > Game.HEIGHT:
            obj.rect.bottom = Game.HEIGHT
            self.vy *= -1
        # left
        if obj.rect.left < 0:  # TODO emit score event
            self.respawn(1)
        elif obj.rect.right > Game.WIDTH:
            self.respawn(-1)

    def respawn(self, direction=None):
        if not direction:
            direction = random.choice((-1, 1))
        self.obj.rect.center = (Game.WIDTH // 2, Game.HEIGHT // 2)
        self.vx = Game.BALL_SPEED_X_MIN * direction
        self.vy = random.randint(-Game.BALL_SPEED_Y_MAX, Game.BALL_SPEED_Y_MAX)


class SolidBodyComponent(Component):
    TypeId = Component.TYPE_SOLID_BODY_COMP

    def on_collide(self, comp):
        pass


class BarSolidBodyComponent(SolidBodyComponent):
    pass


class BallSolidBodyComponent(SolidBodyComponent):
    def update(self):
        for comp in self.obj.game.components[Component.TYPE_SOLID_BODY_COMP]:
            if comp == self: continue
            if pygame.sprite.collide_rect(self.obj, comp.obj):
                comp.on_collide(self)
                self.bounce_from_bar(comp.obj)

    def bounce_from_bar(self, obj):
        self_obj = self.obj
        physics_comp = self_obj.components[Component.TYPE_PHYSICS_COMP]

        physics_comp.vx *= -Game.BALL_ACC
        if self_obj.rect.x < obj.rect.x:
            self_obj.rect.right = obj.rect.left
        else:
            self_obj.rect.left = obj.rect.right

        vy = (self_obj.rect.y - obj.rect.y) / obj.rect.height * Game.BALL_SPEED_Y_MAX - Game.BALL_SPEED_Y_MAX // 2
        physics_comp.vy = vy


class GraphicsComponent(Component):
    """
    IMPORTANT: Do not instantiate this class.
    You must subclass it and also inherit a pygame.sprite class
    """
    TypeId = Component.TYPE_GRAPHICS_COMP


# noinspection PyArgumentList
class StaticGraphicsComponent(GraphicsComponent, pygame.sprite.Sprite):
    def __init__(self, image=None):
        pygame.sprite.Sprite.__init__(self)
        GraphicsComponent.__init__(self)
        self.image = image
        self.rect = None

    def update(self):
        self.rect = self.obj.rect


class ScoreGraphicsComponent(GraphicsComponent, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        GraphicsComponent.__init__(self)


class Event:
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_STOP = 3
    SCORE_PLAYER1 = 4
    SCORE_PLAYER2 = 5

    def __init__(self, _type):
        self.type = _type


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a ** 2 + b ** 2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in range(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in range(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)


if __name__ == '__main__':
    Game().run()
