# *** imports

# ** infra
from tiferet.data import *

# ** app
from ..models.item import *

# *** data

# ** data: column_data
class ColumnData(DataObject):
    """
    Represents a column in a Monday.com item.
    """

    class Options():
        """
        Options for the ColumnData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('title', 'description', 'settings_str'),
            to_data=DataObject.allow()
        )

    # * attribute: title
    title = StringType(
        metadata=dict(
            description='The title of the column.'
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

# ** data: column_value_data
class ColumnValueData(DataObject, ColumnValue):
    """
    Represents a column value in a Monday.com item.
    """

    class Options():
        """
        Options for the ColumnValueData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('column'),
            to_data=DataObject.allow()
        )

    # * attribute: column
    column = ModelType(
        ColumnData,
        required=True,
        metadata=dict(
            description='The column to which the value belongs.'
        )
    )

    # * method: map
    def map(self) -> ColumnValue:
        """
        Maps the data object to a ColumnValue model.

        :return: A ColumnValue model instance.
        :rtype: ColumnValue
        """
        
        return super().map(
            ColumnValue,
            name=self.column.title,
            description=self.column.description,
            settings_str=self.column.settings_str
        )


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

# ** data: item_group_data
class ItemGroupData(DataObject):
    """
    Represents the data required to create an item group in a Monday.com board.
    """

    class Options():
        """
        Options for the ItemGroupData class.
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
            description='The unique identifier of the group to which the item belongs.'
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
        
        # Map the board data to the Item model.
        return super().map(
            Item,
            board_id=self.board.id
        )
    
# ** data: item_detail_data
class ItemDetailData(DataObject, ItemDetail):
    """
    Represents the detailed data of an item in a Monday.com board.
    """

    class Options():
        """
        Options for the ItemDetailData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('board', 'group', 'column_values'),
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

    # * attribute: group
    group = ModelType(
        ItemGroupData,
        required=True,
        metadata=dict(
            description='The group to which the item belongs.'
        )
    )

    # * attribute: column_values
    column_values = ListType(
        ModelType(ColumnValueData),
        default=[],
        metadata=dict(
            description='A list of column values associated with the item.'
        )
    )

    # * method: map
    def map(self) -> ItemDetail:
        """
        Maps the data object to an ItemDetail model.

        :return: An ItemDetail model instance.
        :rtype: ItemDetail
        """
        
        # Map the column values to their respective models.
        return super().map(
            ItemDetail,
            board_id=self.board.id,
            group_id=self.group.id,
            column_values=[value.map() for value in self.column_values]
        )
