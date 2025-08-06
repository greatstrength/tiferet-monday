# *** imports

# ** core
from typing import Dict, Any

# ** infra
from tiferet.commands import Command

# ** app
from ..contracts.item import ItemRepository

# *** commands

# ** command: update_simple_column_value
class UpdateSimpleColumnValue(Command):
    """
    Command for updating the value of a simple column for a specified item.
    """

    # ** attribute: item_repo
    item_repo: ItemRepository

    # ** init
    def __init__(self, item_repo: ItemRepository):
        """
        Initializes the UpdateSimpleColumnValue command with the item repository.

        :param item_repo: The repository for managing item operations.
        :type item_repo: ItemRepository
        """
        self.item_repo = item_repo

    # ** method: execute
    def execute(self, item_id: str | int, column_id: str, value: str, **kwargs) -> Dict[str, Any]:
        """
        Executes the command to update the value of a simple column for the specified item.

        :param item_id: ID of the item to be updated.
        :type item_id: str | int
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
        return self.item_repo.update_simple_column_value(item_id=item_id, column_id=column_id, value=value)