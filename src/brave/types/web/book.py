from typing import List

from pydantic import BaseModel
from pydantic import Field

from .person import Person
from .price import Price
from .rating import Rating


class Book(BaseModel):
    """A model representing a book result."""

    title: str = Field(description="The title of the book.")
    author: List[Person] = Field(description="The author of the book.")
    date: str = Field(description="A published date for the book.")
    price: Price = Field(description="The price of the book.")
    pages: str = Field(description="The number of pages in the book.")
    publisher: Person = Field(description="The publisher of the book.")
    rating: Rating = Field(description="A gathered rating from different sources associated with the book.")
