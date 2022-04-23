# Note before continuing 

### Although this probably violates the TOS of hypergryph, you can use this with a guest account so idk if that counts as risky or not
____________

# ArknightsBattleSimulator
Simulate Arknights stages without costing sanity (works with guest account)

## How To

1. Install [mitmproxy](https://mitmproxy.org/) and [python3](https://www.python.org/downloads/).
2. Configure your emulator to pass data through mitmproxy. [Link](https://docs.mitmproxy.org/stable/overview-getting-started/)
3. Clone the repo.
4. Run `start.bat` in the cloned folder.
5. Open Arknights.

Customize each operator indivually by adding new info in `edit.json`. You can find <operator_key_name> from [here](https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json). By default, all characters will have max level, max potentials, max mastery.

`potentialRank` - 0-5
`evolvePhase` - 0 - E0, 1 - E1, 2 - E2
`skills` - Mastery level for each skill starting from S1.

### Format
```
"<operator_key_name>": {
    "potentialRank": 2,
    "level": 50, 
    "evolvePhase": 1,
    "skills": [1, 0]
}
```
## What works in game
- Can play all main stories
- Can play all Side Stories and Intermezzis currently available in game
- Can play all anniliations
- Can play supplies stages that are opened on the particular day you are playing.
- Selecting skills when forming squads
- Editing squad formations

## What probably doesn't work in game
- Setting default operators skills
- Leveling up operators or skills
- Bringing support unit from friends
- Any base related stuffs
- Any profile related stuffs
- Any gacha related stuffs
- Any contengency contract related stuffs
- Any resource related stuffs (sanity, lmd, originium)
- Any store related stuffs

+Many other that i probably forgot to mention




## TODO

- [ ] Add a UI for easy editing
