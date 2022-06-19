from datetime import datetime
from pydantic import BaseModel, Field


class ShortContractor(BaseModel):
    id: int = Field(description='Уникальный идентификатор', example=1)
    title: str = Field(description='Название', example='ООО Капитал')


class ShortProduct(BaseModel):
    id: int = Field(description='Уникальный идентификатор', example=1)
    title: str = Field(description='Название', example='AirPods Max')


class SupplyResponse(BaseModel):
    id: int = Field(description='Уникальный идентификатор', example=1)
    contractor: ShortContractor = Field()
    product: ShortProduct = Field()
    amount: int = Field(description='Количество', example=20)
    date: datetime = Field(description='Дата поставки', example='2022-03-25 14:00:00')


class CreateSupply(BaseModel):
    contractor_id: int = Field(description='Идентификатор поставщика', example=1)
    product_id: int = Field(description='Идентификатор продукта', example=1)
    amount: int = Field(description='Количество продукта', example=20)
    date: datetime = Field(description='Дата поставки', example='2022-03-25 14:00:00')
