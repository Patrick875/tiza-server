from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4



class Category(BaseModel):
    __tablename__='categories'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    name=db.Column(db.String(255),nullable=False,unique=True)
    description=db.Column(db.String())

    #relations
    listings=db.relationship(
        'Listing',
        back_populates='category'
    )

    def to_dict(self):
        return {
            "id":str(self.uuid),
            "name":self.name,
            "description":self.description,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }
