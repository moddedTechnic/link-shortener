import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel

app = FastAPI()

ROUTES_FILE = Path("./routes.json")


def load_routes():
    if not ROUTES_FILE.exists():
        return {}
    with ROUTES_FILE.open("r") as f:
        return json.load(f)


def save_routes(routes):
    with ROUTES_FILE.open("w") as f:
        return json.dump(routes, f)


REDIRECTIONS = load_routes()


@app.get("/")
def admin():
    return FileResponse("./admin.html")


@app.get("/l")
def redirect(target: str):
    if target not in REDIRECTIONS:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Link not found (got "{target}")',
        )
    return RedirectResponse(REDIRECTIONS[target])


@app.get("/l/{slug}")
def link(slug: str):
    return redirect(slug)


class TokenRequest(BaseModel):
    token: str


@app.post("/auth/validate")
def validate_auth(req: TokenRequest):
    return req.token == os.environ.get("AUTH_TOKEN")


@app.post("/routes")
def get_routes(auth: TokenRequest):
    if not validate_auth(auth):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return REDIRECTIONS


class UpdateRoutesRequest(TokenRequest):
    routes: list[tuple[str | None, str]]


def generate_slug():
    n = os.urandom(4)
    return n.hex()


@app.post("/routes/update")
def update_routes(req: UpdateRoutesRequest):
    if not validate_auth(req):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    routes = {k: v for k, v in req.routes if k and not k.startswith("temp-")}
    new_routes = [v for k, v in req.routes if not k or k.startswith("temp-")]
    keys = set(routes.keys()) | set(REDIRECTIONS.keys())
    for route in new_routes:
        while (slug := generate_slug()) in keys:
            pass
        keys.add(slug)
        routes[slug] = route
    REDIRECTIONS.clear()
    REDIRECTIONS.update(routes)
    save_routes(REDIRECTIONS)
