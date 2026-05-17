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
from ..domain.workspace import Workspace
from ..domain.tag import Tag
from ..domain.webhook import Webhook
from ..events.board import GetBoard, CreateBoard
from ..events.item import GetItems
from ..events.user import GetUsers, GetMe, GetTeams, GetAccount
from ..events.update import CreateNotification
from ..events.workspace import GetWorkspaces, CreateWorkspace as CreateWorkspaceEvent
from ..events.tag import GetTags, CreateOrGetTag
from ..events.webhook import CreateWebhook as CreateWebhookEvent, DeleteWebhook


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

    # * method: get_workspaces
    def get_workspaces(self, ids: List[str] = None, kind: str = None, limit: int = 25) -> List[Workspace]:
        '''
        Retrieve workspaces.

        :param ids: Optional list of workspace IDs.
        :type ids: List[str]
        :param kind: Optional kind filter (open / closed).
        :type kind: str
        :param limit: Number of workspaces.
        :type limit: int
        :return: List of Workspace domain objects.
        :rtype: List[Workspace]
        '''

        # Execute the get workspaces event.
        event = GetWorkspaces(workspace_service=self._workspace_service)
        return event.execute(ids=ids, kind=kind, limit=limit)

    # * method: create_workspace
    def create_workspace(self, name: str, kind: str = 'open', description: str = None) -> Workspace:
        '''
        Create a new workspace.

        :param name: The workspace name.
        :type name: str
        :param kind: The workspace kind (open / closed).
        :type kind: str
        :param description: Optional description.
        :type description: str
        :return: The created Workspace domain object.
        :rtype: Workspace
        '''

        # Execute the create workspace event.
        event = CreateWorkspaceEvent(workspace_service=self._workspace_service)
        return event.execute(name=name, kind=kind, description=description)

    # * method: get_tags
    def get_tags(self, ids: List[str] = None) -> List[Tag]:
        '''
        Retrieve tags.

        :param ids: Optional list of tag IDs.
        :type ids: List[str]
        :return: List of Tag domain objects.
        :rtype: List[Tag]
        '''

        # Execute the get tags event.
        event = GetTags(tag_service=self._tag_service)
        return event.execute(ids=ids)

    # * method: create_or_get_tag
    def create_or_get_tag(self, tag_name: str, board_id: str = None) -> Tag:
        '''
        Create a tag or get it if it already exists.

        :param tag_name: The tag name.
        :type tag_name: str
        :param board_id: Optional board ID.
        :type board_id: str
        :return: The Tag domain object.
        :rtype: Tag
        '''

        # Execute the create or get tag event.
        event = CreateOrGetTag(tag_service=self._tag_service)
        return event.execute(tag_name=tag_name, board_id=board_id)

    # * method: create_webhook
    def create_webhook(self, board_id: str, url: str, event_type: str, config: str = None) -> Webhook:
        '''
        Create a webhook on a board.

        :param board_id: The board ID.
        :type board_id: str
        :param url: The callback URL.
        :type url: str
        :param event_type: The event type.
        :type event_type: str
        :param config: Optional JSON config.
        :type config: str
        :return: The created Webhook domain object.
        :rtype: Webhook
        '''

        # Execute the create webhook event.
        event = CreateWebhookEvent(webhook_service=self._webhook_service)
        return event.execute(board_id=board_id, url=url, event=event_type, config=config)

    # * method: delete_webhook
    def delete_webhook(self, webhook_id: str) -> dict:
        '''
        Delete a webhook.

        :param webhook_id: The webhook ID.
        :type webhook_id: str
        :return: The deleted webhook data.
        :rtype: dict
        '''

        # Execute the delete webhook event.
        event = DeleteWebhook(webhook_service=self._webhook_service)
        return event.execute(webhook_id=webhook_id)

    # * method: __repr__
    def __repr__(self) -> str:
        '''String representation.'''
        return 'MondayApp(authenticated=True)'
