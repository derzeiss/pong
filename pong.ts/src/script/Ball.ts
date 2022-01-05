import { Bar } from './Bar';
import { BALL_SIZE, HEIGHT, WIDTH, BALL_ACC, BALL_SPEED_Y_MAX, BALL_SPEED_X_MIN } from './config';
import { Game } from './Game';
import { IGameObject } from './types';
import { randint } from './util';

export class Ball implements IGameObject {
  private game: Game;
  private x: number;
  private y: number;
  private lastX: number;
  private lastY: number;
  private width: number;
  private height: number;
  private vx: number;
  private vy: number;

  constructor(game: Game, x = 0, y = 0) {
    this.game = game;
    this.x = x;
    this.y = y;
    this.lastX = x;
    this.lastY = y;
    this.width = BALL_SIZE;
    this.height = BALL_SIZE;
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

  handle_input() {}

  update() {
    // update position
    this.lastX = this.x;
    this.lastY = this.y;
    this.x += this.vx;
    this.y += this.vy;

    // check if ball collided on top or bot -> bounce from wall
    if (this.y < 0) {
      // collided top
      this.y = 0;
      this.vy *= -1;
    } else if (this.y > HEIGHT - this.height) {
      // collided bottom
      this.y = HEIGHT - this.height;
      this.vy *= -1;
    }

    // check if ball hit screen bounds left or right -> score
    if (0 >= this.x) {
      // collided left
      if (!this.game.scorePlayer2.addScore()) {
        this.respawn(1);
      }
    } else if (this.x >= WIDTH - this.width) {
      if (!this.game.scorePlayer1.addScore()) {
        this.respawn(-1);
      }
    }

    // check if collided with bar
    if (this.collidedWithBar(this.game.player1)) {
      this.x = this.game.player1.getX() + this.game.player1.getWidth();
      this.bounceFromPlayer(this.game.player1);
    } else if (this.collidedWithBar(this.game.player2)) {
      this.x = this.game.player2.getX() - this.width;
      this.bounceFromPlayer(this.game.player2);
    }
  }

  collidedWithBar(bar: Bar) {
    const averageY = (this.lastY + this.y) / 2;
    const barX = bar.getX();
    const barY = bar.getY();
    if (averageY + this.height < barY) return false; // ball is over the bar
    if (averageY > barY + bar.getHeight()) return false; // ball is beneath the bar
    if (Math.sign(barX - this.x) === Math.sign(barX - this.lastX)) return false; // ball didn't travel through bar last frame
    return true;
  }

  bounceFromPlayer(player: Bar) {
    this.vx = -(this.vx * BALL_ACC);
    this.vy = ((this.y - player.getY()) / player.getHeight()) * BALL_SPEED_Y_MAX - BALL_SPEED_Y_MAX / 2;
  }

  render(ctx: CanvasRenderingContext2D) {
    ctx.rect(this.x, this.y, this.width, this.height);
  }

  getRandomDirection() {
    if (Math.random() < 0.5) return -1;
    return 1;
  }

  respawn(direction = 0) {
    if (direction == 0) {
      direction = this.getRandomDirection();
    }
    this.x = WIDTH / 2;
    this.y = HEIGHT / 2;
    this.vx = BALL_SPEED_X_MIN * direction;
    this.vy = randint(-BALL_SPEED_Y_MAX, BALL_SPEED_Y_MAX);
  }
}
