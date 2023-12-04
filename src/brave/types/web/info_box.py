from typing import Any
from typing import List
from typing import Optional

from pydantic import Field

from ..shared.meta_url import MetaUrl
from ..shared.thumbnail import Thumbnail
from .data_provider import DataProvider
from .faq import QAPage
from .location_result import LocationResult
from .movie_data import MovieData
from .profile import Profile
from .rating import Rating
from .result import Result
from .unit import Unit


class GraphInfobox(Result):
    """Aggregated information on an entity from a knowledge graph."""

    type: str = Field(default="infobox", description="The infobox result type identifier.")
    position: int = Field(description="The position on a search result page.")
    label: str = Field(description="Label of the entity.")
    category: str = Field(description="Category of the entity.")
    long_desc: str = Field(description="Long description of the entity.")
    thumbnail: Thumbnail = Field(description="The thumbnail associated with the entity.")
    attributes: List[Any] = Field(description="A list of attributes about the entity.")
    profiles: List[Profile] = Field(description="The profiles associated with the entity.")
    website_url: str = Field(description="The official website pertaining to the entity.")
    attributes_shown: int = Field(description="The number of attributes to be shown about the entity.")
    ratings: List[Rating] = Field(description="Any ratings given to the entity.")
    providers: List[DataProvider] = Field(description="A list of data sources for the entity.")
    distance: Unit = Field(description="A unit representing quantity relevant to the entity.")
    images: List[Thumbnail] = Field(description="A list of images relevant to the entity.")
    movie: Optional[MovieData] = Field(
        description="Only when the result is a movie, any movie data relevant to the entity."
    )


class GenericInfobox(GraphInfobox):
    """Generic infobox."""

    subtype: str = Field(default="generic", description="The subtype of the infobox.")
    found_in_urls: List[str] = Field(description="URLs where the entity is found.")


class QAInfobox(GraphInfobox):
    """QA infobox."""

    subtype: str = Field(default="code", description="The subtype of the infobox.")
    data: QAPage = Field(description="QA page data.")
    meta_url: MetaUrl = Field(description="Aggregated information about the URL.")


class InfoboxWithLocation(GenericInfobox):
    """Infobox with location information."""

    subtype: str = Field(default="location", description="The subtype of the infobox.")
    is_location: bool = Field(description="Whether the entity is a location.")
    coordinates: List[float] = Field(description="[latitude, longitude]")
    zoom_level: int = Field(description="Zoom level for maps.")
    location: LocationResult = Field(description="Location result data.")


class InfoboxPlace(InfoboxWithLocation):
    """Place-specific infobox."""

    subtype: str = Field(default="place", description="The subtype of the infobox.")
    # Inherits all fields from InfoboxWithLocation and GenericInfobox
