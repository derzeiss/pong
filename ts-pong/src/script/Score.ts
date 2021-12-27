import { DEFAULT_FONT, POINTS_TO_WIN } from './config';
import { Game } from './Game';

export class Score {
  private x: number;
  private y: number;
  private score: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
    this.score = 0;
  }

  handle_input() {}

  update() {}

  render(ctx: CanvasRenderingContext2D) {
      ctx.fillText(this.score.toString(), this.x, this.y);
  }
  getScore() {
    return this.score;
  }
  addScore() {
    this.score += 1;
    return this.score >= POINTS_TO_WIN;
  }
}
