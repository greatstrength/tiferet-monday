# *** imports

# ** core
from typing import (
    List,
    Dict,
    Any,
    Tuple
)

# ** infra
from tiferet import Command

# ** app
from tiferet_monday.contracts import (
    ItemContract,
    ItemDetailContract,
    ColumnValueContract,
    ItemRepository
)

# *** commands

# ** command: query_detail_by_id
class QueryDetailById(Command):
    """
    Command for querying detailed information about an item by its ID.
    """

    # ** attribute: item_repo
    item_repo: ItemRepository

    # ** init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the QueryDetailById command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # ** method: execute
    def execute(self, item_id: str | int, **kwargs) -> ItemDetailContract:
        """
        Executes the command to query detailed information about an item by its ID.

        :param item_id: ID of the item to retrieve details for.
        :type item_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: Detailed information about the item.
        :rtype: ItemDetailContract
        """
        
        # Call the repository method to query details by ID.
        return self.item_repo.query_detail_by_id(item_id=item_id)

# ** command: query_by_ids
class QueryByIds(Command):
    """
    Command for querying items by their IDs.
    """

    # * attribute: item_repo
    item_repo: ItemRepository

    # * init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the QueryByIds command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # * method: execute
    def execute(self, item_ids: List[str | int], **kwargs) -> List[ItemContract]:
        """
        Executes the command to query items by their IDs.

        :param item_ids: List of IDs of the items to be queried.
        :type item_ids: List[str | int]
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: List of items matching the provided IDs.
        :rtype: list[Item]
        """

        # Call the repository method to query items by their IDs.
        return self.item_repo.query_by_ids(item_ids=item_ids)
    
# ** command: query_column_value
class QueryColumnValues(Command):
    """
    Command for querying column values of a specified item.
    """
    
    # * attribute: item_repo
    item_repo: ItemRepository

    # * init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the QueryColumnValues command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # * method: execute
    def execute(self, item_id: str | int, column_ids: List[str] = [], **kwargs) -> Tuple[ColumnValueContract]:
        """
        Executes the command to query column values of the specified item.

        :param item_id: ID of the item whose column values will be queried.
        :type item_id: str | int
        :param column_ids: Optional list of column IDs to filter the results.
        :type column_ids: List[str]
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: Tuple of column values for the specified item.
        :rtype: Tuple[ColumnValue]
        """
        
        # Call the repository method to query column values.
        column_value_map = {cv.id: cv for cv in self.item_repo.query_column_values(item_id=item_id, column_ids=column_ids)}

        # Return the column values in the order of the requested column IDs.
        return tuple(column_value_map[cid] for cid in column_ids if cid in column_value_map)
    
# ** command: query_subitems
class QuerySubitems(Command):
    """
    Command for querying subitems of a specified parent item.
    """

    # * attribute: item_repo
    item_repo: ItemRepository

    # * init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the QuerySubitems command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # * method: execute
    def execute(self, parent_item_id: str | int, **kwargs) -> List[ItemContract]:
        """
        Executes the command to query subitems of the specified parent item.

        :param parent_item_id: ID of the parent item whose subitems will be queried.
        :type parent_item_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: List of subitems under the specified parent item.
        :rtype: list[Item]
        """
        
        # Call the repository method to query subitems.
        return self.item_repo.query_subitems(parent_item_id=parent_item_id)

# ** command: update_simple_column_value
class UpdateSimpleColumnValue(Command):
    """
    Command for updating the value of a simple column for a specified item.
    """

    # ** attribute: item_repo
    item_repo: ItemRepository

    # * init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the UpdateSimpleColumnValue command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # * method: execute
    def execute(self, board_id: str, item_id: str, column_id: str, value: str, **kwargs) -> ItemContract:
        """
        Executes the command to update the value of a simple column for the specified item.

        :param board_id: The ID of the board to which the item belongs.
        :type board_id: str
        :param item_id: The ID of the item to be updated.
        :type item_id: str
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param value: New value for the column.
        :type value: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: Result of the update operation.
        :rtype: Dict[str, Any]
        """
        
        # Call the repository method to update the column value.
        return self.item_repo.update_simple_column_value(
            item_id=item_id, 
            board_id=board_id, 
            column_id=column_id, 
            value=value
        )
    
# ** command: create_subitem
class CreateSubitem(Command):
    """
    Command for creating a subitem under a specified item.
    """

    # * attribute: item_repo
    item_repo: ItemRepository

    # * init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the CreateSubitem command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # * method: execute
    def execute(self, parent_item_id: str | int, item_name: str, column_values: Dict[str, Any] = {}, **kwargs) -> ItemContract:
        """
        Executes the command to create a subitem under the specified parent item.

        :param parent_item_id: ID of the parent item under which the subitem will be created.
        :type parent_item_id: str | int
        :param item_name: Name of the subitem to be created.
        :type item_name: str
        :param column_values: Optional dictionary of column values to set for the new subitem.
        :type column_values: Dict[str, Any]
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The created subitem.
        :rtype: ItemContract
        """
        
        # Call the repository method to create the subitem.
        return self.item_repo.create_subitem(
            parent_item_id=parent_item_id,
            item_name=item_name,
            column_values=column_values
        )