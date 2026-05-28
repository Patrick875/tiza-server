from flask import jsonify
from datetime import datetime, timezone

def api_response(
    success=True,
    message="",
    data=None,
    errors=None,
    status_code=200,
    meta_info={}
):
    response=jsonify({
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
        "timeStamp": datetime.now(timezone.utc).isoformat(),
        "meta_info":meta_info
    })

    response.status_code=status_code
    return response