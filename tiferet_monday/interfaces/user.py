"""Tiferet Monday User Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List, Optional

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: user_service
class UserService(MondayService):
    '''
    Service interface for user-related Monday.com API operations.
    '''

    # * method: get_users
    @abstractmethod
    def get_users(self,
                  ids: List[str] = None,
                  limit: int = 50,
                  page: int = 1,
                  kind: str = 'all',
                  emails: List[str] = None) -> List[dict]:
        '''
        Query users, optionally filtered by IDs, kind, or emails.

        :param ids: Optional list of user IDs.
        :type ids: List[str]
        :param limit: Number of users to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :param kind: User kind filter (all / guests / non_guests / non_pending).
        :type kind: str
        :param emails: Optional list of email addresses to filter by.
        :type emails: List[str]
        :return: List of user data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: get_me
    @abstractmethod
    def get_me(self) -> dict:
        '''
        Query the current user (API token owner).

        :return: The current user data dict.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: get_teams
    @abstractmethod
    def get_teams(self, ids: List[str] = None) -> List[dict]:
        '''
        Query teams, optionally filtered by IDs.

        :param ids: Optional list of team IDs.
        :type ids: List[str]
        :return: List of team data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: get_account
    @abstractmethod
    def get_account(self) -> Optional[dict]:
        '''
        Query account information for the current user.

        :return: The account data dict, or None.
        :rtype: Optional[dict]
        '''
        raise NotImplementedError()
