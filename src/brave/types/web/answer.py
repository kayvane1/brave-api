from pydantic import BaseModel
from pydantic import Field
from typing import Optional


class Answer(BaseModel):
    """A response representing an answer to a question on a forum."""

    text: str = Field(description="The main content of the answer.")
    author: Optional[str] = Field(default=None, description="A name string for the author of the answer.")
    upvoteCount: Optional[int] = Field(default=None, description="Number of upvotes on the answer.")
    downvoteCount: Optional[int] = Field(default=None, description="The number of downvotes on the answer.")
