# *** imports

# ** infra
from tiferet.models import *

# *** models

# ** model: column
class Column(ValueObject):
    """
    Represents a column in a Monday.com board.
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
            description='The title of the column.'
        )
    )

    # * attribute: type
    type = StringType(
        required=True,
        metadata=dict(
            description='The type of the column.'
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

# ** model: group
class Group(ValueObject):
    """
    Represents a group in a Monday.com board.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the group.'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The title of the group.'
        )
    )

    # * attribute: position
    position = StringType(
        metadata=dict(
            description='The position of the group in the board.'
        )
    )