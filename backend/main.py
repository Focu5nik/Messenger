from contextlib import asynccontextmanager

# from core.models import Base, db_helper
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import lifespan
from core.config import settings
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Укажите список разрешенных доменов или "*" для разрешения со всех доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки HTTP
)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello")
def hello():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
