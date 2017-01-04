import random
import sys
import time
import tkinter


class Game(tkinter.Canvas):
    # Game window dimensions
    WIDTH = 700
    HEIGHT = 600

    # Keys
    KEYS = {
        'up': 'Up',
        'down': 'Down'
    }

    # Color
    COL_PRIMARY = 'white'
    COL_SECONDARY = 'black'

    # Bar settings
    BAR_WIDTH = 20
    BAR_HEIGHT = 100
    BAR_SPEED = 5

    # Ball settings
    # Acceleration is applied on-hit
    BALL_SIZE = 20
    BALL_SPEED_X_MIN = 5
    BALL_SPEED_Y_MAX = 10
    BALL_ACC = 1.1

    # Points to win a game
    POINTS_TO_WIN = 5

    # Target FPS
    FPS = 60

    # Style settings
    DEFAULT_FONT = {
        'fill': COL_PRIMARY,
        'font': ("Consolas", 24, "bold")
    }

    def __init__(self, class_player1, class_player2):
        self.window = tkinter.Tk()
        super().__init__(self.window, width=Game.WIDTH, height=Game.HEIGHT, bg=Game.COL_SECONDARY,
                         highlightthickness="0")

        self.keys = None
        self.__objects = None

        # game objects
        self.class_player1 = class_player1
        self.class_player2 = class_player2
        self.player1 = None
        self.player2 = None
        self.score_player1 = None
        self.score_player2 = None
        self.ball = None

        # tkinter window props
        self.x = 0
        self.y = 0
        self.width = Game.WIDTH
        self.height = Game.HEIGHT
        self.screen_width = 0
        self.screen_height = 0

    def run(self):
        self.__objects = []

        # some helper
        game_width = Game.WIDTH
        game_width_2 = game_width // 2
        game_height = Game.HEIGHT
        game_height_2 = game_height // 2
        game_height_10 = game_height // 10

        bar_y = game_height_2 - Game.BAR_HEIGHT // 2

        # init objects
        self.player1 = self.class_player1(self, Game.BAR_WIDTH, bar_y)
        self.player2 = self.class_player2(self, Game.WIDTH - Game.BAR_WIDTH * 2, bar_y)

        self.score_player1 = Score(self, game_width_2 - game_height_10, game_height_10)
        self.score_player2 = Score(self, game_width_2 + game_height_10, game_height_10)

        self.ball = Ball(self)
        self.ball.respawn()

        # add objects to update circle
        self.add_object(self.player1)
        self.add_object(self.player2)
        self.add_object(self.score_player1)
        self.add_object(self.score_player2)
        self.add_object(self.ball)

        # init Tkinter window
        self.window.title("Pong")
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.window.resizable(False, False)
        self.window.focus_force()
        self.pack()

        # create middle line
        self.create_line(self.width / 2, 0, self.width / 2, self.height, width=3, dash=25, fill=Game.COL_PRIMARY)

        self.init_bindings()
        self.next_frame()
        self.window.mainloop()

    def next_frame(self):
        if not self.__check_win():
            self.__handle_input()
            self.__update()
            self.__render()
            self.window.after(int(1000 / Game.FPS), self.next_frame)

    def __check_win(self):
        if self.score_player1.get() >= Game.POINTS_TO_WIN:
            self.__win('Player 1')
            return True
        elif self.score_player2.get() >= Game.POINTS_TO_WIN:
            self.__win('Player 2')
            return True
        return False

    def __handle_input(self):
        for obj in self.__objects:
            obj.handle_input()

    def __update(self):
        for obj in self.__objects:
            obj.update()

    def __render(self):
        for obj in self.__objects:
            obj.render()

    def __win(self, msg):
        self.create_text(Game.WIDTH / 2, Game.HEIGHT / 2, text=msg + ' wins', **Game.DEFAULT_FONT)

    def add_object(self, obj):
        if obj not in self.__objects:
            self.__objects.append(obj)

    def init_bindings(self):
        self.keys = {}
        self.window.bind('<Escape>', lambda e: sys.exit())
        for command, key in Game.KEYS.items():
            self.window.bind('<%s>' % key, self.__key_press)
            self.window.bind('<KeyRelease-%s>' % key, self.__key_press)
            self.keys[key] = False

    def __key_press(self, event):
        self.keys[event.keysym] = event.type == '2'

    def is_pressed(self, key):
        return key in self.keys.keys() and self.keys[key]


class Score:
    def __init__(self, game, x, y):
        self.game = game
        self.__x = x
        self.__y = y
        self.__score = 0
        self.__dirty = 0
        self.__canvas_item = self.game.create_text(self.__x, self.__y, text=self.__score, **Game.DEFAULT_FONT)

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        if self.__dirty:
            self.game.itemconfig(self.__canvas_item, text=self.__score)
            self.__dirty = 0

    def get(self):
        return self.__score

    def score(self):
        self.__score += 1
        self.__dirty = 1
        return self.__score >= Game.POINTS_TO_WIN


