"""Tiferet Monday User Events"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayEvent
from ..interfaces.user import UserService
from ..domain.user import User, Team, Account


# *** events

# ** event: get_users
class GetUsers(MondayEvent):
    '''
    Event to retrieve users from Monday.com.
    '''

    # * attribute: user_service
    user_service: UserService

    # * init
    def __init__(self, user_service: UserService):
        '''
        Initialize the GetUsers event.

        :param user_service: The user service.
        :type user_service: UserService
        '''

        # Set the user service dependency.
        self.user_service = user_service

    # * method: execute
    def execute(self,
                ids: List[str] = None,
                limit: int = 50,
                page: int = 1,
                kind: str = 'all',
                emails: List[str] = None,
                **kwargs) -> List[dict]:
        '''
        Retrieve users. Returns raw dicts for context wrapping.

        :param ids: Optional list of user IDs.
        :type ids: List[str]
        :param limit: Number of users to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :param kind: User kind filter.
        :type kind: str
        :param emails: Optional email addresses to filter by.
        :type emails: List[str]
        :return: List of user data dicts.
        :rtype: List[dict]
        '''

        # Query users from the service.
        return self.user_service.get_users(
            ids=ids,
            limit=limit,
            page=page,
            kind=kind,
            emails=emails,
        )


# ** event: get_me
class GetMe(MondayEvent):
    '''
    Event to retrieve the current user (API token owner).
    '''

    # * attribute: user_service
    user_service: UserService

    # * init
    def __init__(self, user_service: UserService):
        '''
        Initialize the GetMe event.

        :param user_service: The user service.
        :type user_service: UserService
        '''

        # Set the user service dependency.
        self.user_service = user_service

    # * method: execute
    def execute(self, **kwargs) -> dict:
        '''
        Retrieve the current user. Returns raw dict for context wrapping.

        :return: The current user data dict.
        :rtype: dict
        '''

        # Query the current user from the service.
        return self.user_service.get_me()


# ** event: get_teams
class GetTeams(MondayEvent):
    '''
    Event to retrieve teams from Monday.com.
    '''

    # * attribute: user_service
    user_service: UserService

    # * init
    def __init__(self, user_service: UserService):
        '''
        Initialize the GetTeams event.

        :param user_service: The user service.
        :type user_service: UserService
        '''

        # Set the user service dependency.
        self.user_service = user_service

    # * method: execute
    def execute(self, ids: List[str] = None, **kwargs) -> List[Team]:
        '''
        Retrieve teams.

        :param ids: Optional list of team IDs.
        :type ids: List[str]
        :return: List of Team domain objects.
        :rtype: List[Team]
        '''

        # Query teams from the service.
        data = self.user_service.get_teams(ids=ids)

        # Return team domain objects.
        return [Team.model_validate(t) for t in data]


# ** event: get_account
class GetAccount(MondayEvent):
    '''
    Event to retrieve account information.
    '''

    # * attribute: user_service
    user_service: UserService

    # * init
    def __init__(self, user_service: UserService):
        '''
        Initialize the GetAccount event.

        :param user_service: The user service.
        :type user_service: UserService
        '''

        # Set the user service dependency.
        self.user_service = user_service

    # * method: execute
    def execute(self, **kwargs) -> Optional[Account]:
        '''
        Retrieve account information.

        :return: The Account domain object, or None.
        :rtype: Optional[Account]
        '''

        # Query account from the service.
        data = self.user_service.get_account()

        # Return None if not found.
        if not data:
            return None

        # Return the account domain object.
        return Account.model_validate(data)
