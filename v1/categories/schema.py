from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: int = Field(description='Уникальный идентификатор', example=2)
    name: str = Field(description='Название категории', example='древесина')


class CreateCategoryRequest(BaseModel):
    name: str = Field(description='Название категории', example='древесина')