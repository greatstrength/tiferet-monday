# *** imports

# ** core
from typing import (
    List,
    Dict,
    Any
)
import json

# ** infra
from tiferet import Command

# ** app
from ..contracts.board import (
    ColumnContract,
    GroupContract,
    ItemContract,
    BoardRepository
)

# *** commands

# ** command: add_column
class AddColumn(Command):

    # * attribute: board_repo
    board_repo: BoardRepository

    # * init
    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the AddColumn command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        # Initialize the command with the board repository.
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, title: str, column_type: str, description: str = None, labels: List[str] | str = None, **kwargs):
        """
        Adds a new column to the specified board.

        :param board_id: ID of the board to which the column will be added.
        :type board_id: str | int
        :param title: Title of the new column.
        :type title: str
        :param column_type: Type of the new column (e.g., 'text', 'date').
        :type column_type: str
        :param description: Optional description for the column.
        :type description: str
        :param labels: Optional list of labels for the column, can be a JSON string or a list.
        :type labels: List[str] | str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """

        # Deserialize labels if they are provided as a JSON string.
        if isinstance(labels, str):
            try:
                labels = json.loads(labels)
            except json.JSONDecodeError:
                self.raise_error('INVALID_LABELS', 'Labels must be a valid JSON string or a list.')
        
        # Call the repository method to add the column.
        self.board_repo.add_column(
            board_id=board_id,
            title=title,
            column_type=column_type,
            description=description,
            labels=labels
        )

# ** command: query_columns
class QueryColumns(Command):
    """
    Command to query all columns in a specified board.
    """

    # ** attribute: board_repo
    board_repo: BoardRepository

    # * init
    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the ListColumns command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        # Initialize the command with the board repository.
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, **kwargs) -> List[ColumnContract]:
        """
        Lists all columns in the specified board.

        :param board_id: ID of the board from which to list columns.
        :type board_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        # Call the repository method to query columns from the board.
        return self.board_repo.query_columns(board_id=board_id)
    
# ** command: change_column_metadata
class ChangeColumnMetadata(Command):
    """
    Command to change the metadata of a column in a specified board.
    """

    # ** attribute: board_repo
    board_repo: BoardRepository

    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the ChangeColumnMetadata command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        # Initialize the command with the board repository.
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, column_id: str, title: str = None, description: str = None, **kwargs):
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
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """

        # Set the column_property to description and value to the description parameter by default.
        column_property = "description"
        value = description

        # If title is provided, change the column_property to title and value to the title parameter.
        if title is not None:
            column_property = "title"
            value = title

        # Call the repository method to change the column metadata.
        return self.board_repo.change_column_metadata(
            board_id=board_id,
            column_id=column_id,
            column_property=column_property,
            value=value
        )
    
# ** command: delete_column
class DeleteColumn(Command):
    """
    Command to delete a specified column from a board.
    """

    # * attribute: board_repo
    board_repo: BoardRepository

    # * init
    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the DeleteColumn command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, column_id: str, **kwargs):
        """
        Deletes the specified column from the board.

        :param board_id: ID of the board from which the column will be deleted.
        :type board_id: str | int
        :param column_id: ID of the column to be deleted.
        :type column_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        return self.board_repo.delete_column(board_id=board_id, column_id=column_id)
    
# ** command: query_groups
class QueryGroups(Command):
    """
    Command to query groups in a specified board.
    """

    # * attribute: board_repo
    board_repo: BoardRepository

    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the QueryGroups command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, **kwargs) -> List[GroupContract]:
        """
        Queries groups in the specified board.

        :param board_id: ID of the board from which to query groups.
        :type board_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: List of groups in the specified board.
        :rtype: List[Group]
        """
        return self.board_repo.query_groups(board_id=board_id)
    
# ** command: query_items_page
class QueryItemsPage(Command):
    """
    Command to query a paginated list of items in a specified board.
    """

    # * attribute: board_repo
    board_repo: BoardRepository

    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the QueryItemsPage command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        self.board_repo = board_repo

    # * method: execute
    def execute(self, board_id: str | int, limit: int = 25, **kwargs) -> List[ItemContract]:
        """
        Queries a paginated list of items in the specified board.

        :param board_id: ID of the board from which to query items.
        :type board_id: str | int
        :param limit: Number of items to retrieve per page (default is 25).
        :type limit: int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: List of items in the specified board.
        :rtype: List[Item]
        """
        return self.board_repo.query_items_page(board_id=board_id, limit=limit)
    
# ** command: create_item
class CreateItem(Command):
    """
    Command to create a new item in a specified board.
    """

    # * attribute: board_repo
    board_repo: BoardRepository

    # * init
    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the CreateItem command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        self.board_repo = board_repo

    # * method: execute
    def execute(self, 
            board_id: str | int,
            item_name: str,
            group_id: str = None,
            column_values: Dict[str, Any] = {},
            create_labels_if_missing: bool = False,
            **kwargs):
        """
        Creates a new item in the specified board.

        :param board_id: ID of the board where the item will be created.
        :type board_id: str | int
        :param item_name: Name of the new item.
        :type item_name: str
        :param group_id: Optional ID of the group where the item will be created.
        :type group_id: str | None
        :param column_values: Optional dictionary of column values to set for the new item.
        :type column_values: Dict[str, Any]
        :param create_labels_if_missing: Whether to create labels if they are missing (default is False).
        :type create_labels_if_missing: bool
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        return self.board_repo.create_item(
            board_id=board_id, 
            item_name=item_name,
            group_id=group_id,
            column_values=column_values,
            create_labels_if_missing=create_labels_if_missing
        )