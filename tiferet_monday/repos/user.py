"""Tiferet Monday User Repos"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.user import UserService


# *** repos

# ** repo: user_api_proxy
class UserApiProxy(UserService, MondayApiProxy):
    '''
    Concrete UserService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        '''
        Initialize the user API proxy.

        :param monday_api_key: The Monday.com API key.
        :type monday_api_key: str
        '''

        # Initialize the parent proxy.
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: get_users
    def get_users(self,
                  ids: List[str] = None,
                  limit: int = 50,
                  page: int = 1,
                  kind: str = 'all',
                  emails: List[str] = None) -> List[dict]:
        '''
        Query users from the Monday.com API.

        :param ids: Optional list of user IDs.
        :type ids: List[str]
        :param limit: Number of users to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :param kind: User kind filter (all / guests / non_guests / non_pending).
        :type kind: str
        :param emails: Optional email addresses to filter by.
        :type emails: List[str]
        :return: List of user data dicts.
        :rtype: List[dict]
        '''

        # Build variables.
        variables = {
            'limit': limit,
            'page': page,
            'kind': kind,
        }

        # Build dynamic parameter declarations.
        params = ['$limit: Int!', '$page: Int!', '$kind: UserKind']
        args = ['limit: $limit', 'page: $page', 'kind: $kind']

        # Add optional ID filter.
        if ids:
            variables['ids'] = [int(i) for i in ids]
            params.append('$ids: [ID!]')
            args.append('ids: $ids')

        # Add optional email filter.
        if emails:
            variables['emails'] = emails
            params.append('$emails: [String!]')
            args.append('emails: $emails')

        # Build the query string.
        params_str = ', '.join(params)
        args_str = ', '.join(args)

        # Execute the query.
        return self.execute_query(
            query=f"""
                query ({params_str}) {{
                    users ({args_str}) {{
                        id
                        name
                        email
                        phone
                        mobile_phone
                        photo_original
                        photo_thumb
                        title
                        birthday
                        country_code
                        location
                        time_zone_identifier
                        is_guest
                        is_admin
                        is_view_only
                        is_pending
                        enabled
                        created_at
                        url
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('users', []),
        )

    # * method: get_me
    def get_me(self) -> dict:
        '''
        Query the current user (API token owner).

        :return: The current user data dict.
        :rtype: dict
        '''

        # Execute the query.
        return self.execute_query(
            query="""
                query {
                    me {
                        id
                        name
                        email
                        phone
                        mobile_phone
                        photo_original
                        photo_thumb
                        title
                        birthday
                        country_code
                        location
                        time_zone_identifier
                        is_guest
                        is_admin
                        is_view_only
                        is_pending
                        enabled
                        created_at
                        url
                    }
                }
            """,
            start_node=lambda data: data.get('me', {}),
        )

    # * method: get_teams
    def get_teams(self, ids: List[str] = None) -> List[dict]:
        '''
        Query teams from the Monday.com API.

        :param ids: Optional list of team IDs.
        :type ids: List[str]
        :return: List of team data dicts.
        :rtype: List[dict]
        '''

        # Build variables and params.
        variables = {}
        id_param = ''
        id_arg = ''
        if ids:
            variables['ids'] = [int(i) for i in ids]
            id_param = '$ids: [ID!]'
            id_arg = 'ids: $ids'

        # Build the query string.
        param_block = f'({id_param})' if id_param else ''
        arg_block = f'({id_arg})' if id_arg else ''

        # Execute the query.
        return self.execute_query(
            query=f"""
                query {param_block} {{
                    teams {arg_block} {{
                        id
                        name
                        picture_url
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('teams', []),
        )

    # * method: get_account
    def get_account(self) -> Optional[dict]:
        '''
        Query account information for the current user.

        :return: The account data dict, or None.
        :rtype: Optional[dict]
        '''

        # Execute the query via me -> account.
        return self.execute_query(
            query="""
                query {
                    me {
                        account {
                            id
                            name
                            slug
                            tier
                            show_timeline_weekends
                            country_code
                            logo
                        }
                    }
                }
            """,
            start_node=lambda data: data.get('me', {}).get('account'),
        )
