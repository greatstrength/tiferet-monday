# *** imports

# ** core
from abc import abstractmethod
from typing import (
    List,
    Dict,
    Any
)

# ** infra
from tiferet import (
    ModelContract,
    Repository
)

# ** app
from .item import (
    ItemContract,
)

# *** contracts

# ** contract: column
class ColumnContract(ModelContract):
    """
    Represents a column in a Monday.com board.
    """

    # * attribute: id
    id: str

    # * attribute: title
    name: str

    # * attribute: description
    description: str

    # * attribute: settings_str
    settings_str: str

# ** contract: group
class GroupContract(ModelContract):
    """
    Represents a group in a Monday.com board.
    """

    # * attribute: id
    id: str

    # * attribute: name
    name: str

    # * attribute: position
    position: str

# ** contract: board_repo
class BoardRepository(Repository):
    """
    Repository for managing board-related operations.
    """

    # * method: add_column
    @abstractmethod
    def add_column(self, board_id: str | int, column_name: str, column_type: str, description: str = None, labels: List[str] = None):
        """
        Adds a new column to the specified board.

        :param board_id: ID of the board to which the column will be added.
        :type board_id: str | int
        :param column_name: Name of the new column.
        :type column_name: str
        :param column_type: Type of the new column (e.g., 'text', 'date').
        :type column_type: str
        :param description: Optional description for the column.
        :type description: str
        :param labels: Optional list of labels for the column.
        :type labels: List[str]
        """
        raise NotImplementedError('The add_column method must be implemented by the board repository.')
    
    # * method: query_columns
    @abstractmethod
    def query_columns(self, board_id: str | int) -> List[ColumnContract]:
        """
        Queries all columns in the specified board.

        :param board_id: ID of the board from which to list columns.
        :type board_id: str | int
        :return: List of columns in the specified board.
        :rtype: List[ColumnContract]
        """
        raise NotImplementedError('The list_columns method must be implemented by the board repository.')
    
    # * change_column_metadata
    @abstractmethod
    def change_column_metadata(self, board_id: str | int, column_id: str, title: str = None, description: str = None):
        """
        Changes the metadata of a column in the specified board.

        :param board_id: ID of the board containing the column.
        :type board_id: str | int
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param title: New title for the column.
        :type title: str
        :param description: New description for the column.
        :type description: str
        """
        raise NotImplementedError('The change_column_metadata method must be implemented by the board repository.')
    
    # * method: delete_column
    @abstractmethod
    def delete_column(self, board_id: str | int, column_id: str):
        """
        Deletes a column from the specified board.

        :param board_id: ID of the board from which the column will be deleted.
        :type board_id: str | int
        :param column_id: ID of the column to be deleted.
        :type column_id: str
        """
        raise NotImplementedError('The delete_column method must be implemented by the board repository.')
    
    # * method: query_groups
    @abstractmethod
    def query_groups(self, board_id: str | int) -> List[GroupContract]:
        """
        Queries all groups in the specified board.

        :param board_id: ID of the board from which to query groups.
        :type board_id: str | int
        :return: List of groups in the board.
        :rtype: List[GroupContract]
        """
        raise NotImplementedError('The query_groups method must be implemented by the board repository.')
    
    # * method: query_items_page
    @abstractmethod
    def query_items_page(self, board_id: str | int, limit: int = 25) -> List[ItemContract]:
        """
        Queries a page of items from the specified board.

        :param board_id: ID of the board from which to query items.
        :type board_id: str | int
        :param limit: Number of items to retrieve in the page.
        :type limit: int
        :return: List of items in the specified board.
        :rtype: List[ItemContract]
        """
        raise NotImplementedError('The query_items_page method must be implemented by the board repository.')

    # * method: create_item
    @abstractmethod
    def create_item(self,
        board_id: str | int,
        item_name: str,
        group_id: str = None,
        column_values: Dict[str, Any] = {},
        create_labels_if_missing: bool = False
    ) -> ItemContract:
        """
        Creates a new item in the specified board.

        :param board_id: ID of the board in which the item will be created.
        :type board_id: str | int
        :param item_name: Name of the item to be created.
        :type item_name: str
        :param group_id: Optional ID of the group under which the item will be created.
        :type group_id: str
        :param column_values: Optional dictionary of column values to set for the new item.
        :type column_values: Dict[str, Any]
        :param create_labels_if_missing: Whether to create labels if they are missing (default is False).
        :type create_labels_if_missing: bool
        :return: The created item.
        :rtype: ItemContract
        """
        raise NotImplementedError('The create_item method must be implemented by the board repository.')
