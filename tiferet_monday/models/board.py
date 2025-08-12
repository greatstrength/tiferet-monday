# *** imports

# ** infra
from tiferet.models import *

# *** models

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