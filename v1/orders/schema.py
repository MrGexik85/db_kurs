from datetime import datetime
from pydantic import BaseModel, Field

from v1.product.schema import Category


class Customer(BaseModel):
    id: int = Field(example=1)
    title: str = Field(example='ООО Сириус')
    address: str = Field(example='Пушкина, 22')
    phone: str = Field(example='8931234124')
    first_name: str = Field(example='Евгений')
    last_name: str = Field(example='Иванов')


class Product(BaseModel):
    id: int = Field(example=1)
    title: str = Field(example='AirPods Max')
    description: str | None = Field(default=None, example='Полноразмерные беспроводные наушники')
    image_url: str = Field(example="https://blabla.com/jpg")
    price: int = Field(example=20000)
    count: int = Field(example=10)
    package: str = Field(example='Картон')
    category: Category = Field()


class Order(BaseModel):
    id: int = Field(example=1)
    number: int = Field(example=3151512)
    date: datetime = Field(example='2022-04-12 12:00:00')
    note: str | None = Field(example='Доставка не в выходной день')
    delivery_terms: str = Field(example='Самовывоз')
    is_paid: bool = Field(example=False)
    is_deliver: bool = Field(example=True)
    customer: Customer = Field()
    products: list[Product] = Field()

