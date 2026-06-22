from listings.models import Listing,ListingCondition
from categories.models import Category
from prices.models import Price
from users.models import User
from profiles.models import Profile
from sqlalchemy import and_,or_
from media.models import Media
from extensions import db


def apply_filter_and_search(query,filters:dict):
    search = filters.get("query", "").strip()
    categories = filters.get("categories")
    min_price = filters.get("min_price")
    max_price = filters.get("max_price")
    lease_type = filters.get("lease_type")
    location = filters.get("location")
    rating = filters.get("rating")
    security_deposit = filters.get("security_deposit")
    delivery_available = filters.get("delivery_available")
    delivery_fee = filters.get("delivery_fee")
    condition = filters.get("condition")
    listing_verification = filters.get("listing_verification")

    if categories:
        category_uuids = categories.split(",")
        query = query.join(Listing.category).filter(Category.uuid.in_(category_uuids))

    if lease_type:
        lease_types = lease_type.split(",")
        query = query.filter(Listing.primary_lease_type.in_(lease_types))

    if min_price:
        query = query.join(Listing.prices).filter(
            Price.lease_type == Listing.primary_lease_type,
            Price.amount >= float(min_price)
        )

    if max_price:
        query = query.join(Listing.prices).filter(
            Price.lease_type == Listing.primary_lease_type,
            Price.amount <= float(max_price)
        )

    if location:
        query = (
            query.join(Listing.lessor)
            .join(User.profile)
            .filter(Profile.location.ilike(f"%{location}%"))
        )

    if rating:
        query = query.filter(Listing.rating >= float(rating))

    if security_deposit:
        query = query.filter(Listing.security_deposit <= float(security_deposit))

    if delivery_available is not None:
        query = query.filter(Listing.delivery_available == (delivery_available == "true"))

    if delivery_fee:
        query = query.filter(Listing.delivery_fee <= float(delivery_fee))

    if condition:
        conditions = condition.split(",")
        query = query.filter(Listing.condition.in_(conditions))

    if listing_verification:
        query = query.filter(Listing.listing_verification == listing_verification)

    if search:
        query = query.join(Listing.category).filter(
            or_(
                Listing.name.ilike(f"%{search}%"),
                Category.name.ilike(f"%{search}%")
            )
        )

    return query

def apply_sort(query, filters: dict):
    sort = filters.get("sort", "created_at,desc")

    try:
        sort_field, sort_direction = [s.strip() for s in sort.split(",")]
    except ValueError:
        sort_field, sort_direction = "created_at", "desc"

    sort_columns = {
        "created_at": Listing.created_at,
        "updated_at": Listing.updated_at,
        "name": Listing.name,
        "rating": Listing.rating,
        "security_deposit": Listing.security_deposit,
        "delivery_fee": Listing.delivery_fee,
    }

    column = sort_columns.get(sort_field, Listing.created_at)

    return query.order_by(
        column.asc() if sort_direction == "asc" else column.desc()
    )


def attach_thumbnails(listings):
    listing_ids = [listing.id for listing in listings]

    thumbnails = Media.query.filter(
        Media.owner_type == "LISTING",
        Media.owner_id.in_(listing_ids),
        Media.purpose == "THUMBNAIL"
    ).all()

    thumbnail_map = {
        thumbnail.owner_id: thumbnail
        for thumbnail in thumbnails
    }

    data = []

    for listing in listings:
        item = listing.to_list_item()
        thumbnail = thumbnail_map.get(listing.id)

        item["thumbnail"] = {
            "id": str(thumbnail.uuid),
            "name": thumbnail.name,
            "src": thumbnail.src,
            "alt_text": thumbnail.alt_text,
            "mime_type": thumbnail.mime_type,
            "type": thumbnail.type,
        } if thumbnail else None

        data.append(item)

    return data

def paginate_listings(query, filters: dict):
    page = int(filters.get("page", 1))
    per_page = int(filters.get("per_page", 10))

    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "items": attach_thumbnails(paginated.items),
        "pagination": {
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        }
    }

def build_listing_query(filters: dict, include_deleted=False, lessor_id=None):
    query = Listing.query

    if not include_deleted:
        query = query.filter(Listing.status != "DELETED")

    if lessor_id:
        query = query.filter(Listing.lessor_id == lessor_id)

    query = apply_filter_and_search(query, filters)
    query = apply_sort(query, filters)

    return query

def fetch_all_public(filters: dict):
    query = build_listing_query(
        filters=filters,
        include_deleted=False
    )

    return paginate_listings(query, filters)
def fetch_all_per_category(filters: dict,category_id:str):
    filters["categories"]=[category_id]
    query = build_listing_query(
        filters=filters,
        include_deleted=False
    )

    return paginate_listings(query, filters)


