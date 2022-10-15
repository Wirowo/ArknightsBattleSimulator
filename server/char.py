import json

from flask import request


def setDefaultSkill():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    defaultSkillIndex = request_data["defaultSkillIndex"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                   "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and defaultSkillIndex:
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "defaultSkillIndex": defaultSkillIndex
            }
        })
        return data


def changeCharSkin():
    
    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and skinId:
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "skin": skinId
            }
        })
        return data


def setEquipment():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    equipId = request_data["equipId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and equipId:

        with open("data\\userData.json") as f:
            user_data = json.load(f)

        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "currentEquip": equipId
            }
        })

        user_data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "currentEquip": equipId
            }
        })

        with open("data\\userData.json", "w") as f:
            json.dump(user_data, f, indent=4)

        return data
