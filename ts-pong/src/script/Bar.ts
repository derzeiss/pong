import { BAR_WIDTH, BAR_HEIGHT, KEYS, BAR_SPEED, HEIGHT } from './config';
import { Game } from './Game';
import { IGameObject } from './types';

export class Bar implements IGameObject {
  protected game: Game;
  private x: number;
  private y: number;
  private width: number;
  private height: number;
  private vx: number;
  private vy: number;

  constructor(game: Game, x: number, y: number) {
    this.game = game;
    this.x = x;
    this.y = y;
    this.width = BAR_WIDTH;
    this.height = BAR_HEIGHT;
    this.vx = 0;
    this.vy = 0;
  }

  getX() {
    return this.x;
  }

  getY() {
    return this.y;
  }

  getVx() {
    return this.vx;
  }

  getVy() {
    return this.vy;
  }

  getWidth() {
    return this.width;
  }

  getHeight() {
    return this.height;
  }

  handle_input() {
    if (this.game.is_pressed(KEYS['up'])) {
      this.move_up();
    } else if (this.game.is_pressed(KEYS['down'])) {
      this.move_down();
    }
  }

  move_up() {
    this.vy = -BAR_SPEED;
  }

  move_down() {
    this.vy = BAR_SPEED;
  }

  dont_move() {
    this.vy = 0;
  }

  update() {
    // update position (inside screen boundaries)
    this.y = Math.min(Math.max(this.y + this.vy, 0), HEIGHT - this.height);
    // reset velocity for next tick
    this.vx = 0;
    this.vy = 0;
  }

  render(ctx: CanvasRenderingContext2D) {
    ctx.rect(this.x, this.y, this.width, this.height);
  }
}
