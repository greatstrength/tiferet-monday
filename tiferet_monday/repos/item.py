"""Tiferet Monday Item Repos"""

# *** imports

# ** core
import json
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.item import ItemService
from ..mappers.column_value import get_column_value_fragments


# *** repos

# ** repo: item_api_proxy
class ItemApiProxy(ItemService, MondayApiProxy):
    '''
    Concrete ItemService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        '''
        Initialize the item API proxy.

        :param monday_api_key: The Monday.com API key.
        :type monday_api_key: str
        '''

        # Initialize the parent proxy.
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: _build_column_value_fragments
    def _build_column_value_fragments(self) -> str:
        '''
        Build the column_values field with all registered inline fragments.

        :return: The GraphQL column_values field string.
        :rtype: str
        '''

        # Collect all registered fragments.
        fragments = get_column_value_fragments()
        fragments_str = '\n                            '.join(fragments)

        # Return the column_values field with fragments.
        return f"""
                        column_values {{
                            id
                            column {{ title description settings_str }}
                            type
                            text
                            value
                            {fragments_str}
                        }}"""

    # * method: query_items_by_ids
    def query_items_by_ids(self, item_ids: List[str]) -> List[dict]:
        '''
        Query items by their IDs.

        :param item_ids: List of item IDs.
        :type item_ids: List[str]
        :return: List of item data dicts.
        :rtype: List[dict]
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query ($itemIds: [ID!]) {
                    items (ids: $itemIds) {
                        id
                        name
                        board { id }
                        group { id }
                        state
                        created_at
                        updated_at
                    }
                }
            """,
            variables={'itemIds': [int(i) for i in item_ids]},
            start_node=lambda data: data.get('items', []),
        )

    # * method: query_item_detail
    def query_item_detail(self, item_id: str) -> Optional[dict]:
        '''
        Query detailed item information including column values.

        :param item_id: The item ID.
        :type item_id: str
        :return: Item detail data dict, or None.
        :rtype: Optional[dict]
        '''

        # Build the column values fragment.
        cv_field = self._build_column_value_fragments()

        # Execute the query.
        data = self.execute_query(
            query=f"""
                query ($itemId: ID!) {{
                    items (ids: [$itemId]) {{
                        id
                        name
                        board {{ id }}
                        group {{ id }}
                        parent_item {{ id }}
                        state
                        created_at
                        updated_at
                        {cv_field}
                    }}
                }}
            """,
            variables={'itemId': int(item_id)},
            start_node=lambda data: data.get('items', []),
        )

        # Return None if not found.
        if not data:
            return None

        # Return the first item.
        return data[0]

    # * method: query_column_values
    def query_column_values(self, item_id: str, column_ids: List[str] = None) -> List[dict]:
        '''
        Query column values for an item.

        :param item_id: The item ID.
        :type item_id: str
        :param column_ids: Optional column IDs to filter.
        :type column_ids: List[str]
        :return: List of column value data dicts.
        :rtype: List[dict]
        '''

        # Build the column values fragment with all registered inline fragments.
        fragments_str = '\n                            '.join(get_column_value_fragments())

        # Execute the query.
        return self.execute_query(
            query=f"""
                query ($itemId: ID!, $columnIds: [String!]) {{
                    items (ids: [$itemId]) {{
                        column_values (ids: $columnIds) {{
                            id
                            column {{ title description settings_str }}
                            type
                            text
                            value
                            {fragments_str}
                        }}
                    }}
                }}
            """,
            variables={
                'itemId': int(item_id),
                'columnIds': column_ids,
            },
            start_node=lambda data: data.get('items', [{}])[0].get('column_values', []),
        )

    # * method: query_subitems
    def query_subitems(self, parent_item_id: str) -> List[dict]:
        '''
        Query subitems of a parent item.

        :param parent_item_id: The parent item ID.
        :type parent_item_id: str
        :return: List of subitem data dicts.
        :rtype: List[dict]
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query ($parentItemId: [ID!]!) {
                    items (ids: $parentItemId) {
                        subitems {
                            id
                            name
                            board { id }
                            group { id }
                        }
                    }
                }
            """,
            variables={'parentItemId': int(parent_item_id)},
            start_node=lambda data: data.get('items', [{}])[0].get('subitems', []),
        )

    # * method: change_simple_column_value
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

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!, $boardId: ID!, $columnId: String!, $value: String!) {
                    change_simple_column_value (item_id: $itemId, board_id: $boardId, column_id: $columnId, value: $value) {
                        id
                        name
                        board { id }
                    }
                }
            """,
            variables={
                'itemId': int(item_id),
                'boardId': int(board_id),
                'columnId': column_id,
                'value': value,
            },
            start_node=lambda data: data.get('change_simple_column_value', {}),
        )

    # * method: change_multiple_column_values
    def change_multiple_column_values(self, item_id: str, board_id: str, column_values: Dict[str, Any]) -> dict:
        '''
        Change multiple column values.

        :param item_id: The item ID.
        :type item_id: str
        :param board_id: The board ID.
        :type board_id: str
        :param column_values: Column value mappings.
        :type column_values: Dict[str, Any]
        :return: The updated item data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!, $boardId: ID!, $columnValues: JSON!) {
                    change_multiple_column_values (item_id: $itemId, board_id: $boardId, column_values: $columnValues) {
                        id
                        name
                        board { id }
                    }
                }
            """,
            variables={
                'itemId': int(item_id),
                'boardId': int(board_id),
                'columnValues': json.dumps(column_values),
            },
            start_node=lambda data: data.get('change_multiple_column_values', {}),
        )

    # * method: create_subitem
    def create_subitem(self, parent_item_id: str, item_name: str, column_values: Dict[str, Any] = None) -> dict:
        '''
        Create a subitem.

        :param parent_item_id: The parent item ID.
        :type parent_item_id: str
        :param item_name: The subitem name.
        :type item_name: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :return: The created subitem data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($parentItemId: ID!, $itemName: String!, $columnValues: JSON) {
                    create_subitem (parent_item_id: $parentItemId, item_name: $itemName, column_values: $columnValues) {
                        id
                        name
                        board { id }
                    }
                }
            """,
            variables={
                'parentItemId': int(parent_item_id),
                'itemName': item_name,
                'columnValues': json.dumps(column_values) if column_values else None,
            },
            start_node=lambda data: data.get('create_subitem', {}),
        )

    # * method: archive_item
    def archive_item(self, item_id: str) -> dict:
        '''
        Archive an item.

        :param item_id: The item ID.
        :type item_id: str
        :return: The archived item data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!) {
                    archive_item (item_id: $itemId) { id }
                }
            """,
            variables={'itemId': int(item_id)},
            start_node=lambda data: data.get('archive_item', {}),
        )

    # * method: delete_item
    def delete_item(self, item_id: str) -> dict:
        '''
        Delete an item.

        :param item_id: The item ID.
        :type item_id: str
        :return: The deleted item data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!) {
                    delete_item (item_id: $itemId) { id }
                }
            """,
            variables={'itemId': int(item_id)},
            start_node=lambda data: data.get('delete_item', {}),
        )

    # * method: move_item_to_group
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

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!, $groupId: String!) {
                    move_item_to_group (item_id: $itemId, group_id: $groupId) {
                        id
                        name
                        group { id }
                    }
                }
            """,
            variables={
                'itemId': int(item_id),
                'groupId': group_id,
            },
            start_node=lambda data: data.get('move_item_to_group', {}),
        )

    # * method: create_update
    def create_update(self, item_id: str, body: str) -> dict:
        '''
        Create an update on an item.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body.
        :type body: str
        :return: The created update data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($itemId: ID!, $body: String!) {
                    create_update (item_id: $itemId, body: $body) {
                        id
                        body
                        creator_id
                    }
                }
            """,
            variables={
                'itemId': int(item_id),
                'body': body,
            },
            start_node=lambda data: data.get('create_update', {}),
        )
