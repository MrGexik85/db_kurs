from typing import NamedTuple
from pydantic import BaseModel, Field



class UserSession(NamedTuple):
    id: int
    username: str
    isAdmin: bool


class CreateUserOrder(BaseModel):
    productId: int = Field(description='Идентификатор товара', example=2)
    amount: int = Field(description='Количество товара', example=2)
    delivery_terms: str = Field(description='Условия доставки', example='Самовывоз')
    notes: str = Field(description='Заметки к заказу', example='Доставить до 5 июля')
