"""Tiferet Monday Board Events"""

# *** imports

# ** core
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayEvent
from ..interfaces.board import BoardService
from ..domain.board import Board, Column, Group


# *** events

# ** event: get_board
class GetBoard(MondayEvent):
    '''
    Event to retrieve a board by ID.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the GetBoard event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self, board_id: str, **kwargs) -> Optional[Board]:
        '''
        Retrieve a board by its ID.

        :param board_id: The board ID.
        :type board_id: str
        :return: The board, or None.
        :rtype: Optional[Board]
        '''

        # Query the board from the service.
        boards = self.board_service.get_boards(ids=[board_id], limit=1)

        # Return None if not found.
        if not boards:
            return None

        # Return the board domain object.
        return Board.model_validate(boards[0])


# ** event: create_board
class CreateBoard(MondayEvent):
    '''
    Event to create a new board.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the CreateBoard event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self, board_name: str, board_kind: str = 'public', workspace_id: str = None, **kwargs) -> Board:
        '''
        Create a new board.

        :param board_name: The board name.
        :type board_name: str
        :param board_kind: The board kind.
        :type board_kind: str
        :param workspace_id: Optional workspace ID.
        :type workspace_id: str
        :return: The created board.
        :rtype: Board
        '''

        # Create the board via the service.
        data = self.board_service.create_board(
            board_name=board_name,
            board_kind=board_kind,
            workspace_id=workspace_id,
        )

        # Return the board domain object.
        return Board.model_validate(data)


# ** event: query_board_columns
class QueryBoardColumns(MondayEvent):
    '''
    Event to query all columns in a board.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the QueryBoardColumns event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self, board_id: str, **kwargs) -> List[Column]:
        '''
        Query all columns in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of columns.
        :rtype: List[Column]
        '''

        # Query columns from the service.
        data = self.board_service.query_columns(board_id=board_id)

        # Return column domain objects.
        return [Column.model_validate(c) for c in data]


# ** event: query_board_groups
class QueryBoardGroups(MondayEvent):
    '''
    Event to query all groups in a board.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the QueryBoardGroups event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self, board_id: str, **kwargs) -> List[Group]:
        '''
        Query all groups in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of groups.
        :rtype: List[Group]
        '''

        # Query groups from the service.
        data = self.board_service.query_groups(board_id=board_id)

        # Return group domain objects.
        return [Group.model_validate(g) for g in data]


# ** event: query_board_items
class QueryBoardItems(MondayEvent):
    '''
    Event to query items from a board.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the QueryBoardItems event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self, board_id: str, limit: int = 25, **kwargs) -> List[dict]:
        '''
        Query items from a board. Returns raw dicts for context wrapping.

        :param board_id: The board ID.
        :type board_id: str
        :param limit: Number of items per page.
        :type limit: int
        :return: List of item data dicts.
        :rtype: List[dict]
        '''

        # Query items from the service.
        return self.board_service.query_items_page(board_id=board_id, limit=limit)


# ** event: create_board_item
class CreateBoardItem(MondayEvent):
    '''
    Event to create a new item in a board.
    '''

    # * attribute: board_service
    board_service: BoardService

    # * init
    def __init__(self, board_service: BoardService):
        '''
        Initialize the CreateBoardItem event.

        :param board_service: The board service.
        :type board_service: BoardService
        '''

        # Set the board service dependency.
        self.board_service = board_service

    # * method: execute
    def execute(self,
                board_id: str,
                item_name: str,
                group_id: str = None,
                column_values: Dict[str, Any] = None,
                create_labels_if_missing: bool = False,
                **kwargs) -> dict:
        '''
        Create a new item in a board. Returns raw dict for context wrapping.

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
        :return: The created item data dict.
        :rtype: dict
        '''

        # Create the item via the service.
        return self.board_service.create_item(
            board_id=board_id,
            item_name=item_name,
            group_id=group_id,
            column_values=column_values,
            create_labels_if_missing=create_labels_if_missing,
        )
