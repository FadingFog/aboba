from pydantic import BaseModel


class SomeData(BaseModel):
    id: int
    name: str
