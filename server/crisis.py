import json
from time import time

from flask import request


def getCrisisInfo():

    data = request.data
    with open("data\\rune.json") as f:
        rune = json.load(f)

    current_time = round(time())
    next_day = round(time()) + 86400

    rune["ts"] = current_time
    # rune["playerDataDelta"]["modified"]["crisis"]["lst"] = current_time
    # rune["playerDataDelta"]["modified"]["crisis"]["nst"] = next_day
    # rune["playerDataDelta"]["modified"]["crisis"]["training"]["nst"] = next_day

    return rune
