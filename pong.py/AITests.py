import pong


class BasicIntelligenceAIBar(pong.AIBar):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        if self.x < game.width // 2:  # left player
            self.callbacks = [self.on_self_hit, self.on_enemy_hit]
        else:
            self.callbacks = [self.on_enemy_hit, self.on_self_hit]
        self.last_ball_vx = 0
        self.target = game.height // 2

    def handle_input(self):
        self.check_for_hit()
        self.goto_target()

    def check_for_hit(self):
        ball = self.game.ball
        if self.last_ball_vx * ball.vx < 0:  # ball direction changed
            if ball.vx > 0:  # left player hit
                self.callbacks[0]()
            else:
                self.callbacks[1]()
        self.last_ball_vx = ball.vx

    def goto_target(self):
        self_y = self.y
        target = self.target
        if not target:
            return
        if target == 'dynamic':
            target = self.game.ball.y
        if abs(self_y - target) < 5:
            return
        if self_y < target:
            self.move_down()
        else:
            self.move_up()

    def on_enemy_hit(self):
        self.target = 'dynamic'

    def on_self_hit(self):
        self.target = self.game.height // 2 - self.height // 2

if __name__ == '__main__':
    pong.Game(pong.LowIntelligenceAIBar, BasicIntelligenceAIBar).run()