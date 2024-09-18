from sanic import Blueprint, HTTPResponse, response
from sanic.request import Request
from sanic_ext import openapi

from .repository import UsersRepository
from .schema import UserSchemaAdd
from .service import UsersService
from .token_storage import TokenStorage


router = Blueprint("Auth")

service = UsersService(
    users_repo=UsersRepository,
    token_storage=TokenStorage,
)


@router.post("/signin")
@openapi.definition(
    body={"application/json": UserSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")},
)
async def signin(request: Request) -> HTTPResponse:
    """
    Get JWT token
    """
    user = await service.get_user(request.ctx.session, username=request.json.get("username"))
    if not user:
        user = await service.add_user(request.ctx.session, request.json)
    token = await service.auth_user(user)
    resp = response.json({"token": token})
    return resp
