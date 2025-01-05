import json

from sanic import Blueprint
from sanic.request import Request
from sanic_ext import render

from backend.pastes.router import get_paste
from backend.pastes.service import PastesService

import os
import jinja2

frontdir = os.path.dirname(__file__)
loader = jinja2.FileSystemLoader(os.path.join(frontdir))
environment = jinja2.Environment(loader=loader, enable_async=True)
# environment.globals.update({"styles": os.path.join(frontdir, "static/styles.css")})

router = Blueprint("Frontend")


@router.get("/<uri:str>")  # no auth needed
async def render_paste(request: Request, service: PastesService, uri: str):
    """
    Get paste page by URI
    """
    data = await get_paste(request, service, uri)
    body = json.loads(data.body)
    return await render(
        "paste.html",
        environment=environment,
        context={"data": body},
    )
