from pydantic import BaseModel
from pydantic import Field


class Answer(BaseModel):
    """A response representing an answer to a question on a forum."""

    text: str = Field(description="The main content of the answer.")
    author: str = Field(description="A name string for the author of the answer.")
    upvoteCount: int = Field(description="Number of upvotes on the answer.")
    downvoteCount: int = Field(description="The number of downvotes on the answer.")
