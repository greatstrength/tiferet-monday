"""Tiferet Monday User Context"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayContext
from ..domain.user import User, Team
from ..events.user import GetTeams


# *** contexts

# ** context: user_context
class UserContext(MondayContext):
    '''
    Context-as-client for a Monday.com user.
    Wraps a User domain object and exposes domain behaviors as methods.
    Each method triggers a domain event via injected services.
    '''

    # * attribute: _user
    _user: User

    # * init
    def __init__(self, user: User, api_key: str, **kwargs):
        '''
        Initialize the user context.

        :param user: The user domain object.
        :type user: User
        :param api_key: The Monday.com API key.
        :type api_key: str
        '''

        # Initialize the parent context.
        super().__init__(api_key, **kwargs)

        # Set the user domain object.
        self._user = user

    # * method: from_api_data (static)
    @staticmethod
    def from_api_data(data: dict, api_key: str, **kwargs) -> 'UserContext':
        '''
        Create a UserContext from raw Monday.com API response data.

        :param data: The raw API data dict.
        :type data: dict
        :param api_key: The Monday.com API key.
        :type api_key: str
        :return: The UserContext.
        :rtype: UserContext
        '''

        # Create the user domain object.
        user = User.model_validate(data)

        # Return the user context.
        return UserContext(user=user, api_key=api_key, **kwargs)

    # * property: id
    @property
    def id(self) -> str:
        '''The user ID.'''
        return self._user.id

    # * property: name
    @property
    def name(self) -> str:
        '''The user name.'''
        return self._user.name

    # * property: email
    @property
    def email(self) -> Optional[str]:
        '''The user email.'''
        return self._user.email

    # * property: title
    @property
    def title(self) -> Optional[str]:
        '''The user title.'''
        return self._user.title

    # * property: is_admin
    @property
    def is_admin(self) -> Optional[bool]:
        '''Whether the user is an admin.'''
        return self._user.is_admin

    # * property: is_guest
    @property
    def is_guest(self) -> Optional[bool]:
        '''Whether the user is a guest.'''
        return self._user.is_guest

    # * property: enabled
    @property
    def enabled(self) -> Optional[bool]:
        '''Whether the user is enabled.'''
        return self._user.enabled

    # * property: photo_original
    @property
    def photo_original(self) -> Optional[str]:
        '''The user photo URL (original size).'''
        return self._user.photo_original

    # * method: get_teams
    def get_teams(self) -> List[Team]:
        '''
        Query teams that this user belongs to.

        Note: The Monday.com API does not support filtering teams by user
        at the query level. This method queries all teams and is provided
        as a convenience. For user-specific teams, nest teams inside a
        users query at the API proxy level.

        :return: List of Team domain objects.
        :rtype: List[Team]
        '''

        # Execute the get teams event.
        event = GetTeams(user_service=self._user_service)
        return event.execute()

    # * method: __repr__
    def __repr__(self) -> str:
        '''String representation.'''
        return f'UserContext(id={self.id}, name={self.name})'
