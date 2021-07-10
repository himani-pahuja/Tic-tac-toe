# Tic-tac-toe
Generalized form(n\*n) of 3\*3 tic-tac-toe.  
  
**Min-Max algorithm** is a game playing technique turn-by-turn under which 1 ply is maximizing ply(i.e its the your turn therefore you choose the step which maximise your chance of winning or decreases opponents chances) and 1 or more minimizing ply(which are played by your opponent to benefit them or decreasing your chance of winning);used to find the best move at current position of game.  
And in this process of searching for the best move, sometimes we search in parts which will never result in the best move so to prune them we use alpha-beta pruning.  
