from flask import jsonify
from datetime import datetime, timezone

def api_response(
    success=True,
    message="",
    data=None,
    errors=None,
    status_code=200
):
    response=jsonify({
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
        "timeStamp": datetime.now(timezone.utc).isoformat()
    })

    response.status_code=status_code
    return response