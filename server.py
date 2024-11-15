import uvicorn
from sanic import Blueprint, Sanic

from backend.db.db import async_session, create_tables, drop_tables
from backend.pastes.dependencies import paste_service
from backend.pastes.router import router as p_router
from backend.users.dependencies import user_service
from backend.users.router import router as u_router
from frontend.router import router as f_router

app = Sanic("Pastebin")

api = Blueprint.group(u_router, p_router, name_prefix="API", url_prefix="/api")
app.blueprint(api)
app.blueprint(f_router)


app.ext.dependency(user_service)
app.ext.dependency(paste_service)


@app.after_server_start
async def create_db_tables(app, loop):
    await create_tables()


@app.before_server_stop
async def drop_db_tables(app, loop):
    await drop_tables()


@app.on_request
async def inject_session(request):
    request.ctx.session = async_session()


@app.on_response
async def close_session(request, response):
    if hasattr(request.ctx, "session"):
        await request.ctx.session.close()


@app.on_response
async def prevent_xss(request, response):
    response.headers["X-XSS-protection"] = "1; mode=block"


if __name__ == "__main__":  # ASGI
    uvicorn.run(
        app=app,
        loop="none",
        host="0.0.0.0",
        port=8000,
    )
