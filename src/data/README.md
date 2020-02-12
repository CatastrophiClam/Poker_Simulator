## Description
- Data service for entire poker simulator

## Requirements
- Hook into game to record stats

### Be able to display:

#### Hand Win Stats
- Preflop hands and their win percentage if played till each street
- Win percentage of each AI, as fraction of total hands received and also as total hands played
- Preflop hands and their actual win percentage as grouped by each AI
- Win percentage of each AI

#### Money Win Stats
- Money won of each AI
- Groupings of hands and the money they win, sorted, can do different groupings, can also separate by AI

#### Action Stats
- Bet, raise, 3-bet, reraise percentages


## Notable Statistics
- Voluntarily put money in pot (VPIP)% of all hands - how loose-tight player is
- Preflop raise (PFR) % of all hands
- PFR/VPIP - overall how tight-aggresive
- 3 Bet PF % of all hands
	- May want more granularity for 3 Bet PFing after calling, checking or raising
- Won when saw flop (WWSF) - concerns tight-loose dimension
- Aggression Factor (AF) - (Bets + raises)/calls
- Aggression percentage (AF%) of betting rounds where player bets/raises
- Flop C-bet (CBetF) - aggressiveness
- Turn C-bet (CBetT) - preflop aggressor, bets flop and turn
- Check-Raise (CR)
- Cold call preflop (CCPF) - Bad cuz should mostly be reraising or folding to raises
- 3 bet, 4 bet
- PFR_Button, PFR_UTG, VPIP_Button, VPIP_UTG - measures player's use of position