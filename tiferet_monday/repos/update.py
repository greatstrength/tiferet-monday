"""Tiferet Monday Update Repos"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.update import UpdateService


# *** repos

# ** repo: update_api_proxy
class UpdateApiProxy(UpdateService, MondayApiProxy):
    '''
    Concrete UpdateService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        '''
        Initialize the update API proxy.

        :param monday_api_key: The Monday.com API key.
        :type monday_api_key: str
        '''

        # Initialize the parent proxy.
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: query_updates
    def query_updates(self,
                      item_id: str = None,
                      limit: int = 25,
                      page: int = 1) -> List[dict]:
        '''
        Query updates from the Monday.com API.

        :param item_id: Optional item ID to filter updates.
        :type item_id: str
        :param limit: Number of updates to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of update data dicts.
        :rtype: List[dict]
        '''

        # If item_id is provided, query updates via items.
        if item_id:
            return self.execute_query(
                query="""
                    query ($itemId: ID!, $limit: Int!) {
                        items (ids: [$itemId]) {
                            updates (limit: $limit) {
                                id
                                body
                                text_body
                                creator_id
                                item_id
                                replies {
                                    id
                                    creator_id
                                    body
                                }
                            }
                        }
                    }
                """,
                variables={
                    'itemId': int(item_id),
                    'limit': limit,
                },
                start_node=lambda data: data.get('items', [{}])[0].get('updates', []),
            )

        # Otherwise, query updates globally.
        return self.execute_query(
            query="""
                query ($limit: Int!, $page: Int!) {
                    updates (limit: $limit, page: $page) {
                        id
                        body
                        text_body
                        creator_id
                        item_id
                        replies {
                            id
                            creator_id
                            body
                        }
                    }
                }
            """,
            variables={
                'limit': limit,
                'page': page,
            },
            start_node=lambda data: data.get('updates', []),
        )

    # * method: create_update
    def create_update(self, item_id: str, body: str, parent_id: str = None) -> dict:
        '''
        Create an update (comment) on an item.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body text.
        :type body: str
        :param parent_id: Optional parent update ID (for replies).
        :type parent_id: str
        :return: The created update data.
        :rtype: dict
        '''

        # Build variables.
        variables = {
            'itemId': int(item_id),
            'body': body,
        }

        # Build dynamic params for optional parent_id.
        params = '$itemId: ID!, $body: String!'
        args = 'item_id: $itemId, body: $body'
        if parent_id:
            variables['parentId'] = int(parent_id)
            params += ', $parentId: ID'
            args += ', parent_id: $parentId'

        # Execute the mutation.
        return self.execute_query(
            query=f"""
                mutation ({params}) {{
                    create_update ({args}) {{
                        id
                        body
                        text_body
                        creator_id
                        item_id
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('create_update', {}),
        )

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

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($userId: ID!, $targetId: ID!, $text: String!, $targetType: NotificationTargetType!) {
                    create_notification (user_id: $userId, target_id: $targetId, text: $text, target_type: $targetType) {
                        text
                    }
                }
            """,
            variables={
                'userId': int(user_id),
                'targetId': int(target_id),
                'text': text,
                'targetType': target_type,
            },
            start_node=lambda data: data.get('create_notification', {}),
        )

    # * method: delete_update
    def delete_update(self, update_id: str) -> dict:
        '''
        Delete an update.

        :param update_id: The update ID.
        :type update_id: str
        :return: The deleted update data.
        :rtype: dict
        '''

        # Execute the mutation.
        return self.execute_query(
            query="""
                mutation ($updateId: ID!) {
                    delete_update (id: $updateId) {
                        id
                    }
                }
            """,
            variables={'updateId': int(update_id)},
            start_node=lambda data: data.get('delete_update', {}),
        )
