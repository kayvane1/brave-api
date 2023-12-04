from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail


class ImageProperties(BaseModel):
    """Metadata on an image."""

    url: str = Field(description="The image URL.")
    resized: str = Field(description="The resized image.")
    height: int = Field(description="The height of the image.")
    width: int = Field(description="The width of the image.")
    format: str = Field(description="The format specifier for the image.")
    content_size: str = Field(description="The image storage size.")


class Image(BaseModel):
    """A model describing an image."""

    thumbnail: Thumbnail = Field(description="The thumbnail associated with the image.")
    url: str = Field(description="The URL of the image.")
    properties: ImageProperties = Field(description="Metadata on the image.")
