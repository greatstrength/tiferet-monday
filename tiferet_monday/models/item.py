# *** imports

# ** core
from typing import List, Dict, Any, Tuple

# ** infra
from tiferet.models import *

# ** app
from .doc import DocumentBlock
from .column_value import *

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
        metadata=dict(
            description='The unique identifier of the group to which the item belongs.'
        )
    )

    # * attribute: parent_item_id
    parent_item_id = StringType(
        metadata=dict(
            description='The unique identifier of the parent item to which this subitem belongs.'
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

    # * method: new
    @staticmethod
    def new(
        id: str, 
        name: str, 
        board_id: str, 
        group_id: str, 
        parent_item_id: str = None,
        description: Dict[str, Any] = None,
        column_values: List[Dict[str, Any]] = [], 
        updates: List[Dict[str, Any]] = []
    ) -> 'ItemDetail':
        """
        Creates a new ItemDetail instance with the provided attributes.

        :param id: The unique identifier of the item.
        :type id: str
        :param name: The name of the item.
        :type name: str
        :param board_id: The unique identifier of the board to which the item belongs.
        :type board_id: str
        :param group_id: The unique identifier of the group to which the item belongs.
        :type group_id: str
        :param parent_item_id: The unique identifier of the parent item (for subitems).
        :type parent_item_id: str
        :param description: The description of the item as a dictionary.
        :type description: Dict[str, Any]
        :param column_values: A list of column values as dictionaries.
        :type column_values: List[Dict[str, Any]]
        :param updates: A list of updates as dictionaries.
        :type updates: List[Dict[str, Any]]
        :return: A new ItemDetail instance.
        :rtype: ItemDetail
        """

        # Create column values list first.
        column_values = [
            ColumnValue.new(**cv) for cv in column_values
        ]
        
        # Create and return a new ItemDetail instance with the provided attributes.
        return ModelObject.new(
            ItemDetail,
            id=id,
            name=name,
            board_id=board_id,
            group_id=group_id,
            parent_item_id=parent_item_id,
            description=description,
            updates=updates,
            column_values=column_values,
        )

    # method: get_column_value
    def get_column_value(self, column_id_or_title) -> ColumnValue | None:
        """
        Retrieves a column value by its ID.

        :param column_id: The unique identifier of the column.
        :type column_id: str
        :return: The ColumnValue object if found, otherwise None.
        :rtype: ColumnValue | None
        """
        
        # First search on title, as it's more human friendly.
        column_value: ColumnValue = next((cv for cv in self.column_values if cv.name == column_id_or_title), None)
        
        # Return the formatted value if found by title, otherwise search by ID.
        if column_value:
            return column_value
        else:
            return next((cv for cv in self.column_values if cv.id == column_id_or_title), None)
        
    # * method: get_column_values
    def get_column_values(self, column_ids_or_titles: List[str]) -> Tuple[ColumnValue]:
        """
        Retrieves multiple column values by their IDs.

        :param column_ids_or_titles: A list of unique identifiers or titles of the columns.
        :type column_ids_or_titles: List[str]
        :return: A list of ColumnValue objects matching the provided IDs.
        :rtype: List[ColumnValue]
        """
        
        # Create map of column ids for quick lookup.
        column_value_map = {cv.id: cv for cv in self.column_values}

        # Add titles to the map as well.
        column_value_map.update({cv.name: cv for cv in self.column_values}) 

        # Filter and return the column values that match the provided IDs in order.
        return tuple([column_value_map[id_or_title] for id_or_title in column_ids_or_titles])