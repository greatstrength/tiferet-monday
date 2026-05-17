"""Tiferet Monday Item Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: item_service
class ItemService(MondayService):
    '''
    Service interface for item-related Monday.com API operations.
    '''

    # * method: query_items_by_ids
    @abstractmethod
    def query_items_by_ids(self, item_ids: List[str]) -> List[dict]:
        '''
        Query items by their IDs.

        :param item_ids: List of item IDs.
        :type item_ids: List[str]
        :return: List of item data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: query_item_detail
    @abstractmethod
    def query_item_detail(self, item_id: str) -> Optional[dict]:
        '''
        Query detailed information about an item including column values.

        :param item_id: The item ID.
        :type item_id: str
        :return: Item detail data dict, or None.
        :rtype: Optional[dict]
        '''
        raise NotImplementedError()

    # * method: query_column_values
    @abstractmethod
    def query_column_values(self, item_id: str, column_ids: List[str] = None) -> List[dict]:
        '''
        Query column values for an item.

        :param item_id: The item ID.
        :type item_id: str
        :param column_ids: Optional list of column IDs to filter.
        :type column_ids: List[str]
        :return: List of column value data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: query_subitems
    @abstractmethod
    def query_subitems(self, parent_item_id: str) -> List[dict]:
        '''
        Query subitems of a parent item.

        :param parent_item_id: The parent item ID.
        :type parent_item_id: str
        :return: List of subitem data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: change_simple_column_value
    @abstractmethod
    def change_simple_column_value(self, item_id: str, board_id: str, column_id: str, value: str) -> dict:
        '''
        Change a simple column value.

        :param item_id: The item ID.
        :type item_id: str
        :param board_id: The board ID.
        :type board_id: str
        :param column_id: The column ID.
        :type column_id: str
        :param value: The new value.
        :type value: str
        :return: The updated item data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: change_multiple_column_values
    @abstractmethod
    def change_multiple_column_values(self, item_id: str, board_id: str, column_values: Dict[str, Any]) -> dict:
        '''
        Change multiple column values at once.

        :param item_id: The item ID.
        :type item_id: str
        :param board_id: The board ID.
        :type board_id: str
        :param column_values: Column value mappings.
        :type column_values: Dict[str, Any]
        :return: The updated item data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: create_subitem
    @abstractmethod
    def create_subitem(self, parent_item_id: str, item_name: str, column_values: Dict[str, Any] = None) -> dict:
        '''
        Create a subitem under a parent item.

        :param parent_item_id: The parent item ID.
        :type parent_item_id: str
        :param item_name: The subitem name.
        :type item_name: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :return: The created subitem data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: archive_item
    @abstractmethod
    def archive_item(self, item_id: str) -> dict:
        '''
        Archive an item.

        :param item_id: The item ID.
        :type item_id: str
        :return: The archived item data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: delete_item
    @abstractmethod
    def delete_item(self, item_id: str) -> dict:
        '''
        Delete an item.

        :param item_id: The item ID.
        :type item_id: str
        :return: The deleted item data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: move_item_to_group
    @abstractmethod
    def move_item_to_group(self, item_id: str, group_id: str) -> dict:
        '''
        Move an item to a different group.

        :param item_id: The item ID.
        :type item_id: str
        :param group_id: The target group ID.
        :type group_id: str
        :return: The moved item data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: create_update
    @abstractmethod
    def create_update(self, item_id: str, body: str) -> dict:
        '''
        Create an update (comment) on an item.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body text.
        :type body: str
        :return: The created update data.
        :rtype: dict
        '''
        raise NotImplementedError()
