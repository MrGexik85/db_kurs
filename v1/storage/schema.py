from pydantic import BaseModel, Field


class ProductStorage(BaseModel):
    product_id: int = Field(description='Идентификатор продукта', example=2)
    title: str = Field(description='Название продукта', example='AirPods Max')
    remaind: int = Field(description='Остаток', example=20)