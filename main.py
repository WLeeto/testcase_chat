from fastapi import FastAPI

from app.routers.history import history_router
from app.routers.ws.messenger import ws_router

app = FastAPI()
app.include_router(ws_router)
app.include_router(history_router)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "healthy!"}
