from flask import request


def getSkinGoodList():

    data = request.data
    data = {
        "goodList":[],
        "playerDataDelta":{
            "modified":{},
            "deleted":{}
        }
    }

    return data