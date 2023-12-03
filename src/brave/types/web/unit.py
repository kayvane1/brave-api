from pydantic import BaseModel
from pydantic import Field


class Unit(BaseModel):
    """A model representing a unit of measurement."""

    value: float = Field(description="The quantity of the unit.")
    units: str = Field(description="The name of the unit associated with the quantity.")
