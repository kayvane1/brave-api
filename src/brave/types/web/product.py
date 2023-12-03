from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail
from .offer import Offer
from .rating import Rating


class Product(BaseModel):
    """A model representing a product."""

    type: str = Field(
        default="Product", description="A string representing a product type. The value is always product."
    )
    name: str = Field(description="The name of the product.")
    price: Optional[str] = Field(default=None, description="The price of the product.")
    thumbnail: Optional[Thumbnail] = Field(default=None, description="A thumbnail associated with the product.")
    description: Optional[str] = Field(default=None, description="The description of the product.")
    offers: Optional[List[Offer]] = Field(default=None, description="A list of offers available on the product.")
    rating: Optional[Rating] = Field(default=None, description="A rating associated with the product.")
