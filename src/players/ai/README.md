## Description
- Collection of AIs for plugging into poker simulator

Must be able to simulate any kind of strategy

Need way to rank how good a hand is
	This could change depending on the player

Need an absolute rating of a hand

Need way to keep a player at a certain amount of money no matter if they win or lose money

What information encompasses all there is to know about a player?/Player metrics:

## Concepts
### Folding
- Fold freq is bet/(pot + bet)
### Checking
### Betting
### Raising
### Reraising
### Bluffing
- Bluff freq is bet / (bet + call + pot)
- Semi bluffs like draws, stuff with outs
- Take into account showdown value
### Overbetting
- Don't block hands you want to call you when value overbluffing
- When bluffing you want to block stronger hands
### Multi way pots
- Bets more polarized, probs more strong
- Players more honest
- Try less to put people on specific ranges, more of own hand vs board and how good it is
- Focus hands that are easier to play multi way like suited connectors, 3's, etc
- The higher the limits, the less people play hands and vice versa
	- Take advantage of loose ranges, people calling too much
### Reading
- Factor in other people's stack size
### Metagame
- Use one player's tendencies to get another player out
	- Put pressure eg. bet, player with person going after them gets more pressure
### Mixed Strategy
- Do different things in the exact same spot
- Board coverage is good, increase it with hands that have postflop potential


## AI Levels By Skill
### Preflop

##### Levels of Checking
0) Check whenever possible
	
##### Levels of Betting:
0) No betting
1) Bet according to range
2) Bet according to range and position
3) Bet according to range, position and other player's tendencies
	
##### Levels of Bluffing:
0) No bluffs

##### Levels of Calling:
0) Call big blind no matter what, fold to any bet
1) Call only bets within own betting range
2) Have a dedicated calling range
3) Have a dedicated calling range influenced by position
4) Have a dedicated calling range influenced by position and other player's tendencies

##### Levels of Raising:
0) No raising
1) Raise or reraise when other player's bets are too low relative to own range's bet size
2) Raise/reraise based on read of other players, position
3) Raise/reraise base on other various factors

### Postflop

##### Levels of Checking:
0) Check everything

##### Levels of Betting:
0) No bets
	
##### Levels of Bluffing:
0) No bluffs

##### Levels of Calling:
0) Fold to any bet

##### Levels of Raising:
0) No raising

### Levels of Opponent Reading

### Levels of Game Theory

### Self Learning
- Find some way to represent causes, effects, actions, events and entities
- Find some way to let them change and be affected by existing characteristics

## AI Levels By AI
### Generation 0
- Bet according to hand
- No bluffs
- Fold according to other's bets
	- Calling range is betting range or somewhere around there

### Generation 1
- Bet according to hand
- Randomly bluff set percent of time
- Fold according to other's bets
	- Have a calling range for each hand