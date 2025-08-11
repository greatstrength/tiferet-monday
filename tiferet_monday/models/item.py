# *** imports

# ** infra
from tiferet.models import *

# *** models

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