from pydantic import BaseModel
from pydantic import Field


class Language(BaseModel):
    """
    A model representing a language.

    url: https://api.search.brave.com/app/documentation/web-search/responses#Language
    """

    main: str = Field(description="The main language seen in the string.")
