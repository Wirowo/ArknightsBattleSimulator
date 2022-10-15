from flask import request


def batchSetCharVoiceLan():

    data = request.data
    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def getUnconfirmedOrderIdList():

    data = request.data
    data = {
        "orderIdList": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

    return data


def checkIn():

    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def changeSecretary():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "status":{
                    "secretary":"",
                    "secretarySkinId":"",
                }
            },
            "deleted":{}
        }
    }

    if charInstId and skinId:
        data["playerDataDelta"]["modified"]["status"]["secretary"] = skinId.split("@")[0] if "@" in skinId else skinId.split("#")[0]
        data["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = skinId
        return data

