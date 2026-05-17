"""Tiferet Monday Workspace Domain Objects"""

# *** imports

# ** core
from typing import Optional

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: workspace
class Workspace(MondayDomainObject):
    '''
    Represents a workspace in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the workspace.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the workspace.'
    )

    # * attribute: kind
    kind: Optional[str] = Field(
        default=None,
        description='The workspace kind (open / closed).'
    )

    # * attribute: description
    description: Optional[str] = Field(
        default=None,
        description='The workspace description.'
    )

    # * attribute: state
    state: Optional[str] = Field(
        default=None,
        description='The workspace state (active / archived / deleted).'
    )

    # * attribute: created_at
    created_at: Optional[str] = Field(
        default=None,
        description='The workspace creation date.'
    )
