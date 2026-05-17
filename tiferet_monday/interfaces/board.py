"""Tiferet Monday Board Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import Any, Dict, List, Optional

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: board_service
class BoardService(MondayService):
    '''
    Service interface for board-related Monday.com API operations.
    '''

    # * method: get_boards
    @abstractmethod
    def get_boards(self, ids: List[str] = None, limit: int = 25, page: int = 1) -> List[dict]:
        '''
        Retrieve boards, optionally filtered by IDs.

        :param ids: Optional list of board IDs.
        :type ids: List[str]
        :param limit: Number of boards to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of board data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_board
    @abstractmethod
    def create_board(self, board_name: str, board_kind: str, workspace_id: str = None) -> dict:
        '''
        Create a new board.

        :param board_name: The board name.
        :type board_name: str
        :param board_kind: The board kind (public / private / share).
        :type board_kind: str
        :param workspace_id: Optional workspace ID.
        :type workspace_id: str
        :return: The created board data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: archive_board
    @abstractmethod
    def archive_board(self, board_id: str) -> dict:
        '''
        Archive a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: The archived board data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: query_columns
    @abstractmethod
    def query_columns(self, board_id: str) -> List[dict]:
        '''
        Query all columns in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of column data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: add_column
    @abstractmethod
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
        raise NotImplementedError()

    # * method: query_groups
    @abstractmethod
    def query_groups(self, board_id: str) -> List[dict]:
        '''
        Query all groups in a board.

        :param board_id: The board ID.
        :type board_id: str
        :return: List of group data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_group
    @abstractmethod
    def create_group(self, board_id: str, group_name: str) -> dict:
        '''
        Create a new group in a board.

        :param board_id: The board ID.
        :type board_id: str
        :param group_name: The group name.
        :type group_name: str
        :return: The created group data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: query_items_page
    @abstractmethod
    def query_items_page(self, board_id: str, limit: int = 25) -> List[dict]:
        '''
        Query a page of items from a board.

        :param board_id: The board ID.
        :type board_id: str
        :param limit: Number of items per page.
        :type limit: int
        :return: List of item data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_item
    @abstractmethod
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
        raise NotImplementedError()
