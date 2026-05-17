"""Tiferet Monday Webhook Events"""

# *** imports

# ** core
from typing import Optional

# ** app
from .settings import MondayEvent
from ..interfaces.webhook import WebhookService
from ..domain.webhook import Webhook


# *** events

# ** event: create_webhook
class CreateWebhook(MondayEvent):
    '''
    Event to create a webhook on a board.
    '''

    # * attribute: webhook_service
    webhook_service: WebhookService

    # * init
    def __init__(self, webhook_service: WebhookService):
        self.webhook_service = webhook_service

    # * method: execute
    def execute(self, board_id: str, url: str, event: str, config: str = None, **kwargs) -> Webhook:
        '''
        Create a webhook.

        :param board_id: The board ID.
        :type board_id: str
        :param url: The callback URL.
        :type url: str
        :param event: The event type.
        :type event: str
        :param config: Optional config JSON string.
        :type config: str
        :return: The created Webhook domain object.
        :rtype: Webhook
        '''

        # Create the webhook via the service.
        data = self.webhook_service.create_webhook(board_id=board_id, url=url, event=event, config=config)

        # Return the webhook domain object.
        return Webhook.model_validate(data)


# ** event: delete_webhook
class DeleteWebhook(MondayEvent):
    '''
    Event to delete a webhook.
    '''

    # * attribute: webhook_service
    webhook_service: WebhookService

    # * init
    def __init__(self, webhook_service: WebhookService):
        self.webhook_service = webhook_service

    # * method: execute
    def execute(self, webhook_id: str, **kwargs) -> dict:
        '''
        Delete a webhook.

        :param webhook_id: The webhook ID.
        :type webhook_id: str
        :return: The deleted webhook data.
        :rtype: dict
        '''

        # Delete the webhook via the service.
        return self.webhook_service.delete_webhook(webhook_id=webhook_id)
