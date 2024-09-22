import json

from sanic import Blueprint
from sanic.request import Request
from sanic_ext import render

from backend.pastes.router import get_paste

router = Blueprint("Frontend")


@router.get("/")
async def render_main(request: Request):
    """
    Get main page
    """
    return await render(
        "main.html",
        context={"request": request},
    )


@router.get("/<uri>")  # no auth needed
async def render_paste(request: Request, uri: str):
    """
    Get paste page by URI
    """
    data = await get_paste(request, uri)
    body = json.loads(data.body)
    return await render(
        "paste.html",
        context={"data": body},
    )
