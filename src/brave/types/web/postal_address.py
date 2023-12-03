from pydantic import BaseModel
from pydantic import Field


class PostalAddress(BaseModel):
    """A model representing a postal address of a location."""

    type: str = Field(
        default="PostalAddress", description="A type identifying a postal address. The value is always postaladdress."
    )
    country: str = Field(description="The country associated with the location.")
    postalCode: str = Field(description="The postal code associated with the location.")
    streetAddress: str = Field(description="The street address associated with the location.")
    addressRegion: str = Field(description="The region associated with the location. This is usually a state.")
    addressLocality: str = Field(description="The address locality or subregion associated with the location.")
    displayAddress: str = Field(description="The displayed address string.")
