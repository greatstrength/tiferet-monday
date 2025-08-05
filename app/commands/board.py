# *** imports

# ** core
from typing import List
import json

# ** infra
from tiferet.commands import Command

# ** app
from ..contracts.board import BoardRepository

# *** commands

# ** command: add_column
class AddColumn(Command):

    # ** attribute: board_repo
    board_repo: BoardRepository

    # ** init
    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the AddColumn command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        # Initialize the command with the board repository.
        self.board_repo = board_repo

    # ** method: execute
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

# ** command: list_columns
class ListColumns(Command):
    """
    Command to list all columns in a specified board.
    """

    # ** attribute: board_repo
    board_repo: BoardRepository

    def __init__(self, board_repo: BoardRepository):
        """
        Initializes the ListColumns command with the board repository.

        :param board_repo: The repository for managing board operations.
        :type board_repo: BoardRepository
        """
        self.board_repo = board_repo

    def execute(self, board_id: str | int, **kwargs):
        """
        Lists all columns in the specified board.

        :param board_id: ID of the board from which to list columns.
        :type board_id: str | int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        return self.board_repo.list_columns(board_id=board_id)