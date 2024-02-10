from sqladmin import ModelView

from app.users.models import Users
from app.baskets.models import Baskets
from app.candles.models import Candles


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.baskets] # kakie kolonki pokazat
    column_details_exclude_list = [Users.hashed_password] #kakie kolonki skrivat
    can_delete = True # pravo na udaleniye
    name = "Пользователь" # nazvanie 1-go elementa
    name_plural = "Пользователи" # nazvanie gruppi elementov
    icon = "fa-solid fa-user" # ikonka


class BasketsAdmin(ModelView, model=Baskets):
    column_list = [c.name for c in Baskets.__table__.c] + [Baskets.user, Baskets.candle]# kakie kolonki pokazat
    name = "Корзина" # nazvanie 1-go elementa
    name_plural = "Корзины" # nazvanie gruppi elementov


class CandlesAdmin(ModelView, model=Candles):
    column_list = [c.name for c in Candles.__table__.c] + [Candles.baskets]
    name = "Свеча"
    name_plural = "Свечи"



