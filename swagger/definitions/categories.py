category_definition = {
    "Category": {
        "type": "object",
        "properties": {
            "id": {"type": "uid", "example": "9e39c0f5-462e-49e2-bb8b-84496f77f274 "},
            "name": {"type": "string", "example": "Electronics"},
            "description": {
                "type": "string",
                "example": "Electronic products and accessories"
            },
            "created_at": {
                "type": "string",
                "format": "date-time",
                "example": "2026-06-16T10:30:00Z"
            },
            "updated_at": {
                "type": "string",
                "format": "date-time",
                "example": "2026-06-16T10:30:00Z"
            }
        }
    }
}