import json
from generate_procedure import *


def lambda_handler(event, context):
    body = json.loads(event.get("body"))

    procedure = body.get("procedure")

    params = {
        "name": body.get("name"),
        "lastname": body.get("lastname"),
        "birthdate": body.get("birthdate")
    }

    generate_procedure(procedure, params)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "OK"
        }),
    }
