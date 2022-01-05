import { Ball } from './Ball';
import { Bar } from './Bar';
import {
  BAR_HEIGHT,
  BAR_WIDTH, COL_PRIMARY, COL_SECONDARY, DEFAULT_FONT, HEIGHT, POINTS_TO_WIN, WIDTH, X_CENTER, Y_CENTER
} from './config';
import { Score } from './Score';
import { IGameObject } from './types';

export class Game {
  private keys!: { [key: string]: boolean };
  private objects!: IGameObject[];
  private player1Class: typeof Bar;
  private player2Class: typeof Bar;
  public player1!: Bar;
  public player2!: Bar;
  public scorePlayer1!: Score;
  public scorePlayer2!: Score;
  public ball!: Ball;
  private canvas!: HTMLCanvasElement;
  private ctx!: CanvasRenderingContext2D;

  constructor(player1Class: typeof Bar, player2Class: typeof Bar, canvasId: string = '') {
    if (canvasId) {
      this.initCanvas(canvasId);
    }

    // game objects
    this.player1Class = player1Class;
    this.player2Class = player2Class;
  }

  initCanvas(canvasId: string) {
    this.canvas = document.getElementById(canvasId) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d') as CanvasRenderingContext2D;
    this.canvas.width = WIDTH;
    this.canvas.height = HEIGHT;

    // set default params
    this.ctx.strokeStyle = COL_PRIMARY;
    this.ctx.lineWidth = 3;
    this.ctx.setLineDash([10, 3]);
    this.ctx.font = DEFAULT_FONT;
    this.ctx.textAlign = 'center';
  }

  init() {
    this.keys = {};
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

    // add objects to update cycle
    this.addObject(this.player1);
    this.addObject(this.player2);
    this.addObject(this.scorePlayer1);
    this.addObject(this.scorePlayer2);
    this.addObject(this.ball);
  }

  run() {
    this.init();
    this.initBindings();
    this.runNextFrame();
  }

  simulate(runs: number, debug = false) {
    const securityTimeout = 36000; // let a game run max 10 mins @ 60FPS
    const halftime = Math.round(runs / 2); // used to switch bar positions on half time
    const t0 = Date.now(); // save current time to determine how long the simulation took
    let victories = [0, 0, 0]; // draws, p1 wins, p2 wins

    // swap victory scores; used in halftime on bar-position-switch and at the end of the simulation
    const swapVictories = () => {
      const v1 = victories[1];
      victories[1] = victories[2];
      victories[2] = v1;
    };

    // run n games
    for (var i = 0; i < runs; i++) {
      let securityCounter = securityTimeout;
      let victoriousPlayer = 0;

      // switch bar positions on halftime
      if (i === halftime) {
        let c1 = this.player1Class;
        this.player1Class = this.player2Class;
        this.player2Class = c1;
        swapVictories();
      }

      // run all the standard init stuff to reset the game to a blank state
      this.init();

      // run one game until there's a winner or timeout ran off
      while (victoriousPlayer === 0 && securityCounter-- > 0) {
        this.handleInput();
        this.update();

        victoriousPlayer = this.checkWin(true);
      }

      if (debug) {
        console.log(
          `finished game ${i} in ${securityTimeout - securityCounter} frames (about ${Math.round(
            (securityTimeout - securityCounter) / 60
          )}s @ 60fps, ${Math.round((securityCounter * 100) / securityTimeout)}% of game time available)`
        );
      }
      // count victory (securityCounter exceeded = draw will increase index 0 by one)
      victories[victoriousPlayer]++;
    }

    // we swapped victories in halftime, now we need to swap it back
    swapVictories();
    console.log(`Simulation took ${Math.round(Date.now() - t0) / 1000}s.`);
    return victories;
  }

  runNextFrame() {
    if (!this.checkWin()) {
      this.handleInput();
      this.update();
      this.render();

      window.requestAnimationFrame(this.runNextFrame.bind(this));
    }
  }

  checkWin(isSimulation: boolean = false) {
    if (this.scorePlayer1.getScore() >= POINTS_TO_WIN) {
      if (!isSimulation) {
        this.win('Player 1');
      }
      return 1;
    } else if (this.scorePlayer2.getScore() >= POINTS_TO_WIN) {
      if (!isSimulation) {
        this.win('Player 2');
      }
      return 2;
    }
    return 0;
  }

  handleInput() {
    for (const obj of this.objects) {
      obj.handleInput();
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

    // render middle line
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

  addObject(obj: IGameObject) {
    if (this.objects.indexOf(obj) < 0) {
      this.objects.push(obj);
    }
  }
  initBindings() {
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
