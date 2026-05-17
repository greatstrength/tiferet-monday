"""Tiferet Monday Item Domain Objects"""

# *** imports

# ** core
from typing import Optional, List

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: reply
class Reply(MondayDomainObject):
    '''
    Represents a reply to an update on a Monday.com item.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the reply.'
    )

    # * attribute: creator_id
    creator_id: Optional[str] = Field(
        default=None,
        description='The unique identifier of the reply creator.'
    )

    # * attribute: body
    body: Optional[str] = Field(
        default=None,
        description='The content of the reply.'
    )


# ** model: update
class Update(MondayDomainObject):
    '''
    Represents an update (comment) on a Monday.com item.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the update.'
    )

    # * attribute: creator_id
    creator_id: Optional[str] = Field(
        default=None,
        description='The unique identifier of the update creator.'
    )

    # * attribute: item_id
    item_id: Optional[str] = Field(
        default=None,
        description='The item ID this update belongs to.'
    )

    # * attribute: body
    body: Optional[str] = Field(
        default=None,
        description='The HTML content of the update.'
    )

    # * attribute: text_body
    text_body: Optional[str] = Field(
        default=None,
        description='The plain text content of the update.'
    )

    # * attribute: replies
    replies: List[Reply] = Field(
        default_factory=list,
        description='A list of replies to this update.'
    )


# ** model: item
class Item(MondayDomainObject):
    '''
    Represents an item (row) in a Monday.com board.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the item.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the item.'
    )

    # * attribute: board_id
    board_id: Optional[str] = Field(
        default=None,
        description='The board ID this item belongs to.'
    )

    # * attribute: group_id
    group_id: Optional[str] = Field(
        default=None,
        description='The group ID this item belongs to.'
    )

    # * attribute: state
    state: Optional[str] = Field(
        default=None,
        description='The state of the item (active / archived / deleted).'
    )

    # * attribute: created_at
    created_at: Optional[str] = Field(
        default=None,
        description='The creation date of the item (ISO8601).'
    )

    # * attribute: updated_at
    updated_at: Optional[str] = Field(
        default=None,
        description='The last update date of the item (ISO8601).'
    )

    # * attribute: parent_item_id
    parent_item_id: Optional[str] = Field(
        default=None,
        description='The parent item ID (for subitems).'
    )

    # * attribute: creator_id
    creator_id: Optional[str] = Field(
        default=None,
        description='The creator user ID.'
    )
