from flask import Request
from sqlalchemy import or_
from sqlalchemy.orm.query import Query
from ..models.user import TUSER


def get_filters(request: Request) -> Query[TUSER]:
    search_param = request.args.get("search")

    if search_param:
        return TUSER.query.filter(
            or_(
                TUSER.first_name.ilike(f"%{search_param}%"),
                TUSER.first_surname.ilike(f"%{search_param}%"),
                TUSER.second_surname.ilike(f"%{search_param}%"),
                TUSER.email.ilike(f"%{search_param}%"),
            )
        )
    else:
        return TUSER.query
