"""Tiferet Monday Board Context"""

# *** imports

# ** core
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayContext
from ..domain.board import Board, Column, Group
from ..events.board import (
    GetBoard,
    CreateBoard,
    QueryBoardColumns,
    QueryBoardGroups,
    QueryBoardItems,
    CreateBoardItem,
)


# *** contexts

# ** context: board_context
class BoardContext(MondayContext):
    '''
    Context-as-client for a Monday.com board.
    Wraps a Board domain object and exposes domain behaviors as methods.
    Each method triggers a domain event via injected services.
    '''

    # * attribute: _board
    _board: Board

    # * init
    def __init__(self, board: Board, api_key: str, **kwargs):
        '''
        Initialize the board context.

        :param board: The board domain object.
        :type board: Board
        :param api_key: The Monday.com API key.
        :type api_key: str
        '''

        # Initialize the parent context.
        super().__init__(api_key, **kwargs)

        # Set the board domain object.
        self._board = board

    # * property: id
    @property
    def id(self) -> str:
        '''The board ID.'''
        return self._board.id

    # * property: name
    @property
    def name(self) -> str:
        '''The board name.'''
        return self._board.name

    # * property: description
    @property
    def description(self) -> Optional[str]:
        '''The board description.'''
        return self._board.description

    # * property: board_kind
    @property
    def board_kind(self) -> Optional[str]:
        '''The board kind.'''
        return self._board.board_kind

    # * property: state
    @property
    def state(self) -> Optional[str]:
        '''The board state.'''
        return self._board.state

    # * method: get_items
    def get_items(self, limit: int = 25) -> list:
        '''
        Query items from this board. Returns a list of ItemContext objects.

        :param limit: Number of items to retrieve.
        :type limit: int
        :return: List of ItemContext objects.
        :rtype: list[ItemContext]
        '''

        # Import here to avoid circular dependency.
        from .item import ItemContext

        # Execute the query board items event.
        event = QueryBoardItems(board_service=self._board_service)
        items_data = event.execute(board_id=self.id, limit=limit)

        # Wrap each item dict in an ItemContext.
        return [
            ItemContext.from_api_data(data, api_key=self._api_key, board_service=self._board_service, item_service=self._item_service)
            for data in items_data
        ]

    # * method: get_columns
    def get_columns(self) -> List[Column]:
        '''
        Query all columns in this board.

        :return: List of Column domain objects.
        :rtype: List[Column]
        '''

        # Execute the query board columns event.
        event = QueryBoardColumns(board_service=self._board_service)
        return event.execute(board_id=self.id)

    # * method: get_groups
    def get_groups(self) -> List[Group]:
        '''
        Query all groups in this board.

        :return: List of Group domain objects.
        :rtype: List[Group]
        '''

        # Execute the query board groups event.
        event = QueryBoardGroups(board_service=self._board_service)
        return event.execute(board_id=self.id)

    # * method: create_item
    def create_item(self, item_name: str, group_id: str = None, column_values: Dict[str, Any] = None, **kwargs):
        '''
        Create a new item in this board. Returns an ItemContext.

        :param item_name: The item name.
        :type item_name: str
        :param group_id: Optional group ID.
        :type group_id: str
        :param column_values: Optional column values.
        :type column_values: Dict[str, Any]
        :return: The created ItemContext.
        :rtype: ItemContext
        '''

        # Import here to avoid circular dependency.
        from .item import ItemContext

        # Execute the create board item event.
        event = CreateBoardItem(board_service=self._board_service)
        data = event.execute(
            board_id=self.id,
            item_name=item_name,
            group_id=group_id,
            column_values=column_values,
            **kwargs,
        )

        # Wrap in ItemContext.
        return ItemContext.from_api_data(data, api_key=self._api_key, board_service=self._board_service, item_service=self._item_service)

    # * method: __repr__
    def __repr__(self) -> str:
        '''String representation.'''
        return f'BoardContext(id={self.id}, name={self.name})'
