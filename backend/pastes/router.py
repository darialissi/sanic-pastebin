from sanic import Blueprint, HTTPResponse, response
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic_ext import openapi

from backend.utils.auth.token import Token
from config import settings

from .schema import PasteSchemaAdd
from .service import PastesService

router = Blueprint("Pastes", url_prefix="/pastes")


@router.post("/")
@openapi.definition(
    body={"application/json": PasteSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")},
)
async def add_paste(request: Request, service: PastesService) -> HTTPResponse:
    """
    Create new paste [need auth]
    """
    try:
        token = request.cookies.get("jwt-token")
    except Exception:
        raise SanicException("You are unauthorized!", status_code=401)
    decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=token)
    user_id = decoded.get("sub")
    request.json.update({"user_id": user_id})
    uri = await service.add_paste(request.ctx.session, request.json)
    return response.json({"uri": uri})


@router.get("/")
async def get_user_pastes(request: Request, service: PastesService) -> HTTPResponse:
    """
    Get user pastes [need auth]
    """
    try:
        token = request.cookies.get("jwt-token")
    except Exception:
        raise SanicException("You are unauthorized!", status_code=401)
    decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=token)
    user_id = decoded.get("sub")
    resp = await service.get_user_pastes(request.ctx.session, user_id=user_id)
    if not resp:
        raise SanicException("User has no any pastes", status_code=404)
    return response.json(resp)


@router.get("/<uri:str>")  # no auth needed
async def get_paste(request: Request, service: PastesService, uri: str) -> HTTPResponse:
    """
    Get paste by URI
    """
    resp = await service.get_paste(request.ctx.session, uri=uri)
    if not resp:
        raise SanicException("Paste does not exist", status_code=404)
    return response.json(resp)
