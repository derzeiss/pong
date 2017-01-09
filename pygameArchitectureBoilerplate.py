import pygame


class Game:
    # Game window dimensions
    WIDTH = 800
    HEIGHT = 600

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

    SUBTYPE_NONE = 0
    SUBTYPE_INPUT_HUMAN = 1

    TypeId = TYPE_COMP
    SubtypeId = SUBTYPE_NONE

    def __init__(self):
        self.obj = None

    def update(self):
        pass

    def on_event(self, event):
        pass


class InputComponent(Component):
    TypeId = Component.TYPE_INPUT_COMP


class PhysicsComponent(Component):
    TypeId = Component.TYPE_PHYSICS_COMP

    def __init__(self):
        super().__init__()
        self.vx = 0
        self.vy = 0


class SolidBodyComponent(Component):
    TypeId = Component.TYPE_SOLID_BODY_COMP

    def on_collide(self, comp):
        pass


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


class DirtyGraphicsComponent(GraphicsComponent, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        GraphicsComponent.__init__(self)


class EventEmitter:
    def __init__(self):
        self.__subscriber = []

    def add_subscriber(self, subscriber):
        if subscriber not in self.__subscriber and hasattr(subscriber, 'on_event'):
            self.__subscriber.append(subscriber)
            return True
        return False

    def emit(self, event):
        for subscriber in self.__subscriber:
            subscriber.on_event(event)


class EventSubscriber:
    def on_event(self):
        pass


class Event:
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_STOP = 3
    SCORE_PLAYER1 = 4
    SCORE_PLAYER2 = 5

    def __init__(self, _type):
        self.type = _type


if __name__ == '__main__':
    Game().run()
