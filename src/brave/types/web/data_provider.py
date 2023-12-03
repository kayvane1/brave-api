from pydantic import BaseModel
from pydantic import Field


class DataProvider(BaseModel):
    """A model representing the data provider associated with the entity."""

    type: str = Field(
        default="external", description="A type representing the source of data. This is usually external."
    )
    name: str = Field(description="The name of the data provider. This can be a domain.")
    url: str = Field(description="The URL where the information is coming from.")
    long_name: str = Field(description="The long name for the data provider.")
    img: str = Field(description="The served URL for the image data.")