class Bar:
    def __init__(self, game, x, y):
        self.game = game
        self.__x = x
        self.__y = y
        self.__width = Game.BAR_WIDTH
        self.__height = Game.BAR_HEIGHT
        self.__vx = 0
        self.__vy = 0
        self.__canvas_item = self.game.create_rectangle(
            self.__x, self.__y, self.__x + self.__width, self.__y + self.__height,
            width='0', tag='bar', fill=Game.COL_PRIMARY)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def vx(self):
        return self.__vx

    @property
    def vy(self):
        return self.__vy

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def handle_input(self):
        if self.game.is_pressed(Game.KEYS['up']):
            self.move_up()
        elif self.game.is_pressed(Game.KEYS['down']):
            self.move_down()

    def move_up(self):
        self.__vy = -Game.BAR_SPEED

    def move_down(self):
        self.__vy = Game.BAR_SPEED

    def update(self):
        # update position (inside screen boundaries)
        self.__y = min(max(self.__y + self.__vy, 0), Game.HEIGHT - self.__height)
        # reset velocity for next tick
        self.__vx = 0
        self.__vy = 0

    def render(self):
        self.game.coords(self.__canvas_item, self.__x, self.__y, self.__x + self.__width, self.__y + self.__height)


class AIBar(Bar):
    def handle_input(self):
        pass


class Ball:
    def __init__(self, game, x=0, y=0):
        self.game = game
        self.__x = x
        self.__y = y
        self.__width = Game.BALL_SIZE
        self.__height = Game.BALL_SIZE
        self.__vx = 0
        self.__vy = 0
        self.__canvas_item = self.game.create_rectangle(
            self.__x, self.__y, self.__x + self.__width, self.__y + self.__height,
            width='0', tag='ball', fill=Game.COL_PRIMARY)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def vx(self):
        return self.__vx

    @property
    def vy(self):
        return self.__vy

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def handle_input(self):
        pass

    def update(self):
        # update position
        self.__x += self.__vx
        self.__y += self.__vy

        # check if ball collided on top or bot -> bounce from wall
        if self.__y < 0:  # collided top
            self.__y = 0
            self.__vy *= -1
        elif self.__y > Game.HEIGHT - self.__height:  # collided bottom
            self.__y = Game.HEIGHT - self.__height
            self.__vy *= -1

        # check if ball collided on left or right -> score
        if 0 >= self.__x:  # collided left
            if not self.game.score_player2.score():
                self.respawn(1)

        elif self.__x >= Game.WIDTH - self.__width:
            if not self.game.score_player1.score():
                self.respawn(-1)

        # check if collided with bar
        if self.collides_with_object(self.game.player1):
            self.__x = self.game.player1.x + self.game.player1.width
            self.bounce_from_player(self.game.player1)
        elif self.collides_with_object(self.game.player2):
            self.__x = self.game.player2.x - self.__width
            self.bounce_from_player(self.game.player2)

    def bounce_from_player(self, player):
        self.__vx = -(self.vx * Game.BALL_ACC)
        self.__vy = (self.__y - player.y) / player.height * Game.BALL_SPEED_Y_MAX - Game.BALL_SPEED_Y_MAX // 2

    def render(self):
        self.game.coords(self.__canvas_item, self.__x, self.__y, self.__x + self.__width, self.__y + self.__height)

    def respawn(self, dir=None):
        if not dir: dir = random.choice((-1, 1))
        self.__x = Game.WIDTH // 2
        self.__y = Game.HEIGHT // 2
        self.__vx = Game.BALL_SPEED_X_MIN * dir
        self.__vy = random.randint(-Game.BALL_SPEED_Y_MAX, Game.BALL_SPEED_Y_MAX)

    def collides_with_object(self, obj):
        sx = self.__x
        sy = self.__y
        sw = self.__width
        sh = self.__height

        ox = obj.x
        oy = obj.y
        ow = obj.width
        oh = obj.height
        return sx < ox + ow and sy < oy + oh and ox < sx + sw and oy < sy + sh


class LowIntelligenceAIBar(AIBar):
    def handle_input(self):
        ball = self.game.ball
        ball_center = ball.y + ball.height // 2
        self_center = self.y + self.height // 2
        if abs(ball_center - self_center) > 5:  # prevent ball flickering
            if ball_center < self_center:
                self.move_up()
            elif ball_center > self_center:
                self.move_down()


if __name__ == '__main__':
    Game(Bar, LowIntelligenceAIBar).run()
