import json
from time import time

import requests
from flask import request


def accountLogin():

    data = request.data

    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    playerData = requests.post('https://gs.arknights.global:8443/account/login',
        headers=headers,
        json=request.json
    ).json()

    secret = playerData["secret"]
    uid = playerData["uid"]

    data = {
        "result": 0,
        "uid": "-1",
        "secret": "yostar",
        "serviceLicenseVersion": 0
    }

    with open("data\\auth.json", 'w') as f:
        json.dump({"secret": secret, "uid": uid}, f, indent=4)

    return data


def syncData():

    data = request.data
    with open("data\\auth.json") as f:
        user_data = json.load(f)

    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    headers["uid"] = user_data["uid"]
    headers["secret"] = user_data["secret"]
    playerData = requests.post('https://gs.arknights.global:8443/account/syncData',
        headers=headers,
        json=request.json
    ).json()

    dataSkin = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/skin_table.json').json()
    character_table = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json').json()
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

    with open("config\\charEdit.json") as f:
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

        maxEvolvePhase = len(character_table[i]["phases"]) - 1
        evolvePhase = maxEvolvePhase

        if edit_json["evolvePhase"] != -1:
            if edit_json["evolvePhase"] > maxEvolvePhase:
                evolvePhase = maxEvolvePhase
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
        if operatorKeys[cnt] not in ["char_508_aguard", "char_509_acast", "char_510_amedic", "char_511_asnipe"]:
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

    with open("data\\userData.json", "w") as f:
        json.dump(playerData, f, indent=4)
    
    return playerData


def syncStatus():
    
    data = request.data
    data = {
        "ts": round(time()),
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data

