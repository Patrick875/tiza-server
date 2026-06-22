from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4
from enum import Enum

class MediaType(Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    AUDIO = "AUDIO"

class Media(BaseModel):
    __tablename__='media'

    name = db.Column(db.String(255))
    src = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(255))

    mime_type = db.Column(db.String(100))
    size = db.Column(db.Integer)
    
    duration=db.Column(db.Integer)
    thumbnail= db.Column(db.String(500))

    type = db.Column(db.String(50), default=MediaType.IMAGE.value)
    storage_provider = db.Column(db.String(50), default="LOCAL")

    owner_type = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)

    purpose = db.Column(db.String(50), nullable=False)

    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id":str(self.uuid),
            "name":self.name,
            "src":self.src,
            "alt_text":self.alt_text,
            "mime_type":self.mime_type,
            "size":self.size,
            "duration":self.duration,
            "thumbnail":self.thumbnail,
            "type":self.type,
            "storage_provider":self.storage_provider,
            "owner_type":self.owner_type,
            "owner_id":self.owner_id,
            "purpose":self.purpose,
            "is_primary":self.is_primary,
            "sort_order":self.sort_order,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }