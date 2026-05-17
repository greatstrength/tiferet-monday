"""Tiferet Monday Update Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List, Optional

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: update_service
class UpdateService(MondayService):
    '''
    Service interface for update and notification Monday.com API operations.
    '''

    # * method: query_updates
    @abstractmethod
    def query_updates(self,
                      item_id: str = None,
                      limit: int = 25,
                      page: int = 1) -> List[dict]:
        '''
        Query updates (comments), optionally filtered by item.

        :param item_id: Optional item ID to filter updates.
        :type item_id: str
        :param limit: Number of updates to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of update data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_update
    @abstractmethod
    def create_update(self, item_id: str, body: str, parent_id: str = None) -> dict:
        '''
        Create an update (comment) on an item, optionally as a reply.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body text.
        :type body: str
        :param parent_id: Optional parent update ID (for replies).
        :type parent_id: str
        :return: The created update data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: create_notification
    @abstractmethod
    def create_notification(self,
                            user_id: str,
                            target_id: str,
                            text: str,
                            target_type: str = 'Project') -> dict:
        '''
        Send a notification to a user.

        :param user_id: The target user ID.
        :type user_id: str
        :param target_id: The target object ID (item/board for Project, update/reply for Post).
        :type target_id: str
        :param text: The notification text.
        :type text: str
        :param target_type: The target type (Project or Post).
        :type target_type: str
        :return: The notification response data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: delete_update
    @abstractmethod
    def delete_update(self, update_id: str) -> dict:
        '''
        Delete an update.

        :param update_id: The update ID.
        :type update_id: str
        :return: The deleted update data.
        :rtype: dict
        '''
        raise NotImplementedError()
