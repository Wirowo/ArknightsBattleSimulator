import json
from time import time

from flask import request


def getCrisisInfo():

    data = request.data
    with open("config\\crisisConfig.json") as f:
        selected_crisis = json.load(f)["selectedCrisis"]

    with open(f"data\\crisis\\{selected_crisis}.json") as f:
        rune = json.load(f)

    current_time = round(time())
    next_day = round(time()) + 86400

    rune["ts"] = current_time
    rune["playerDataDelta"]["modified"]["crisis"]["lst"] = current_time
    rune["playerDataDelta"]["modified"]["crisis"]["nst"] = next_day
    rune["playerDataDelta"]["modified"]["crisis"]["training"]["nst"] = next_day

    return rune


def crisisBattleStart():

    data = request.data
    data = request.get_json()
    with open("config\\crisisConfig.json") as f:
        selected_crisis = json.load(f)["selectedCrisis"]

    with open(f"data\\crisis\\{selected_crisis}.json") as f:
        rune_data = json.load(f)["data"]["stageRune"][data["stageId"]]

    totalRisks = 0
    for each_rune in data["rune"]:
        totalRisks += rune_data[each_rune]["points"]

    with open("data\\rune.json", "w") as f:
        json.dump({
            "chosenCrisis": selected_crisis,
            "chosenRisks": data["rune"],
            "totalRisks": totalRisks
        }, f, indent=4)
    
    data = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0,
        'sign': "abcde",
        'signStr': "abcdefg"
    }

    return data


def crisisBattleFinish():

    with open("data\\rune.json") as f:
        totalRisks = json.load(f)["totalRisks"]

    data = request.data
    data = {
        "result": 0,
        "score": totalRisks,
        "updateInfo": {
            "point": {
                "before": -1,
                "after": totalRisks
            }
        },
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data

