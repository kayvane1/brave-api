from typing import List

from pydantic import BaseModel
from pydantic import Field

from .search_result import SearchResult


class ForumData(BaseModel):
    """Defines a result from a discussion forum."""

    forum_name: str = Field(description="The name for the forum.")
    num_answers: int = Field(description="The number of answers in the post.")
    score: str = Field(description="The score of the post in the forum.")
    title: str = Field(description="The title of the post in the forum.")
    question: str = Field(description="The question asked in the forum post.")
    top_comment: str = Field(description="The top-rated comment on the forum post.")


class DiscussionResult(SearchResult):
    """A discussion result. These are forum posts and discussions that are relevant to the search query."""

    type: str = Field(
        default="discussion", description="The discussion result type identifier. The value is always discussion."
    )
    data: ForumData = Field(description="The enriched aggregated data for the relevant forum post.")


class Discussions(BaseModel):
    """A model representing a discussion cluster relevant to the query."""

    type: str = Field(
        default="search",
        description="The type identifying a discussion cluster. Currently, the value is always search.",
    )
    results: List[DiscussionResult] = Field(description="A list of discussion results.")
    mutated_by_goggles: bool = Field(
        default=False, description="Whether the discussion results are changed by a Goggle."
    )
