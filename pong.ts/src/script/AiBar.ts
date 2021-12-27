import { Bar } from "./Bar";

export class AIBar extends Bar {
  handle_input() {}
}

export class LowIntelligenceAIBar extends AIBar {
  handle_input() {
    const ball = this.game.ball;
    const ball_center = ball.getY() + ball.getHeight() / 2;
    const self_center = this.getY() + this.getHeight() / 2;
    if (Math.abs(ball_center - self_center) > 5) {
      // prevent ball flickering
      if (ball_center < self_center) {
        this.move_up();
      } else if (ball_center > self_center) {
        this.move_down();
      }
    }
  }
}