"""Tiferet Monday Board Domain Objects"""

# *** imports

# ** core
from typing import Optional

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: column
class Column(MondayDomainObject):
    '''
    Represents a column in a Monday.com board.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the column.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The title of the column.'
    )

    # * attribute: type
    type: str = Field(
        ...,
        description='The type of the column.'
    )

    # * attribute: description
    description: Optional[str] = Field(
        default=None,
        description='A description of the column.'
    )

    # * attribute: settings_str
    settings_str: Optional[str] = Field(
        default=None,
        description='A JSON string representing the settings of the column.'
    )


# ** model: group
class Group(MondayDomainObject):
    '''
    Represents a group in a Monday.com board.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the group.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The title of the group.'
    )

    # * attribute: position
    position: Optional[str] = Field(
        default=None,
        description='The position of the group in the board.'
    )

    # * attribute: color
    color: Optional[str] = Field(
        default=None,
        description='The color of the group.'
    )


# ** model: board
class Board(MondayDomainObject):
    '''
    Represents a board in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the board.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the board.'
    )

    # * attribute: description
    description: Optional[str] = Field(
        default=None,
        description='The description of the board.'
    )

    # * attribute: board_kind
    board_kind: Optional[str] = Field(
        default=None,
        description='The kind of the board (public / private / share).'
    )

    # * attribute: state
    state: Optional[str] = Field(
        default=None,
        description='The state of the board (active / archived / deleted).'
    )

    # * attribute: workspace_id
    workspace_id: Optional[str] = Field(
        default=None,
        description='The workspace unique identifier.'
    )

    # * attribute: permissions
    permissions: Optional[str] = Field(
        default=None,
        description='The board permissions.'
    )

    # * attribute: updated_at
    updated_at: Optional[str] = Field(
        default=None,
        description='The last time the board was updated (ISO8601).'
    )
