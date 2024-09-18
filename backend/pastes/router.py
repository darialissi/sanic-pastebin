from sanic import Blueprint, HTTPResponse, response
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic_ext import openapi

from backend.utils.auth.token import Token
from config import settings

from .object_storage import PastesStorage
from .repository import PastesRepository
from .schema import PasteSchemaAdd, PasteURI
from .service import PastesService

router = Blueprint("Pastes", url_prefix="/pastes")

service = PastesService(
    pastes_repo=PastesRepository,
    object_storage=PastesStorage,
)


@router.post("/")
@openapi.definition(
    body={"application/json": PasteSchemaAdd.model_json_schema(ref_template="#/components/schemas/{model}")},
)
async def add_paste(request: Request) -> HTTPResponse:
    """
    Create new paste [need auth]
    """
    if not request.token:
        raise SanicException("You are unauthorized", status_code=401)
    decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=request.token)
    user_id = decoded.get("sub")
    request.json.update({"user_id": user_id})
    uri = await service.add_paste(request.ctx.session, request.json)
    return response.json({"uri": uri})


@router.get("/")
async def get_user_pastes(request: Request) -> HTTPResponse:
    """
    Get user pastes [need auth]
    """
    if not request.token:
        raise SanicException("You are unauthorized", status_code=401)
    decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=request.token)
    user_id = decoded.get("sub")
    resp = await service.get_user_pastes(request.ctx.session, user_id=user_id)
    if not resp:
        raise SanicException("User has no any pastes", status_code=404)
    return response.json(resp)


@router.get("/<uri>")  # no auth needed
async def get_paste(request: Request, uri: PasteURI) -> HTTPResponse:
    """
    Get paste by URI
    """
    resp = await service.get_paste(request.ctx.session, uri=uri)
    if not resp:
        raise SanicException("Paste does not exist", status_code=404)
    return response.json(resp)
