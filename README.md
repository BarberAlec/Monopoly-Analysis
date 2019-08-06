# Monopoly-Analysis
Monopoly is a game of skill and luck where the player must attempt to buy property and dominate the market (creating a monopoly). This repository looks at some of the aspects the should be considered when deciding what property to buy,the expected number of lands per turn per tile, the exected income of a tile etc.

## Building a Simulator
Initially a Monopoly enviroment was created based on the London edition of the game. The game contains 16 chance and 16 community cards. As of 6/Aug/2019 a simplifed version has been implemented that includes all mechanics except money and property/rent. This version was used to build a model of chance of landing on any tile.

## Results

### Statistical Distribution of Landing on any tile on any Random Turn

![Simulation with error bars with 500,000 games and 100 turns per game](https://github.com/BarberAlec/Monopoly-Analysis/blob/master/Monopoly_500_000_Games_100_turns.png)

Initial Experiment which tested the simulator over 500,000 games, each lasting 100 turns. A statistical model is shown with error bars showing the probability of landing on any one tile on any random turn.
