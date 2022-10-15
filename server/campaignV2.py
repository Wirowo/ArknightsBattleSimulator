from flask import request


def anniBattleStart():

    data = request.data
    data = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    return data


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