def fetch_all_for_user(filters: dict, user_id: int, roles: list[str]):
    if "ADMIN" in roles:
        query = build_listing_query(
            filters=filters,
            include_deleted=True
        )

    elif "LESSOR" in roles:
        query = build_listing_query(
            filters=filters,
            include_deleted=True,
            lessor_id=user_id
        )

    else:
        raise ValueError("You are not allowed to view these listings")

    return paginate_listings(query, filters)


def fetch_by_id(listing_id):
    listing = Listing.query.filter_by(uuid=listing_id).first_or_404()

    if not listing or listing.status=='DELETED':
        raise ValueError("Listing not found")

    media = Media.query.filter(
        Media.owner_type == "LISTING",
        Media.owner_id == listing.id
    ).order_by(Media.sort_order.asc()).all()

    thumbnail = next(
        (
            item for item in media
            if item.purpose == "THUMBNAIL"
        ),
        None
    )

    gallery = [
        {
            "id": str(item.uuid),
            "name": item.name,
            "src": item.src,
            "alt_text": item.alt_text,
            "mime_type": item.mime_type,
            "size": item.size,
            "duration": item.duration,
            "thumbnail": item.thumbnail,
            "type": item.type,
            "purpose": item.purpose,
            "is_primary": item.is_primary,
            "sort_order": item.sort_order,
        }
        for item in media
        if item.purpose == "GALLERY"
    ]

    data = listing.to_dict()

    data["thumbnail"] = {
        "id": str(thumbnail.uuid),
        "name": thumbnail.name,
        "src": thumbnail.src,
        "alt_text": thumbnail.alt_text,
        "mime_type": thumbnail.mime_type,
        "size": thumbnail.size,
        "type": thumbnail.type,
    } if thumbnail else None

    data["media"] = gallery

    return data


def create_listing(data:dict):
    category_id = data.pop("category_id", None)
    lessor_id = data.pop("lessor_id", None)
    prices_data = data.pop("prices", [])
    thumbnail_data = data.pop("display_image", None)
    media_data = data.pop("media", [])
    category=Category.query.filter_by(id=category_id).first()
    
    if not category_id or not category:
        raise ValueError("Item category not found")
    if not lessor_id or not User.query.filter_by(id=lessor_id).first():
        raise ValueError("Owner not found")

    listing=Listing(
        **data,
        lessor_id=lessor_id,
        category_id=category.id
        )
    db.session.add(listing)
    db.session.flush()

    for item in prices_data:
       db.session.add(Price(
            status=item.get("status" ,"ACTIVE"),
            amount=item.get("amount"),
            lease_type=item.get("lease_type"),
            lease_duration=item.get("lease_duration"),
            listing_id=listing.id
        )
       )
    
    if thumbnail_data:
        db.session.add(Media(
            **thumbnail_data,
            owner_type="LISTING",
            owner_id=listing.id,
            purpose="THUMBNAIL",
            is_primary=True,
            sort_order=0
        ))

    for index, item in enumerate(media_data):
        db.session.add(Media(
            **item,
            owner_type="LISTING",
            owner_id=listing.id,
            purpose="GALLERY",
            is_primary=False,
            sort_order=index + 1
        ))
    db.session.commit()
    return listing.to_dict()

def update_listing(id:str,data:dict):
    listing=Listing.query.filter_by(uuid=id).first()

    if not listing or listing.status=='DELETED' :
        raise ValueError('Listing not found')

    LISTING_UPDATE_FIELDS = [
        "name",
        "description",
        "category_id",
        "condition",
        "tags",
        "included_items",
        "leasing_types",
        "primary_lease_type",
        "security_deposit",
        "delivery_available",
        "delivery_fee",
        "available_from",
        "available_to",
    ]
    

    for key, value in data.items():
        if key in LISTING_UPDATE_FIELDS:
                setattr(listing, key, value)  
    
    prices_data=data.get('prices',[])
    price_update_fields=['amount','lease_type','lease_duration','status']

    for price_data in prices_data:
        price_id=price_data.get("id")
        if price_id:
            price=Price.query.filter_by(uuid=price_id).first()
            if not price:
                raise ValueError(f"Price with id {price_id} not found for this listing")
            
            for key,value in price_data.items():
                if key in price_update_fields:
                    setattr(price,key,value)
        else:
            new_price=Price(
                lease_duration=price_data.get("lease_duration"),
                lease_type=price_data.get("lease_type"),
                status=price_data.get("status"),
                amount=price_data.get("amount"),
                listing_id=listing.id
            )
            db.session.add(new_price)
    
    
    db.session.commit()

    return listing.to_dict()


def delete_listing(id:str,user_id:int,is_admin:bool):
    listing= Listing.query.filter_by(uuid=id).first()
    if not is_admin or user_id!=listing.lessor_id:
        raise ValueError("Unauthorized, you can not delete this listing")
    if not listing or listing.status=='DELETED':
        raise ValueError("Listing not found")
    listing.status='DELETED'
    db.session.commit()
    return listing