import { Bar } from "./Bar";

export class LowIntelligenceAIBar extends Bar {
  handleInput() {
    const ball = this.game.ball;
    const ball_center = ball.getY() + ball.getHeight() / 2;
    const self_center = this.getY() + this.getHeight() / 2;
    if (Math.abs(ball_center - self_center) > 5) {
      // prevent ball flickering
      if (ball_center < self_center) {
        this.moveUp();
      } else if (ball_center > self_center) {
        this.moveDown();
      }
    }
  }
}