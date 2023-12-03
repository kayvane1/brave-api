from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class Offer(BaseModel):
    """An offer associated with a product."""

    url: HttpUrl = Field(description="The URL where the offer can be found.")
    priceCurrency: str = Field(description="The currency in which the offer is made.")
    price: str = Field(description="The price of the product currently on offer.")
