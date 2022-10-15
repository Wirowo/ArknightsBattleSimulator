import json
from time import time
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)
port = 8443
secret = ""
uid = 0

@app.route('/account/login', methods=['POST'])
def account_login():
    global secret, uid
    data = request.data
    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    playerData = requests.post('https://gs.arknights.global:8443/account/login',
        headers=headers,
        json=request.json
    ).json()
    secret = playerData["secret"]
    uid = playerData["uid"]

    return {
        "result": 0,
        "uid": "-1",
        "secret": "yostar",
        "serviceLicenseVersion": 0
    }

@app.route('/charBuild/batchSetCharVoiceLan', methods=['POST'])
def batchSetCharVoiceLan():
    data = request.data
    status = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return status


@app.route('/account/syncStatus', methods=['POST'])
def syncStatus():
    data = request.data
    status = {
        "ts": round(time()),
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return status


@app.route('/crisis/getInfo', methods=['POST'])
def getTestInfo():
    data = request.data
    with open("rune.json") as f:
        rune = json.load(f)

    current_time = round(time())
    next_day = round(time()) + 86400

    rune["ts"] = current_time
    # rune["playerDataDelta"]["modified"]["crisis"]["lst"] = current_time
    # rune["playerDataDelta"]["modified"]["crisis"]["nst"] = next_day
    # rune["playerDataDelta"]["modified"]["crisis"]["training"]["nst"] = next_day

    return rune


@app.route('/account/syncData', methods=['POST'])
def syncData():
    global secret, uid
    data = request.data
    writeLog("Modifying Operators and Skins...")

    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    headers["uid"] = uid
    headers["secret"] = secret
    playerData = requests.post('https://gs.arknights.global:8443/account/syncData',
        headers=headers,
        json=request.json
    ).json()

    dataSkin = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/skin_table.json').json()
    character_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json').json()
    patch_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/char_patch_table.json').json()["patchChars"]
    equip_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/uniequip_table.json').json()
    equip_keys = list(equip_table["charEquip"].keys())

    cnt = 0
    cntInstId = 1
    tempSkinTable = {}
    myCharList = {}

    #Tamper Skins
    skinKeys = list(dataSkin["charSkins"].keys())
    playerData["user"]["skin"]["characterSkins"] = {}
    for i in dataSkin["charSkins"]:
        if "@" not in skinKeys[cnt]:
            # Not Special Skins
            cnt += 1
            continue
        
        playerData["user"]["skin"]["characterSkins"][skinKeys[cnt]] = 1
        tempSkinTable[dataSkin["charSkins"][i]["charId"]] = dataSkin["charSkins"][i]["skinId"]
        cnt += 1
        
    #Tamper Operators

    with open("edit.json") as f:
        edit_json = json.load(f)

    cnt = 0

    operatorKeys = list(character_table.keys())
    for i in character_table:
        if "char" not in operatorKeys[cnt]:
            cnt += 1
            continue

        # Add all operators
        if edit_json["level"] == -1:
            level = character_table[i]["phases"][edit_json["evolvePhase"]]["maxLevel"]
        else:
            level = edit_json["level"]

        if edit_json["evolvePhase"] == -1:
            evolvePhase = len(character_table[i]["phases"]) - 1
        else:
            evolvePhase = edit_json["evolvePhase"]

        myCharList[int(cntInstId)] = {
            "instId": int(cntInstId),
            "charId": operatorKeys[cnt],
            "favorPoint": edit_json["favorPoint"],
            "potentialRank": edit_json["potentialRank"],
            "mainSkillLvl": edit_json["mainSkillLvl"],
            "skin": str(operatorKeys[cnt]) + "#1",
            "level": level,
            "exp": 0,
            "evolvePhase": evolvePhase,
            "defaultSkillIndex": 0,
            "gainTime": int(time()),
            "skills": [],
            "voiceLan": "JP",
            "currentEquip": None,
            "equip": {}
        }

        # set to E2 art if available
        if myCharList[int(cntInstId)]["evolvePhase"] == 2:
            myCharList[int(cntInstId)]["skin"] = str(operatorKeys[cnt]) + "#2"

        # set to seasonal skins [lastest release]
        if operatorKeys[cnt] in tempSkinTable.keys():
            myCharList[int(cntInstId)]["skin"] = tempSkinTable[operatorKeys[cnt]]

        # Add Skills
        for index, skill in enumerate(character_table[i]["skills"]):
            myCharList[int(cntInstId)]["skills"].append({
                "skillId": skill["skillId"],
                "unlock": 1,
                "state": 0,
                "specializeLevel": 0,
                "completeUpgradeTime": -1
            })

            # M3
            if len(skill["levelUpCostCond"]) > 0:
                myCharList[int(cntInstId)]["skills"][index]["specializeLevel"] = edit_json["skillsSpecializeLevel"]

        # Add equips
        if myCharList[int(cntInstId)]["charId"] in equip_keys:

            for equip in equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]]:
                myCharList[int(cntInstId)]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": 1
                    }
                })

            myCharList[int(cntInstId)]["currentEquip"] = equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]][-1]

        # Dexnav
        playerData["user"]["dexNav"]["character"][operatorKeys[cnt]] = {
            "charInstId": cntInstId,
            "count": 6
        }

        editList = edit_json["customUnitInfo"]

        for char in editList:
            if operatorKeys[cnt] == char:
                for key in editList[char]:
                    if key != "skills":
                        myCharList[int(cntInstId)][key] = editList[char][key]
                    else:
                        for skillIndex, skillValue in enumerate(editList[char]["skills"]):
                            myCharList[int(cntInstId)]["skills"][skillIndex]["specializeLevel"] = skillValue

        cnt += 1
        cntInstId += 1

    cnt = 0
    patchOperatorKeys = list(patch_table.keys())
    for i in patch_table:
        if "char" not in patchOperatorKeys[cnt]:
            cnt += 1
            continue

        # Add all operators
        if edit_json["level"] == -1:
            level = patch_table[i]["phases"][edit_json["evolvePhase"]]["maxLevel"]
        else:
            level = edit_json["level"]

        if edit_json["evolvePhase"] == -1:
            evolvePhase = len(patch_table[i]["phases"]) - 1
        else:
            evolvePhase = edit_json["evolvePhase"]

        myCharList[int(cntInstId)] = {
            "instId": int(cntInstId),
            "charId": patchOperatorKeys[cnt],
            "favorPoint": edit_json["favorPoint"],
            "potentialRank": edit_json["potentialRank"],
            "mainSkillLvl": edit_json["mainSkillLvl"],
            "skin": str(patchOperatorKeys[cnt]) + "#1",
            "level": level,
            "exp": 0,
            "evolvePhase": evolvePhase,
            "defaultSkillIndex": 0,
            "gainTime": int(time()),
            "skills": [],
            "voiceLan": "JP",
            "currentEquip": None,
            "equip": {}
        }

        # set to E2 art if available
        if myCharList[int(cntInstId)]["evolvePhase"] == 2:
            myCharList[int(cntInstId)]["skin"] = str(patchOperatorKeys[cnt]) + "#2"

        # set to seasonal skins [lastest release]
        if patchOperatorKeys[cnt] in tempSkinTable.keys():
            myCharList[int(cntInstId)]["skin"] = tempSkinTable[patchOperatorKeys[cnt]]

        # Add Skills
        for index, skill in enumerate(patch_table[i]["skills"]):
            myCharList[int(cntInstId)]["skills"].append({
                "skillId": skill["skillId"],
                "unlock": 1,
                "state": 0,
                "specializeLevel": 0,
                "completeUpgradeTime": -1
            })

            # M3
            if len(skill["levelUpCostCond"]) > 0:
                myCharList[int(cntInstId)]["skills"][index]["specializeLevel"] = edit_json["skillsSpecializeLevel"]

        # Add equips
        if myCharList[int(cntInstId)]["charId"] in equip_keys:

            for equip in equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]]:
                myCharList[int(cntInstId)]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": 1
                    }
                })

            myCharList[int(cntInstId)]["currentEquip"] = equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]][-1]

        # Dexnav
        playerData["user"]["dexNav"]["character"][patchOperatorKeys[cnt]] = {
            "charInstId": cntInstId,
            "count": 6
        }

        editList = edit_json["customUnitInfo"]

        for char in editList:
            if patchOperatorKeys[cnt] == char:
                for key in editList[char]:
                    if key != "skills":
                        myCharList[int(cntInstId)][key] = editList[char][key]
                    else:
                        for skillIndex, skillValue in enumerate(editList[char]["skills"]):
                            myCharList[int(cntInstId)]["skills"][skillIndex]["specializeLevel"] = skillValue

        cnt += 1
        cntInstId += 1


    playerData["user"]["troop"]["chars"] = myCharList
    playerData["user"]["troop"]["curCharInstId"] = cntInstId

    # Tamper story
    myStoryList = {"init": 1}
    story_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/story_table.json').json()
    for story in story_table:
        myStoryList.update({story:1})

    playerData["user"]["status"]["flags"] = myStoryList

    # Tamper Stages
    myStageList = {}
    stage_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/stage_table.json').json()
    for stage in stage_table["stages"]:
        myStageList.update({
            stage: {
                "completeTimes": 1,
                "hasBattleReplay": 0,
                "noCostCnt": 0,
                "practiceTimes": 0,
                "stageId": stage_table["stages"][stage]["stageId"],
                "startTimes": 1,
                "state": 3
            }
        })
    
    playerData["user"]["dungeon"]["stages"] = myStageList

    # Tamper Side Stories and Intermezzis
    for side in playerData["user"]["retro"]["block"]:
        playerData["user"]["retro"]["block"][side]["locked"] = 0

    # Tamper Anniliations
    playerData["user"]["campaignsV2"]["open"]["permanent"] = []
    playerData["user"]["campaignsV2"]["open"]["training"] = []
    for stage in stage_table["stages"]:
        if stage.startswith("camp"):
            playerData["user"]["campaignsV2"]["open"]["permanent"].append(stage)
            playerData["user"]["campaignsV2"]["open"]["training"].append(stage)

    writeLog("Done")

    ts = round(time())

    playerData["user"]["status"]["lastRefreshTs"] = ts
    playerData["user"]["status"]["lastApAddTime"] = ts
    playerData["user"]["status"]["registerTs"] = ts
    playerData["user"]["status"]["lastOnlineTs"] = ts
    playerData["ts"] = ts

    playerData["user"]["status"]["ap"] = 5000
    playerData["user"]["status"]["diamondShard"] = 5000
    playerData["user"]["status"]["payDiamond"] = 500
    playerData["user"]["status"]["nickName"] = "Yostar"
    playerData["user"]["status"]["nickNumber"] = 1111
    playerData["user"]["status"]["level"] = 200
    playerData["user"]["status"]["exp"] = 0
    playerData["user"]["status"]["resume"] = "What you doing"
    # playerData["user"]["status"]["secretary"] = "char_113_cqbw"
    # playerData["user"]["status"]["secretarySkinId"] = "char_113_cqbw#2"
    playerData["user"]["status"]["uid"] = "123456789"

    playerData["user"]["checkIn"]["canCheckIn"] = 0
    
    return playerData


