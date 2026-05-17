"""Tiferet Monday Tag Domain Objects"""

# *** imports

# ** core
from typing import Optional

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: tag
class Tag(MondayDomainObject):
    '''
    Represents a tag in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the tag.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the tag.'
    )

    # * attribute: color
    color: Optional[str] = Field(
        default=None,
        description='The color of the tag.'
    )
