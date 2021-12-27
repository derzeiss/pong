export const randint = (min: number, max: number = -1) => {
  if (max == -1) {
    max = min;
    min = 0;
  }
  return Math.floor(Math.random() * (max - min) + min);
};