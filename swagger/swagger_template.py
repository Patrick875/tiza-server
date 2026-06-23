from swagger.definitions.categories import category_definition
from swagger.definitions.auth import auth_definitions
from swagger.definitions.profiles import profile_definitions

swagger_template={
    "swagger":"2.0",
    "info":{
        "title":"Tiza v1.0 API",
        "version":"1.0.0"
    },
    "securityDefinitions":{
        "Bearer":{
            "type":"apiKey",
            "name":"Authorization",
            "in":"header",
            "description":"JWT Authorization header. Example: Bearer eyJhbGciOiJIUzI1NiIs..."
        }
    },
    "definitions":{
        **category_definition,
        **auth_definitions,
        **profile_definitions
    }
}