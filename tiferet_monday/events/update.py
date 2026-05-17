"""Tiferet Monday Update Events"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayEvent
from ..interfaces.update import UpdateService
from ..domain.item import Update


# *** events

# ** event: query_updates
class QueryUpdates(MondayEvent):
    '''
    Event to query updates (comments) from Monday.com.
    '''

    # * attribute: update_service
    update_service: UpdateService

    # * init
    def __init__(self, update_service: UpdateService):
        '''
        Initialize the QueryUpdates event.

        :param update_service: The update service.
        :type update_service: UpdateService
        '''

        # Set the update service dependency.
        self.update_service = update_service

    # * method: execute
    def execute(self,
                item_id: str = None,
                limit: int = 25,
                page: int = 1,
                **kwargs) -> List[Update]:
        '''
        Query updates. Returns Update domain objects.

        :param item_id: Optional item ID to filter.
        :type item_id: str
        :param limit: Number of updates.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of Update domain objects.
        :rtype: List[Update]
        '''

        # Query updates from the service.
        data = self.update_service.query_updates(
            item_id=item_id,
            limit=limit,
            page=page,
        )

        # Return update domain objects.
        return [Update.model_validate(u) for u in data]


# ** event: create_update
class CreateUpdate(MondayEvent):
    '''
    Event to create an update (comment) on an item.
    '''

    # * attribute: update_service
    update_service: UpdateService

    # * init
    def __init__(self, update_service: UpdateService):
        '''
        Initialize the CreateUpdate event.

        :param update_service: The update service.
        :type update_service: UpdateService
        '''

        # Set the update service dependency.
        self.update_service = update_service

    # * method: execute
    def execute(self, item_id: str, body: str, parent_id: str = None, **kwargs) -> Update:
        '''
        Create an update on an item.

        :param item_id: The item ID.
        :type item_id: str
        :param body: The update body text.
        :type body: str
        :param parent_id: Optional parent update ID (for replies).
        :type parent_id: str
        :return: The created Update domain object.
        :rtype: Update
        '''

        # Create the update via the service.
        data = self.update_service.create_update(
            item_id=item_id,
            body=body,
            parent_id=parent_id,
        )

        # Return the update domain object.
        return Update.model_validate(data)


# ** event: create_notification
class CreateNotification(MondayEvent):
    '''
    Event to send a notification to a user.
    '''

    # * attribute: update_service
    update_service: UpdateService

    # * init
    def __init__(self, update_service: UpdateService):
        '''
        Initialize the CreateNotification event.

        :param update_service: The update service.
        :type update_service: UpdateService
        '''

        # Set the update service dependency.
        self.update_service = update_service

    # * method: execute
    def execute(self,
                user_id: str,
                target_id: str,
                text: str,
                target_type: str = 'Project',
                **kwargs) -> dict:
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

        # Create the notification via the service.
        return self.update_service.create_notification(
            user_id=user_id,
            target_id=target_id,
            text=text,
            target_type=target_type,
        )


# ** event: delete_update
class DeleteUpdate(MondayEvent):
    '''
    Event to delete an update.
    '''

    # * attribute: update_service
    update_service: UpdateService

    # * init
    def __init__(self, update_service: UpdateService):
        '''
        Initialize the DeleteUpdate event.

        :param update_service: The update service.
        :type update_service: UpdateService
        '''

        # Set the update service dependency.
        self.update_service = update_service

    # * method: execute
    def execute(self, update_id: str, **kwargs) -> dict:
        '''
        Delete an update.

        :param update_id: The update ID.
        :type update_id: str
        :return: The deleted update data.
        :rtype: dict
        '''

        # Delete the update via the service.
        return self.update_service.delete_update(update_id=update_id)
