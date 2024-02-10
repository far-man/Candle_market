from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI


from redis import asyncio as aioredis

from app.baskets.router import router as router_baskets
from app.users.router import router as router_auth
from app.candles.router import router as router_candles

from app.pages.router import router as router_pages

from app.images.router import router as router_images

from app.importer.router import router as router_import

from app.config import settings
from app.database import engine

from app.admin.views import UsersAdmin, BasketsAdmin, CandlesAdmin
from app.admin.auth import authentication_backend


app = FastAPI(
    title="Ароматизированные свечи",
    version="0.1.0",
    root_path="/api",
    )# sozdayem API


app.include_router(router_auth)
app.include_router(router_baskets)
app.include_router(router_candles)

app.include_router(router_pages)
app.include_router(router_images) #podklyuchaem routeri
app.include_router(router_import)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"], # dlya CORS dayem razreshenie dlya HTML
)



# Подключение версионирования
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/api/v{major}',
)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")# dlya REDIS


admin = Admin(app, engine, authentication_backend=authentication_backend) # adminka

admin.add_view(UsersAdmin)
admin.add_view(BasketsAdmin)
admin.add_view(CandlesAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static") # dlya HTML