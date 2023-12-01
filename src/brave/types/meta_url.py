from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class MetaUrl(BaseModel):
    """
    Aggregated information about a URL.

    url: https://api.search.brave.com/app/documentation/web-search/responses#MetaUrl
    """

    scheme: str = Field(description="The protocol scheme extracted from the URL.")
    netloc: str = Field(description="The network location part extracted from the URL.")
    hostname: str = Field(description="The lowercased domain name extracted from the URL.")
    favicon: HttpUrl = Field(description="The favicon used for the URL.")
    path: str = Field(description="The hierarchical path of the URL useful as a display string.")
