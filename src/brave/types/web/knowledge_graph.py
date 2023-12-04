from pydantic import BaseModel
from pydantic import Field

from .url import URL


class KnowledgeGraphEntity(BaseModel):
    """Represents a knowledge graph entity."""

    title: str = Field(description="A short title describing the entity.")
    description: str = Field(description="A description of the entity.")
    url: URL = Field(description="The URL representing the entity.")
    thumbnail: URL = Field(description="The thumbnail associated with the entity.")


class KnowledgeGraphProfile(KnowledgeGraphEntity):
    """Represents an entity profile from a knowledge graph."""

    description: str = Field(description="A description of the entity.")
    url: URL = Field(description="The URL representing the entity.")
