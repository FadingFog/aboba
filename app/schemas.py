from pydantic import BaseModel, ConfigDict


class SomeData(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Added to simplify tests

    id: int
    name: str
