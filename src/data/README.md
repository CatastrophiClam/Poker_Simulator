## Description
- Data service for entire poker simulator

## Requirements
- Hook into game to record stats
- Need dynamic way to choose what sort of data to record
- Store data into some sort of structure

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

## Design
- There will be 2 types of data we need to keep track of: accumulative data and non-accumulative data
- We will also need filters and categories for data

### Accumulative Data
- This is data that can't be aggregated - we have to store the whole thing every time
- Eg. Whole rounds of poker, the hands that a player plays, etc
- The amount of data will accumulate with the amount of rounds run, so keeping track of this data will
limit the amount of rounds we can run

### Non-Accumulative Data
- Data that can be aggregated
- Eg. Total winnings of a player, win percentages of hands
- This data does not increase with the amount of rounds run

### Data Stores
- We store all necessary data using data stores
- Each data store stores one particular metric we want to measure and provides methods to log and recall
those metrics
- This way we can easily and declaratively choose which metrics we want to keep track of each session

### Filters
We want a way to dynamically filter our data sets. At a high level,
every one of our data stores should be able to take in Filter objects. They should then store data in a way 
such that we can get accurate sets of data from different combinations of filters. Note that our accumulative 
data wouldn't be able to do combinations of filters though.

Each filter should take in a roundRecord and decide if it passes the filter or not. Its str method should
return a description of itself. The filters split our data records into segments. 

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