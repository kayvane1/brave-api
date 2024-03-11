from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Thumbnail(BaseModel):
    """Aggregated details representing a picture thumbnail."""

    src: Optional[str] = Field(default=None, description="The served URL of the image.")
    height: Optional[int] = Field(default=None, description="The height of the image.")
    width: Optional[int] = Field(default=None, description="The width of the image.")
    bg_color: Optional[str] = Field(default=None, description="The background color of the image.")
    original: Optional[str] = Field(default=None, description="The original URL of the image.")
    logo: Optional[bool] = Field(default=False, description="Whether the image is a logo.")
    duplicated: Optional[bool] = Field(default=None, description="Whether the image is duplicated.")
    theme: Optional[str] = Field(default=None, description="The theme associated with the thumbnail.")
