from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from ..shared.meta_url import MetaUrl
from .answer import Answer


class QAPage(BaseModel):
    """Aggreated result from a question answer page."""

    question: str = Field(description="The question being asked.")
    answer: Answer = Field(description="The answer to the question.")


class QA(BaseModel):
    """A question-answer result."""

    question: str = Field(description="The question being asked.")
    answer: str = Field(description="The answer to the question.")
    title: str = Field(description="The title of the post.")
    url: HttpUrl = Field(description="The URL pointing to the post.")
    meta_url: MetaUrl = Field(description="Aggregated information about the URL.")


class FAQ(BaseModel):
    """Frequently asked questions relevant to the search query term."""

    type: str = Field(default="faq", description="The FAQ result type identifier. The value is always faq.")
    results: Optional[List[QA]] = Field(
        default=None, description="A list of aggregated question-answer results relevant to the query."
    )
