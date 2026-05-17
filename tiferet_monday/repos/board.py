"""Tiferet Monday Board Repos"""

# *** imports

# ** core
import json
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.board import BoardService
from ..mappers.column_value import get_column_value_fragments


# *** repos

# ** repo: board_api_proxy
class BoardApiProxy(BoardService, MondayApiProxy):
    '''
    Concrete BoardService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        '''
        Initialize the board API proxy.

        :param monday_api_key: The Monday.com API key.
        :type monday_api_key: str
        '''

        # Initialize the parent proxy.
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: get_boards
    def get_boards(self, ids: List[str] = None, limit: int = 25, page: int = 1) -> List[dict]:
        '''
        Retrieve boards from the Monday.com API.

        :param ids: Optional list of board IDs.
        :type ids: List[str]
        :param limit: Number of boards to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of board data dicts.
        :rtype: List[dict]
        '''

        # Build variables.
        variables = {'limit': limit, 'page': page}
        id_param = ''
        if ids:
            variables['ids'] = [int(i) for i in ids]
            id_param = ', $ids: [ID!]'

        # Execute the query.
        return self.execute_query(
            query=f"""
                query ($limit: Int!, $page: Int!{id_param}) {{
                    boards (limit: $limit, page: $page{', ids: $ids' if ids else ''}) {{
                        id
                        name
                        description
                        board_kind
                        state
                        workspace_id
                        permissions
                        updated_at
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('boards', []),
        )

    # * method: create_board
    def create_board(self, board_name: str, board_kind: str, workspace_id: str = None) -> dict:
        '''
        Create a new board.

        :param board_name: The board name.
        :type board_name: str
        :param board_kind: The board kind.
        :type board_kind: str
        :param workspace_id: Optional workspace ID.
        :type workspace_id: str
        :return: The created board data.
        :rtype: dict
        '''

        # Build variables.
        variables = {
            'boardName': board_name,
            'boardKind': board_kind,
        }
        if workspace_id:
            variables['workspaceId'] = int(workspace_id)

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($boardName: String!, $boardKind: BoardKind!, $workspaceId: ID) {
                    create_board (board_name: $boardName, board_kind: $boardKind, workspace_id: $workspaceId) {
                        id
                        name
                        board_kind
                        state
                    }
                }
            """,
            variables=variables,
            start_node=lambda data: data.get('create_board', {}),
        )

    # * method: archive_board
    def archive_board(self, board_id: str) -> dict:
        '''
        Archive a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: The archived board data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($boardId: ID!) {
                    archive_board (board_id: $boardId) {
                        id
                        state
                    }
                }
            """,
            variables={'boardId': int(board_id)},
            start_node=lambda data: data.get('archive_board', {}),
        )

    # * method: query_columns
    def query_columns(self, board_id: str) -> List[dict]:
        '''
        Query columns in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of column data dicts.
        :rtype: List[dict]
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query ($boardId: [ID!]) {
                    boards (ids: $boardId) {
                        columns {
                            id
                            title
                            type
                            description
                            settings_str
                        }
                    }
                }
            """,
            variables={'boardId': int(board_id)},
            start_node=lambda data: data.get('boards', [{}])[0].get('columns', []),
        )

    # * method: add_column
    def add_column(self, board_id: str, title: str, column_type: str, description: str = None) -> dict:
        '''
        Add a column to a board.

        :param board_id: The board ID.
        :type board_id: str
        :param title: The column title.
        :type title: str
        :param column_type: The column type.
        :type column_type: str
        :param description: Optional description.
        :type description: str
        :return: The created column data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($boardId: ID!, $title: String!, $columnType: ColumnType!, $description: String) {
                    create_column (board_id: $boardId, title: $title, column_type: $columnType, description: $description) {
                        id
                        title
                        type
                        description
                    }
                }
            """,
            variables={
                'boardId': int(board_id),
                'title': title,
                'columnType': column_type,
                'description': description,
            },
            start_node=lambda data: data.get('create_column', {}),
        )

    # * method: query_groups
    def query_groups(self, board_id: str) -> List[dict]:
        '''
        Query groups in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of group data dicts.
        :rtype: List[dict]
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query ($boardId: [ID!]) {
                    boards (ids: $boardId) {
                        groups {
                            id
                            title
                            position
                            color
                        }
                    }
                }
            """,
            variables={'boardId': int(board_id)},
            start_node=lambda data: data.get('boards', [{}])[0].get('groups', []),
        )

    # * method: create_group
    def create_group(self, board_id: str, group_name: str) -> dict:
        '''
        Create a group in a board.

        :param board_id: The board ID.
        :type board_id: str
        :param group_name: The group name.
        :type group_name: str
        :return: The created group data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($boardId: ID!, $groupName: String!) {
                    create_group (board_id: $boardId, group_name: $groupName) {
                        id
                        title
                        position
                        color
                    }
                }
            """,
            variables={
                'boardId': int(board_id),
                'groupName': group_name,
            },
            start_node=lambda data: data.get('create_group', {}),
        )

    # * method: query_items_page
    def query_items_page(self, board_id: str, limit: int = 25) -> List[dict]:
        '''
        Query a page of items from a board.

        :param board_id: The board ID.
        :type board_id: str
        :param limit: Number of items.
        :type limit: int
        :return: List of item data dicts.
        :rtype: List[dict]
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query ($boardId: [ID!], $limit: Int!) {
                    boards (ids: $boardId) {
                        items_page (limit: $limit) {
                            items {
                                id
                                name
                                group { id }
                                board { id }
                            }
                        }
                    }
                }
            """,
            variables={
                'boardId': int(board_id),
                'limit': limit,
            },
            start_node=lambda data: data.get('boards', [{}])[0].get('items_page', {}).get('items', []),
        )

    # * method: create_item
    def create_item(self,
                    board_id: str,
                    item_name: str,
                    group_id: str = None,
                    column_values: Dict[str, Any] = None,
                    create_labels_if_missing: bool = False) -> dict:
        '''
        Create a new item in a board.

        :param board_id: The board ID.
        :type board_id: str
        :param item_name: The item name.
        :type item_name: str
        :param group_id: Optional group ID.
        :type group_id: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :param create_labels_if_missing: Create labels if missing.
        :type create_labels_if_missing: bool
        :return: The created item data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($boardId: ID!, $itemName: String!, $groupId: String, $columnValues: JSON, $createLabels: Boolean) {
                    create_item (board_id: $boardId, item_name: $itemName, group_id: $groupId, column_values: $columnValues, create_labels_if_missing: $createLabels) {
                        id
                        name
                        group { id }
                        board { id }
                    }
                }
            """,
            variables={
                'boardId': int(board_id),
                'itemName': item_name,
                'groupId': group_id,
                'columnValues': json.dumps(column_values) if column_values else None,
                'createLabels': create_labels_if_missing,
            },
            start_node=lambda data: data.get('create_item', {}),
        )
