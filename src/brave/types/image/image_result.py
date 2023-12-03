from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from ..shared.meta_url import MetaUrl
from ..shared.thumbnail import Thumbnail
from .properties import Properties


class ImageResult(BaseModel):
    """A model representing an image result for the requested query."""

    type: str = Field(
        default="image_result", description="The type of image search API result. The value is always image_result."
    )
    title: str = Field(description="The title of the image.")
    url: HttpUrl = Field(description="The original page URL where the image was found.")
    source: str = Field(description="The source domain where the image is found.")
    page_fetched: str = Field(
        description="The ISO date time when the page was last fetched. The format is YYYY-MM-DDTHH:MM:SSZ"
    )
    thumbnail: Thumbnail = Field(description="A thumbnail for the image.")
    properties: Properties = Field(description="Metadata for the image.")
    meta_url: MetaUrl = Field(description="Aggregated information on the URL associated with the image search result.")
