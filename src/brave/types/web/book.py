from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field

from .person import Person
from .price import Price
from .rating import Rating


class Book(BaseModel):
    """A model representing a book result."""

    title: str = Field(description="The title of the book.")
    author: Optional[List[Person]] = Field(default=None, description="The author of the book.")
    date: Optional[str] = Field(default=None, description="A published date for the book.")
    price: Optional[Union[Price, dict]] = Field(default=None, description="The price of the book.")
    pages: Optional[Union[str, int]] = Field(default=None, description="The number of pages in the book.")
    publisher: Optional[Person] = Field(default=None, description="The publisher of the book.")
    rating: Optional[Rating] = Field(
        default=None, description="A gathered rating from different sources associated with the book."
    )
