from sanic import Blueprint, HTTPResponse, response
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic_ext import openapi, validate

from backend.users.service import UsersService

from .schema import PasteSchemaAdd
from .service import PastesService

router = Blueprint("Pastes", url_prefix="/pastes")


@router.post("/")
@openapi.definition(
    body={"application/json": PasteSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")},
)
@validate(json=PasteSchemaAdd)
async def add_paste(
    request: Request, service: PastesService, user_service: UsersService, body: PasteSchemaAdd
) -> HTTPResponse:
    """
    Create new paste [need auth]
    """
    token = request.headers.get("Authorization")
    if not token:
        raise SanicException("You are unauthorized!", status_code=401)
    try:
        user_id = user_service.get_auth_user_id(token)
    except:
        raise SanicException("Please authorize again", status_code=401)
    body = body.model_dump()
    body.update({"user_id": user_id})
    uri = await service.add_paste(request.ctx.session, body)
    return response.json({"uri": uri})


@router.get("/")
async def get_user_pastes(request: Request, service: PastesService, user_service: UsersService) -> HTTPResponse:
    """
    Get user pastes [need auth]
    """
    token = request.headers.get("Authorization")
    if not token:
        raise SanicException("You are unauthorized!", status_code=401)
    try:
        user_id = user_service.get_auth_user_id(token)
    except:
        raise SanicException("Please authorize again", status_code=401)
    resp = await service.get_user_pastes(request.ctx.session, user_id=user_id)
    if not resp:
        raise SanicException("User has no any pastes", status_code=404)
    return response.json(resp)


@router.get("/<uri:str>")  # no auth needed
async def get_paste(request: Request, service: PastesService, uri: str) -> HTTPResponse:
    """
    Get paste by URI
    """
    try:
        resp = await service.get_paste(request.ctx.session, uri=uri)
        return response.json(resp)
    except:
        raise SanicException("Paste does not exist", status_code=404)
