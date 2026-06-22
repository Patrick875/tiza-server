from extensions import db
from categories.models import Category


def fetch_all():
    query= Category.query
    # categories=Category.query.all()
    paginated=query.paginate(
        page=1,
        per_page=10,
        error_out=False
    )
    data=[category.to_dict() for category in paginated.items] or []

    return {
        "items":data,
        "pagination":{
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        }
    }

def get_single(id:str):
    print('id',id)
    category=Category.query.filter_by(uuid=id).first()
    print(category)
    if not category:
        raise ValueError("Category not found")
    return category.to_dict()

def create(data:dict):
    name=data.get("name",None)
    
    exists=Category.query.filter_by(name=name).first()
    if exists is not None:
        raise ValueError("Category already exists")
    
    category=Category(**data)
    db.session.add(category)
    db.session.commit()
    return category.to_dict()

def update_cat(id:str,data:dict):
    name=data.get("name",None)
    description=data.get("description",None)
    category=Category.query.filter_by(uuid=id).one_or_none()
    if not category :
        raise ValueError("Category with id not found")
    if name is not None:
        category.name=name
    if description is not None:
        category.description= description
    db.session.commit()
    return category.to_dict()

def delete_cat(id:str):
    #uses hard delete
    category = Category.query.filter_by(uuid=id).first()

    if not category:
        raise ValueError("Category with id not found")
    
    db.session.delete(category)
    db.session.commit()
    return {"success":True}