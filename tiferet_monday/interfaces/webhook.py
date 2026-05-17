"""Tiferet Monday Webhook Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: webhook_service
class WebhookService(MondayService):
    '''
    Service interface for webhook-related Monday.com API operations.
    '''

    # * method: create_webhook
    @abstractmethod
    def create_webhook(self, board_id: str, url: str, event: str, config: str = None) -> dict:
        '''
        Create a webhook on a board.

        :param board_id: The board ID.
        :type board_id: str
        :param url: The webhook callback URL.
        :type url: str
        :param event: The event type.
        :type event: str
        :param config: Optional JSON config string.
        :type config: str
        :return: The created webhook data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: delete_webhook
    @abstractmethod
    def delete_webhook(self, webhook_id: str) -> dict:
        '''
        Delete a webhook.

        :param webhook_id: The webhook ID.
        :type webhook_id: str
        :return: The deleted webhook data.
        :rtype: dict
        '''
        raise NotImplementedError()
