import os, json, datetime

def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "Oii da Carol :) estou testando Lambda com Python e CI/CD",
            "commit": os.getenv("GIT_SHA", "unknown"),
            "built_at": os.getenv("BUILT_AT", "unknown"),
        })
    }
