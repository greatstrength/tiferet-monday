"""Tiferet Monday Item Context"""

# *** imports

# ** core
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayContext
from ..domain.item import Item, Update
from ..domain.column_value import ColumnValue
from ..mappers.column_value import ColumnValueType
from ..events.item import (
    GetItemDetail,
    QueryColumnValues,
    ChangeColumnValue,
    CreateSubitem,
    ArchiveItem,
    CreateItemUpdate,
)

# ** infra
import pydantic


# *** contexts

# ** context: item_context
class ItemContext(MondayContext):
    '''
    Context-as-client for a Monday.com item.
    Wraps an Item domain object and exposes domain behaviors as methods.
    Each method triggers a domain event via injected services.
    '''

    # * attribute: _item
    _item: Item

    # * init
    def __init__(self, item: Item, api_key: str, **kwargs):
        '''
        Initialize the item context.

        :param item: The item domain object.
        :type item: Item
        :param api_key: The Monday.com API key.
        :type api_key: str
        '''

        # Initialize the parent context.
        super().__init__(api_key, **kwargs)

        # Set the item domain object.
        self._item = item

    # * method: from_api_data (static)
    @staticmethod
    def from_api_data(data: dict, api_key: str, **kwargs) -> 'ItemContext':
        '''
        Create an ItemContext from raw Monday.com API response data.
        Normalizes nested board/group structures into flat fields.

        :param data: The raw API data dict.
        :type data: dict
        :param api_key: The Monday.com API key.
        :type api_key: str
        :return: The ItemContext.
        :rtype: ItemContext
        '''

        # Normalize nested board/group into flat fields.
        normalized = dict(data)
        if 'board' in normalized and isinstance(normalized['board'], dict):
            normalized['board_id'] = str(normalized.pop('board', {}).get('id', ''))
        if 'group' in normalized and isinstance(normalized['group'], dict):
            normalized['group_id'] = str(normalized.pop('group', {}).get('id', ''))
        if 'parent_item' in normalized and isinstance(normalized['parent_item'], dict):
            normalized['parent_item_id'] = str(normalized.pop('parent_item', {}).get('id', ''))

        # Create the item domain object.
        item = Item.model_validate(normalized)

        # Return the item context.
        return ItemContext(item=item, api_key=api_key, **kwargs)

    # * property: id
    @property
    def id(self) -> str:
        '''The item ID.'''
        return self._item.id

    # * property: name
    @property
    def name(self) -> str:
        '''The item name.'''
        return self._item.name

    # * property: board_id
    @property
    def board_id(self) -> Optional[str]:
        '''The board ID this item belongs to.'''
        return self._item.board_id

    # * property: group_id
    @property
    def group_id(self) -> Optional[str]:
        '''The group ID this item belongs to.'''
        return self._item.group_id

    # * property: state
    @property
    def state(self) -> Optional[str]:
        '''The item state.'''
        return self._item.state

    # * method: get_column_values
    def get_column_values(self, column_ids: List[str] = None) -> list:
        '''
        Query column values for this item.
        Returns typed ColumnValue subclasses via discriminated union dispatch.

        :param column_ids: Optional column IDs to filter.
        :type column_ids: List[str]
        :return: List of typed ColumnValue objects.
        :rtype: list[ColumnValue]
        '''

        # Execute the query column values event.
        event = QueryColumnValues(item_service=self._item_service)
        data_list = event.execute(item_id=self.id, column_ids=column_ids)

        # Normalize column title from nested column object.
        normalized = []
        for cv_data in data_list:
            cv = dict(cv_data)
            if 'column' in cv and isinstance(cv['column'], dict):
                col = cv.pop('column')
                cv.setdefault('name', col.get('title', ''))
                cv.setdefault('description', col.get('description'))
                cv.setdefault('settings_str', col.get('settings_str'))
            normalized.append(cv)

        # Use a temporary Pydantic model to leverage discriminated union dispatch.
        class _Wrapper(pydantic.BaseModel):
            model_config = pydantic.ConfigDict(extra='ignore')
            cvs: List[ColumnValueType] = []

        wrapper = _Wrapper.model_validate({'cvs': normalized})
        return list(wrapper.cvs)

    # * method: change_column_value
    def change_column_value(self, column_id: str, value: str) -> 'ItemContext':
        '''
        Change a simple column value on this item. Returns a refreshed ItemContext.

        :param column_id: The column ID.
        :type column_id: str
        :param value: The new value.
        :type value: str
        :return: The updated ItemContext.
        :rtype: ItemContext
        '''

        # Execute the change column value event.
        event = ChangeColumnValue(item_service=self._item_service)
        data = event.execute(
            item_id=self.id,
            board_id=self.board_id,
            column_id=column_id,
            value=value,
        )

        # Return a refreshed ItemContext.
        return ItemContext.from_api_data(
            data, api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
        )

    # * method: create_subitem
    def create_subitem(self, item_name: str, column_values: Dict[str, Any] = None) -> 'ItemContext':
        '''
        Create a subitem under this item. Returns the new ItemContext.

        :param item_name: The subitem name.
        :type item_name: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :return: The created ItemContext.
        :rtype: ItemContext
        '''

        # Execute the create subitem event.
        event = CreateSubitem(item_service=self._item_service)
        data = event.execute(
            parent_item_id=self.id,
            item_name=item_name,
            column_values=column_values,
        )

        # Return the new ItemContext.
        return ItemContext.from_api_data(
            data, api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
        )

    # * method: add_update
    def add_update(self, body: str) -> Update:
        '''
        Create an update (comment) on this item.

        :param body: The update body text.
        :type body: str
        :return: The created Update domain object.
        :rtype: Update
        '''

        # Execute the create item update event.
        event = CreateItemUpdate(item_service=self._item_service)
        data = event.execute(item_id=self.id, body=body)

        # Return as Update domain object.
        return Update.model_validate(data)

    # * method: archive
    def archive(self) -> 'ItemContext':
        '''
        Archive this item.

        :return: The archived ItemContext.
        :rtype: ItemContext
        '''

        # Execute the archive item event.
        event = ArchiveItem(item_service=self._item_service)
        data = event.execute(item_id=self.id)

        # Return a refreshed ItemContext.
        return ItemContext.from_api_data(
            data, api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
        )

    # * method: __repr__
    def __repr__(self) -> str:
        '''String representation.'''
        return f'ItemContext(id={self.id}, name={self.name})'
