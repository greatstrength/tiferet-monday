# *** imports

# ** infra
from tiferet.data import *

# ** app
from ..models.item import *

# *** data


# ** data: item_board_data
class ItemBoardData(DataObject):
    """
    Represents the data required to create an item in a Monday.com board.
    """

    class Options():
        """
        Options for the ItemBoardData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('id'),
            to_data=DataObject.allow()
        )

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the board to which the item belongs.'
        )
    )

# ** data: item_data
class ItemData(DataObject, Item):
    """
    Represents the data required to create an item in a Monday.com board.
    """

    class Options():
        """
        Options for the ItemData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('board'),
            to_data=DataObject.allow()
        )

    # * attribute: board
    board = ModelType(
        ItemBoardData,
        required=True,
        metadata=dict(
            description='The board to which the item belongs.'
        )
    )

    # * method: map
    def map(self) -> Item:
        """
        Maps the data object to an Item model.

        :return: An Item model instance.
        :rtype: Item
        """
        
        return super().map(
            Item,
            board_id=self.board.id
        )