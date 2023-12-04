from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class ButtonResult(BaseModel):
    """A result which can be used as a button."""

    type: str = Field(
        default="button_result", description="A type identifying button result. The value is always button_result."
    )
    title: str = Field(description="The title of the result.")
    url: HttpUrl = Field(description="The URL for the button result.")
