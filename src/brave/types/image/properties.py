from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class Properties(BaseModel):
    """Metadata on an image."""

    url: HttpUrl = Field(description="The image URL.")
    placeholder: HttpUrl = Field(description="The lower resolution placeholder image URL.")
