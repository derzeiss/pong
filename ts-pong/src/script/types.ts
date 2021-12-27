import { Bar } from "./Bar";
import { Game } from "./Game";

export interface IGameObject {
  handle_input: () => void;
  update: () => void;
  render: (ctx: CanvasRenderingContext2D) => void;
}

export type BarFactory = (game: Game, x: number, y: number) => Bar;
