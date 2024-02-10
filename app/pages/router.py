from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.candles.router import get_candles, get_all_candles


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/candles")
async def get_candles_page(
        request: Request,
        candles=Depends(get_candles)
):
    return templates.TemplateResponse(
        name="candles.html",
        context={"request": request, "candles": candles}
    )


@router.get("/candles_all")
async def get_candles_all_page(
    request: Request,
    candles=Depends(get_all_candles)
):
    return templates.TemplateResponse(
        name="candles.html",
        context={"request": request, "candles": candles},
    )





