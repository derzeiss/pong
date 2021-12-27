import { Ball } from './Ball';
import { Bar } from './Bar';
import {
  WIDTH,
  HEIGHT,
  COL_PRIMARY,
  DEFAULT_FONT,
  Y_CENTER,
  BAR_HEIGHT,
  BAR_WIDTH,
  X_CENTER,
  POINTS_TO_WIN,
  COL_SECONDARY,
} from './config';
import { Score } from './Score';
import { IGameObject } from './types';

export class Game {
  private keys: { [ke: string]: boolean };
  private objects: IGameObject[];
  private player1Class: typeof Bar;
  private player2Class: typeof Bar;
  public player1!: Bar;
  public player2!: Bar;
  public scorePlayer1!: Score;
  public scorePlayer2!: Score;
  public ball!: Ball;
  private canvas!: HTMLCanvasElement;
  private ctx!: CanvasRenderingContext2D;

  constructor(canvasId: string, player1Class: typeof Bar, player2Class: typeof Bar) {
    this.keys = {};
    this.objects = [];

    this.initCanvas(canvasId);

    // game objects
    this.player1Class = player1Class;
    this.player2Class = player2Class;
  }

  initCanvas(canvasId: string) {
    this.canvas = document.getElementById(canvasId) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d') as CanvasRenderingContext2D;
    this.canvas.width = WIDTH;
    this.canvas.height = HEIGHT;

    this.ctx.strokeStyle = COL_PRIMARY;
    this.ctx.lineWidth = 3;
    this.ctx.setLineDash([10, 3]);
    this.ctx.font = DEFAULT_FONT;
    this.ctx.textAlign = 'center';
  }

  run() {
    this.objects = [];

    // some helper
    const game_height_10 = HEIGHT / 10;

    const bar_y = Y_CENTER - BAR_HEIGHT / 2;

    // init objects
    this.player1 = new this.player1Class(this, BAR_WIDTH, bar_y);
    this.player2 = new this.player2Class(this, WIDTH - BAR_WIDTH * 2, bar_y);

    this.scorePlayer1 = new Score(X_CENTER - game_height_10, game_height_10);
    this.scorePlayer2 = new Score(X_CENTER + game_height_10, game_height_10);

    this.ball = new Ball(this);
    this.ball.respawn();

    // add objects to update circle
    this.add_object(this.player1);
    this.add_object(this.player2);
    this.add_object(this.scorePlayer1);
    this.add_object(this.scorePlayer2);
    this.add_object(this.ball);

    this.init_bindings();
    this.next_frame();
  }

  next_frame() {
    if (!this.check_win()) {
      this.handle_input();
      this.update();
      this.render();

      window.requestAnimationFrame(this.next_frame.bind(this));
    }
  }

  check_win() {
    if (this.scorePlayer1.getScore() >= POINTS_TO_WIN) {
      this.win('Player 1');
      return true;
    } else if (this.scorePlayer2.getScore() >= POINTS_TO_WIN) {
      this.win('Player 2');
      return true;
    }
    return false;
  }

  handle_input() {
    for (const obj of this.objects) {
      obj.handle_input();
    }
  }

  update() {
    for (const obj of this.objects) {
      obj.update();
    }
  }

  render() {
    // render bg
    this.ctx.fillStyle = COL_SECONDARY;
    this.ctx.beginPath();
    this.ctx.rect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fill();

    // render line
    this.ctx.beginPath();
    this.ctx.moveTo(X_CENTER, 0);
    this.ctx.lineTo(X_CENTER, HEIGHT);
    this.ctx.stroke();

    // render objects
    this.ctx.fillStyle = COL_PRIMARY;
    this.ctx.beginPath();
    for (const obj of this.objects) {
      obj.render(this.ctx);
    }
    this.ctx.fill();
  }

  win(msg: string) {
    this.ctx.fillText(msg + ' wins', X_CENTER, Y_CENTER);
  }

  add_object(obj: IGameObject) {
    if (this.objects.indexOf(obj) < 0) {
      this.objects.push(obj);
    }
  }
  init_bindings() {
    this.keys = {};
    document.addEventListener('keydown', this.keyDown.bind(this));
    document.addEventListener('keyup', this.keyUp.bind(this));
  }

  keyDown(event: any) {
    this.keys[event.key] = true;
  }

  keyUp(event: any) {
    this.keys[event.key] = false;
  }

  is_pressed(key: string) {
    return this.keys[key];
  }
}
