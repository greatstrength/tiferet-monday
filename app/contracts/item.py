# *** imports

# ** infra
from tiferet.contracts import Repository, abstractmethod

# *** contracts

# ** contract: item_repo
class ItemRepository(Repository):
    """
    Repository for managing item-related operations.
    """

    @abstractmethod
    def update_simple_column_value(self, item_id: str | int, column_id: str, value: str):
        """
        Updates the value of a simple column for the specified item.

        :param item_id: ID of the item to be updated.
        :type item_id: str | int
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param value: New value for the column.
        :type value: str
        """

        raise NotImplementedError('The update_simple_column_value method must be implemented by the item repository.')