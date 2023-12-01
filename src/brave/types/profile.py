from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class Profile(BaseModel):
    """
    Profile of an entity.

    url: https://api.search.brave.com/app/documentation/web-search/responses#Profile
    """

    name: str = Field(description="The name of the profile.")
    url: HttpUrl = Field(description="The original URL where the profile is available.")
    long_name: str = Field(description="The long name of the profile.")
    img: HttpUrl = Field(description="The served image URL representing the profile.")
