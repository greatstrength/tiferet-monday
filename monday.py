from typing import Dict, Any
import json
from monday_app import app


def create_item(
        board_id: str,
        item_name: str,
        group_id: str = None,
        column_values: Dict[str, Any] = {},
        create_labels_if_missing: bool = False
    ):
    """
    Create a new item on the specified board.

    :param board_id: The ID of the board where the item will be created.
    :type board_id: str
    :param item_name: The name of the new item.
    :type item_name: str
    :param group_id: The ID of the group where the item will be created. If None, the default group is used.
    :type group_id: str
    :param column_values: A dictionary of column values to set for the new item.
    :type column_values: Dict[str, Any]
    :param create_labels_if_missing: Whether to create labels if they are missing (default is False).
    :type create_labels_if_missing: bool
    :return: The created ItemDetail object.
    :rtype: ItemDetail
    """

    data = dict(
        board_id=board_id,
        item_name=item_name,
        group_id=group_id,
        column_values=column_values,
        create_labels_if_missing=create_labels_if_missing
    )

    return app.run('board.create_item', data=data)


def update_simple_column_value(item_id: str, column_id: str, value: str):
    """
    Update the value of a simple column for the specified item.
    
    :param item_id: The ID of the item to be updated.
    :type item_id: str
    :param column_id: The ID of the column to be updated.
    :type column_id: str
    :param value: The new value for the column.
    :type value: str
    :return: Result of the update operation.
    :rtype: Dict[str, Any]
    """

    data = dict(
        item_id=item_id,
        column_id=column_id,
        value=value
    )

    app.run('item.update_simple_column_value', data=data)


def query_columns(board_id: str):
    """
    Query the columns of the specified board.

    :param board_id: The ID of the board whose columns are to be queried.
    :type board_id: str
    :return: List of columns in the specified board.
    :rtype: List[Column]
    """

    data = dict(
        board_id=board_id
    )

    return app.run('board.query_columns', data=data)

def query_items_page(board_id: str, limit: int = 25, page: int = 1):
    """
    Query a page of items from the specified board.

    :param board_id: The ID of the board whose items are to be queried.
    :type board_id: str
    :param limit: The number of items to retrieve per page (default is 25).
    :type limit: int
    :param page: The page number to retrieve (default is 1).
    :type page: int
    :return: A page of items from the specified board.
    :rtype: ItemPage
    """

    data = dict(
        board_id=board_id,
        limit=limit,
        page=page
    )

    return app.run('board.query_items_page', data=data)