@app.route('/pay/getUnconfirmedOrderIdList', methods=['POST'])
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


@app.route('/charBuild/setDefaultSkill', methods=['POST'])
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


@app.route('/charBuild/changeCharSkin', methods=['POST'])
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


@app.route('/quest/squadFormation', methods=['POST'])
def squadFormation():
    data = request.data
    request_data = request.get_json()
    squadId = request_data["squadId"]
    slots = request_data["slots"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "squads":{}
                }
            },
            "deleted":{}
        }
    }

    if squadId and slots:
        data["playerDataDelta"]["modified"]["troop"]["squads"].update({
            str(squadId): {
                "slots": slots
            }
        })
        return data


@app.route('/user/changeSecretary', methods=['POST'])
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


@app.route('/quest/battleStart', methods=['POST'])
def battleStart():
    data = request.data
    training = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    return training


@app.route('/quest/battleFinish', methods=['POST'])
def battleFinish():
    data = request.data
    data = {
        "result":0,
        "playerDataDelta": {
            "modified": {
                "mission": {
                    "missions": {
                        "GUIDE": {
                            "guide_8": {
                                "progress": [{
                                    "target": 1,
                                    "value": 1
                                    }]
                                }
                            }
                        }
                    }
                },
            "deleted": {}
        }
    }

    return data


@app.route('/quest/saveBattleReplay', methods=['POST'])
def saveBattleReplay():
    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


@app.route('/campaignV2/battleStart', methods=['POST'])
def anniBattleStart():
    data = request.data
    training = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    return training


@app.route('/campaignV2/battleFinish', methods=['POST'])
def anniBattleFinish():
    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


@app.route('/quest/getAssistList', methods=['POST'])
def getAssistList():
    data = request.data
    with open("edit.json") as f:
        assistList = json.load(f)

    data = {
        "allowAskTs": int(time()),
        "assistList": [
            {
                "uid": "88888888",
                "aliasName": "",
                "nickName": "Yostar",
                "nickNumber": "8888",
                "level": 110,
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


@app.route('/user/checkIn', methods=['POST'])
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


@app.route('/building/sync', methods=['POST'])
def building_sync():
    data = request.data
    data = {
        "ts": round(time()),
        "playerDataDelta": {
            "modified": {
                "building": {},
                "event": {
                    "building": round(time()) + 3000
                }
            },
            "deleted": {}
        }
    }
    return data



def writeLog(data):
    print(f'[{datetime.utcnow()}] {data}')

if __name__ == "__main__":
    writeLog('[SERVER] Server started at port ' + str(port))
    app.run(port=port)