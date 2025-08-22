# *** imports

# ** infra
from tiferet.models import *

# ** app
from ..models.doc import DocumentBlock

# *** models

# * model: reply
class Reply(Entity):
    """
    Represents a reply in a Monday.com item.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the reply.'
        )
    )

    # * attribute: creator_id
    creator_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the user who created the reply.'
        )
    )

    # * attribute: body
    body = StringType(
        required=True,
        metadata=dict(
            description='The content of the reply.'
        )
    )

# ** model: update
class Update(Entity):
    """
    Represents an update in a Monday.com item.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the update.'
        )
    )

    # * attribute: creator_id
    creator_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the user who created the update.'
        )
    )

    # * item_id
    item_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the item to which the update belongs.'
        )
    )

    # * attribute: body
    body = StringType(
        required=True,
        metadata=dict(
            description='The content of the update.'
        )
    )

    # * attribute: replies
    replies = ListType(
        ModelType(Reply),
        default=[],
        metadata=dict(
            description='A list of replies associated with the update.'
        )
    )

# ** model: column_value
class ColumnValue(ValueObject):
    """
    Represents a column value in a Monday.com item.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the column.'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The column title.'
        )
    )

    # * attribute: type
    type = StringType(
        required=True,
        metadata=dict(
            description='The type of the column value.'
        )
    )

    # * attribute: value
    value = StringType(
        metadata=dict(
            description='The actual value of the column.'
        )
    )

    # * attribute: description
    description = StringType(
        metadata=dict(
            description='A description of the column.'
        )
    )
    
    # * attribute: settings_str
    settings_str = StringType(
        metadata=dict(
            description='A JSON string representing the settings of the column.'
        )
    )

# ** model: item
class Item(Entity):
    """
    Represents an item in the Monday.com system.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the monday.com item.'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The name of the item.'
        )
    )

    # * attribute: board_id
    board_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the board to which the item belongs.'
        )
    )

    # * attribute: updates
    updates = ListType(
        ModelType(Update),
        default=[],
        metadata=dict(
            description='A list of updates associated with the item.'
        )
    )

# ** model: item_description
class ItemDescription(Entity):
    """
    Represents the description of a Monday.com item.
    """

    # * attribute: 
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the item description document.'
        )
    )

    # * attribute: blocks
    blocks = ListType(
        ModelType(DocumentBlock),
        default=[],
        metadata=dict(
            description='A list of document blocks that make up the item description.'
        )
    )

# ** model: item_detail
class ItemDetail(Item):
    """
    Represents the detailed information of an item in a Monday.com board.
    """

    # * attribute: group_id
    group_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the group to which the item belongs.'
        )
    )

    # * attribute: description
    description = ModelType(
        ItemDescription,
        metadata=dict(
            description='The description of the item.'
        )
    )

    # * attribute: column_values
    column_values = ListType(
        ModelType(ColumnValue),
        default=[],
        metadata=dict(
            description='A list of column values associated with the item.'
        )
    )

# ** model: subitem
class Subitem(Item):
    """
    Represents a subitem in a Monday.com item.
    """

    # * attribute: parent_item_id
    parent_item_id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the parent item to which this subitem belongs.'
        )
    )

    # * attribute: column_values
    column_values = ListType(
        ModelType(ColumnValue),
        default=[],
        metadata=dict(
            description='A list of column values associated with the subitem.'
        )
    )
