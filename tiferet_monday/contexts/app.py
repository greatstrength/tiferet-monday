"""Tiferet Monday App Context"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayContext
from .board import BoardContext
from .item import ItemContext
from ..domain.board import Board
from ..domain.user import Team, Account
from ..events.board import GetBoard, CreateBoard
from ..events.item import GetItems
from ..events.user import GetUsers, GetMe, GetTeams, GetAccount
from ..events.update import CreateNotification


# *** contexts

# ** context: monday_app
class MondayApp(MondayContext):
    '''
    Top-level Monday.com client context.
    Entry point for all Monday.com API interactions.

    Usage::

        from tiferet_monday import MondayApp

        app = MondayApp(api_key='your_api_key')
        board = app.get_board('12345')
        items = board.get_items()
        item = items[0]
        cvs = item.get_column_values()
    '''

    # * init
    def __init__(self, api_key: str):
        '''
        Initialize the Monday.com application client.

        :param api_key: The Monday.com API key.
        :type api_key: str
        '''

        # Initialize the parent context with the API key.
        super().__init__(api_key)

    # * method: get_board
    def get_board(self, board_id: str) -> Optional[BoardContext]:
        '''
        Retrieve a board by ID. Returns a BoardContext for chained operations.

        :param board_id: The board ID.
        :type board_id: str
        :return: The BoardContext, or None if not found.
        :rtype: Optional[BoardContext]
        '''

        # Execute the get board event.
        event = GetBoard(board_service=self._board_service)
        board = event.execute(board_id=board_id)

        # Return None if not found.
        if not board:
            return None

        # Wrap in BoardContext.
        return BoardContext(
            board=board,
            api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
        )

    # * method: create_board
    def create_board(self, board_name: str, board_kind: str = 'public', workspace_id: str = None) -> BoardContext:
        '''
        Create a new board. Returns a BoardContext for chained operations.

        :param board_name: The board name.
        :type board_name: str
        :param board_kind: The board kind (public / private / share).
        :type board_kind: str
        :param workspace_id: Optional workspace ID.
        :type workspace_id: str
        :return: The created BoardContext.
        :rtype: BoardContext
        '''

        # Execute the create board event.
        event = CreateBoard(board_service=self._board_service)
        board = event.execute(
            board_name=board_name,
            board_kind=board_kind,
            workspace_id=workspace_id,
        )

        # Wrap in BoardContext.
        return BoardContext(
            board=board,
            api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
        )

    # * method: get_items
    def get_items(self, item_ids: List[str]) -> List[ItemContext]:
        '''
        Retrieve items by their IDs. Returns ItemContext objects.

        :param item_ids: List of item IDs.
        :type item_ids: List[str]
        :return: List of ItemContext objects.
        :rtype: List[ItemContext]
        '''

        # Execute the get items event.
        event = GetItems(item_service=self._item_service)
        items_data = event.execute(item_ids=item_ids)

        # Wrap each in ItemContext.
        return [
            ItemContext.from_api_data(
                data,
                api_key=self._api_key,
                board_service=self._board_service,
                item_service=self._item_service,
            )
            for data in items_data
        ]

    # * method: get_users
    def get_users(self, ids: List[str] = None, limit: int = 50) -> list:
        '''
        Retrieve users. Returns a list of UserContext objects.

        :param ids: Optional list of user IDs.
        :type ids: List[str]
        :param limit: Number of users to retrieve.
        :type limit: int
        :return: List of UserContext objects.
        :rtype: list[UserContext]
        '''

        # Import here to avoid circular dependency.
        from .user import UserContext

        # Execute the get users event.
        event = GetUsers(user_service=self._user_service)
        users_data = event.execute(ids=ids, limit=limit)

        # Wrap each in UserContext.
        return [
            UserContext.from_api_data(
                data,
                api_key=self._api_key,
                board_service=self._board_service,
                item_service=self._item_service,
                user_service=self._user_service,
            )
            for data in users_data
        ]

    # * method: get_me
    def get_me(self) -> 'UserContext':
        '''
        Retrieve the current user (API token owner). Returns a UserContext.

        :return: The UserContext for the current user.
        :rtype: UserContext
        '''

        # Import here to avoid circular dependency.
        from .user import UserContext

        # Execute the get me event.
        event = GetMe(user_service=self._user_service)
        data = event.execute()

        # Wrap in UserContext.
        return UserContext.from_api_data(
            data,
            api_key=self._api_key,
            board_service=self._board_service,
            item_service=self._item_service,
            user_service=self._user_service,
        )

    # * method: get_teams
    def get_teams(self, ids: List[str] = None) -> List[Team]:
        '''
        Retrieve teams.

        :param ids: Optional list of team IDs.
        :type ids: List[str]
        :return: List of Team domain objects.
        :rtype: List[Team]
        '''

        # Execute the get teams event.
        event = GetTeams(user_service=self._user_service)
        return event.execute(ids=ids)

    # * method: get_account
    def get_account(self) -> Optional[Account]:
        '''
        Retrieve account information.

        :return: The Account domain object, or None.
        :rtype: Optional[Account]
        '''

        # Execute the get account event.
        event = GetAccount(user_service=self._user_service)
        return event.execute()

    # * method: create_notification
    def create_notification(self,
                            user_id: str,
                            target_id: str,
                            text: str,
                            target_type: str = 'Project') -> dict:
        '''
        Send a notification to a user.

        :param user_id: The target user ID.
        :type user_id: str
        :param target_id: The target object ID.
        :type target_id: str
        :param text: The notification text.
        :type text: str
        :param target_type: The target type (Project or Post).
        :type target_type: str
        :return: The notification response data.
        :rtype: dict
        '''

        # Execute the create notification event.
        event = CreateNotification(update_service=self._update_service)
        return event.execute(
            user_id=user_id,
            target_id=target_id,
            text=text,
            target_type=target_type,
        )

    # * method: __repr__
    def __repr__(self) -> str:
        '''String representation.'''
        return 'MondayApp(authenticated=True)'
