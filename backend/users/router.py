from sanic import Blueprint, HTTPResponse, response
from sanic.request import Request
from sanic_ext import openapi

from config import settings

from .schema import UserSchemaAdd
from .service import UsersService

router = Blueprint("Auth")


@router.post("/signin")
@openapi.definition(
    body={"application/json": UserSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")},
)
async def signin(request: Request, service: UsersService) -> HTTPResponse:
    """
    Get JWT token
    """
    user = await service.get_user(request.ctx.session, username=request.json.get("username"))
    if not user:
        user = await service.add_user(request.ctx.session, request.json)
    token = await service.auth_user(user)
    resp = response.json({"token": token})
    resp.add_cookie(key="jwt-token", value=token, max_age=60 * settings.TOKEN_EXPIRE_MINUTES, httponly=True)
    return resp
