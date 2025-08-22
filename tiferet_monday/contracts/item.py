# *** imports

# ** core
from typing import List, Any

# ** infra
from tiferet.contracts import *

# ** app
from .doc import DocumentBlockContract

# *** contracts

# ** contract: item
class ItemContract(ModelContract):
    
    # * attribute: id
    id: str

    # * attribute: name
    name: str

    # * attribute: board_id
    board_id: str

# ** contract: column_value
class ColumnValueContract(ModelContract):
    """
    Represents a column value in a Monday.com item.
    """

    # * attribute: id
    id: str

    # * attribute: name
    name: str

    # * attribute: type
    type: str

    # * attribute: value
    value: str

# ** contract: item_description
class ItemDescriptionContract(ModelContract):
    """
    Represents the description of a Monday.com item.
    """

    # * attribute: text
    text: str

    # * attribute: blocks
    blocks: List[DocumentBlockContract]

# ** contract: item_detail
class ItemDetailContract(ItemContract):
    """
    Represents the detailed information of an item in a Monday.com board.
    """

    # * attribute: group_id
    group_id: str

    # * attribute: column_values
    column_values: List[ColumnValueContract]

    # * attribute: description
    description: ItemDescriptionContract

# ** contract: subitem
class SubitemContract(ItemContract):
    """
    Represents a subitem in a Monday.com item.
    """

    # * attribute: parent_item_id
    parent_item_id: str

    # * attribute: column_values
    column_values: List[ColumnValueContract]

# ** contract: item_repo
class ItemRepository(Repository):
    """
    Repository for managing item-related operations.
    """

    # * method: query_detail_by_id
    @abstractmethod
    def query_detail_by_id(self, item_id: str | int) -> ItemDetailContract:
        """
        Queries detailed information about an item by its ID.

        :param item_id: ID of the item to retrieve.
        :type item_id: str | int
        :return: Detailed information of the item.
        :rtype: ItemDetailContract
        """
        raise NotImplementedError('The get_detail_by_id method must be implemented by the item repository.')

    # * method: query_by_ids
    @abstractmethod
    def query_by_ids(self, item_ids: list[str | int]) -> list[ItemContract]:
        """
        Queries items by their IDs.

        :param item_ids: List of item IDs to query.
        :type item_ids: list[str | int]
        :return: List of items matching the provided IDs.
        :rtype: list[ItemContract]
        """
        raise NotImplementedError('The query_by_ids method must be implemented by the item repository.')
    
    # * method: query_subitems
    @abstractmethod
    def query_subitems(self, parent_item_id: str | int) -> List[SubitemContract]:
        """
        Queries subitems for a given parent item ID.

        :param parent_item_id: ID of the parent item for which to query subitems.
        :type parent_item_id: str | int
        :return: List of subitems for the specified parent item.
        :rtype: List[SubitemContract]
        """
        raise NotImplementedError('The query_subitems method must be implemented by the item repository.')

    # * method: update_simple_column_value
    @abstractmethod
    def update_simple_column_value(self, item_id: str | int, board_id: str | int, column_id: str, value: str):
        """
        Updates the value of a simple column for the specified item.

        :param item_id: ID of the item to be updated.
        :type item_id: str | int
        :param board_id: ID of the board to which the item belongs.
        :type board_id: str | int
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param value: New value for the column.
        :type value: str
        """
        raise NotImplementedError('The update_simple_column_value method must be implemented by the item repository.')
    
    # * method: create_subitem
    @abstractmethod
    def create_subitem(self, parent_item_id: str | int, item_name: str) -> Any:
        """
        Creates a subitem under the specified item.

        :param parent_item_id: ID of the parent item under which the subitem will be created.
        :type parent_item_id: str | int
        :param item_name: Name of the subitem to be created.
        :type item_name: str
        :return: Result of the subitem creation operation.
        :rtype: Any
        """
        raise NotImplementedError('The create_subitem method must be implemented by the item repository.')