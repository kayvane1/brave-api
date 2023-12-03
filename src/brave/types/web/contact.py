from pydantic import BaseModel
from pydantic import Field


class Contact(BaseModel):
    """A model representing contact information for an entity."""

    email: str = Field(description="The email address.")
    telephone: str = Field(description="The telephone number.")
