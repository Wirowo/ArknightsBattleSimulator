from flask import request

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

