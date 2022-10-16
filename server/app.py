from datetime import datetime

from flask import Flask

import assist, auth, battle, building, campaignV2, char, crisis, is2, misc, shop, squad

app = Flask(__name__)
port = 8443

# Assist
app.add_url_rule('/quest/getAssistList', methods=['POST'], view_func=assist.getAssistList)

# Auth
app.add_url_rule('/account/login', methods=['POST'], view_func=auth.accountLogin)
app.add_url_rule('/account/syncData', methods=['POST'], view_func=auth.syncData)
app.add_url_rule('/account/syncStatus', methods=['POST'], view_func=auth.syncStatus)

# Battle
app.add_url_rule('/quest/battleStart', methods=['POST'], view_func=battle.battleStart)
app.add_url_rule('/quest/battleFinish', methods=['POST'], view_func=battle.battleFinish)
app.add_url_rule('/quest/saveBattleReplay', methods=['POST'], view_func=battle.saveBattleReplay)

# Building
app.add_url_rule('/building/sync', methods=['POST'], view_func=building.buildingSync)

# Annilation
app.add_url_rule('/campaignV2/battleStart', methods=['POST'], view_func=campaignV2.anniBattleStart)
app.add_url_rule('/campaignV2/battleFinish', methods=['POST'], view_func=campaignV2.anniBattleFinish)

# Char
app.add_url_rule('/charBuild/setDefaultSkill', methods=['POST'], view_func=char.setDefaultSkill)
app.add_url_rule('/charBuild/changeCharSkin', methods=['POST'], view_func=char.changeCharSkin)
app.add_url_rule('/charBuild/setEquipment', methods=['POST'], view_func=char.setEquipment)

# Crisis
app.add_url_rule('/crisis/getInfo', methods=['POST'], view_func=crisis.getCrisisInfo)

# IS2
app.add_url_rule('/rlv2/createGame', methods=['POST'], view_func=is2.createGame)
app.add_url_rule('/rlv2/chooseInitialRelic', methods=['POST'], view_func=is2.chooseInitialRelic)
app.add_url_rule('/rlv2/selectChoice', methods=['POST'], view_func=is2.selectChoice)
app.add_url_rule('/rlv2/chooseInitialRecruitSet', methods=['POST'], view_func=is2.chooseInitialRecruitSet)
app.add_url_rule('/rlv2/activeRecruitTicket', methods=['POST'], view_func=is2.activeRecruitTicket)
app.add_url_rule('/rlv2/recruitChar', methods=['POST'], view_func=is2.recruitChar)
app.add_url_rule('/rlv2/closeRecruitTicket', methods=['POST'], view_func=is2.closeRecruitTicket)
app.add_url_rule('/rlv2/finishEvent', methods=['POST'], view_func=is2.finishEvent)
app.add_url_rule('/rlv2/moveAndBattleStart', methods=['POST'], view_func=is2.moveAndBattleStart)


# Misc
app.add_url_rule('/charBuild/batchSetCharVoiceLan', methods=['POST'], view_func=misc.batchSetCharVoiceLan)
app.add_url_rule('/pay/getUnconfirmedOrderIdList', methods=['POST'], view_func=misc.getUnconfirmedOrderIdList)
app.add_url_rule('/user/checkIn', methods=['POST'], view_func=misc.checkIn)
app.add_url_rule('/user/changeSecretary', methods=['POST'], view_func=misc.changeSecretary)

# Shop
app.add_url_rule('/shop/getSkinGoodList', methods=['POST'], view_func=shop.getSkinGoodList)

# Squad
app.add_url_rule('/quest/squadFormation', methods=['POST'], view_func=squad.squadFormation)


def writeLog(data):
    print(f'[{datetime.utcnow()}] {data}')

if __name__ == "__main__":
    writeLog('[SERVER] Server started at port ' + str(port))
    app.run(port=port)
