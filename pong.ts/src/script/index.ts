import { LowIntelligenceAIBar } from './AiBar';
import { Game } from './Game';

(() => {
  const g = new Game(LowIntelligenceAIBar, LowIntelligenceAIBar, 'game-canvas');
  console.log(g.simulate(1000));
  g.run();
})();
