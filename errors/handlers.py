from werkzeug.exceptions import HTTPException
from utils.response import api_response
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return api_response(
            status_code=e.code,
            status=False,
            message=e.description,
            errors=[e.description]
        )
    

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return api_response(
            status_code=400,
            success=False,
            message="Validation error",
            errors=e.messages,
        )
    
    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return api_response(
            status_code=500,
            success=False,
            message="Internal server error",
            errors=[str(e)],
        )