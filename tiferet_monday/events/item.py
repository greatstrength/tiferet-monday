"""Tiferet Monday Item Events"""

# *** imports

# ** core
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayEvent
from ..interfaces.item import ItemService
from ..domain.item import Item


# *** events

# ** event: get_items
class GetItems(MondayEvent):
    '''
    Event to retrieve items by IDs.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the GetItems event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_ids: List[str], **kwargs) -> List[dict]:
        '''
        Retrieve items by their IDs. Returns raw dicts for context wrapping.

        :param item_ids: List of item IDs.
        :type item_ids: List[str]
        :return: List of item data dicts.
        :rtype: List[dict]
        '''

        # Query items from the service.
        return self.item_service.query_items_by_ids(item_ids=item_ids)


# ** event: get_item_detail
class GetItemDetail(MondayEvent):
    '''
    Event to retrieve detailed item information including column values.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the GetItemDetail event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_id: str, **kwargs) -> Optional[dict]:
        '''
        Retrieve item detail. Returns raw dict for context wrapping.

        :param item_id: The item ID.
        :type item_id: str
        :return: The item detail data, or None.
        :rtype: Optional[dict]
        '''

        # Query item detail from the service.
        return self.item_service.query_item_detail(item_id=item_id)


# ** event: query_column_values
class QueryColumnValues(MondayEvent):
    '''
    Event to query column values for an item.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the QueryColumnValues event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_id: str, column_ids: List[str] = None, **kwargs) -> List[dict]:
        '''
        Query column values for an item.

        :param item_id: The item ID.
        :type item_id: str
        :param column_ids: Optional column IDs to filter.
        :type column_ids: List[str]
        :return: List of column value data dicts.
        :rtype: List[dict]
        '''

        # Query column values from the service.
        return self.item_service.query_column_values(
            item_id=item_id,
            column_ids=column_ids,
        )


# ** event: change_column_value
class ChangeColumnValue(MondayEvent):
    '''
    Event to change a simple column value on an item.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the ChangeColumnValue event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_id: str, board_id: str, column_id: str, value: str, **kwargs) -> dict:
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

        # Change the column value via the service.
        return self.item_service.change_simple_column_value(
            item_id=item_id,
            board_id=board_id,
            column_id=column_id,
            value=value,
        )


# ** event: create_subitem
class CreateSubitem(MondayEvent):
    '''
    Event to create a subitem under a parent item.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the CreateSubitem event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, parent_item_id: str, item_name: str, column_values: Dict[str, Any] = None, **kwargs) -> dict:
        '''
        Create a subitem. Returns raw dict for context wrapping.

        :param parent_item_id: The parent item ID.
        :type parent_item_id: str
        :param item_name: The subitem name.
        :type item_name: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :return: The created subitem data.
        :rtype: dict
        '''

        # Create the subitem via the service.
        return self.item_service.create_subitem(
            parent_item_id=parent_item_id,
            item_name=item_name,
            column_values=column_values,
        )


# ** event: archive_item
class ArchiveItem(MondayEvent):
    '''
    Event to archive an item.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the ArchiveItem event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_id: str, **kwargs) -> dict:
        '''
        Archive an item.

        :param item_id: The item ID.
        :type item_id: str
        :return: The archived item data.
        :rtype: dict
        '''

        # Archive the item via the service.
        return self.item_service.archive_item(item_id=item_id)


# ** event: create_item_update
class CreateItemUpdate(MondayEvent):
    '''
    Event to create an update (comment) on an item.
    '''

    # * attribute: item_service
    item_service: ItemService

    # * init
    def __init__(self, item_service: ItemService):
        '''
        Initialize the CreateItemUpdate event.

        :param item_service: The item service.
        :type item_service: ItemService
        '''

        # Set the item service dependency.
        self.item_service = item_service

    # * method: execute
    def execute(self, item_id: str, body: str, **kwargs) -> dict:
        '''
        Create an update on an item.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body text.
        :type body: str
        :return: The created update data.
        :rtype: dict
        '''

        # Create the update via the service.
        return self.item_service.create_update(item_id=item_id, body=body)
