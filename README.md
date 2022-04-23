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

## TODO

- [ ] Add a UI for easy editing
