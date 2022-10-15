import json
from time import time

from flask import request

def getAssistList():

    data = request.data
    with open("config\\assistChar.json") as f:
        assistList = json.load(f)

    data = {
        "allowAskTs": int(time()),
        "assistList": [
            {
                "uid": "88888888",
                "aliasName": "",
                "nickName": "Yostar",
                "nickNumber": "8888",
                "level": 200,
                "avatarId": "0",
                "avatar": {
                    "type": "ASSISTANT",
                    "id": "char_421_crow#1"
                },
                "lastOnlineTime": int(time()),
                "assistCharList": [
                    assistList
                ],
                "powerScore": 500,
                "isFriend": True,
                "canRequestFriend": False,
                "assistSlotIndex": 0
            }
        ],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data
