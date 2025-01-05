from sanic import Blueprint, HTTPResponse, response
from sanic.request import Request
from sanic_ext import openapi, validate

from .schema import UserSchemaAdd
from .service import UsersService

router = Blueprint("Auth")


@router.post("/signin")
@openapi.definition(
    body={"application/json": UserSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")}
)
@validate(json=UserSchemaAdd)
async def signin(request: Request, service: UsersService, body: UserSchemaAdd) -> HTTPResponse:
    """
    Get JWT token
    """
    user = await service.get_user(request.ctx.session, username=body.username)
    if not user:
        user = await service.add_user(request.ctx.session, body)
    token = service.auth_user(user)
    return response.json({"token": token})
