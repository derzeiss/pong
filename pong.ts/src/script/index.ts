import { LowIntelligenceAIBar } from './AiBar';
import { Bar } from './Bar';
import { Game } from './Game';

(() => {
  const g = new Game('game-canvas', Bar, LowIntelligenceAIBar);
  g.run();
})();
