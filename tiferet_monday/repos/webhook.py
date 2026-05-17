"""Tiferet Monday Webhook Repos"""

# *** imports

# ** core
from typing import Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.webhook import WebhookService


# *** repos

# ** repo: webhook_api_proxy
class WebhookApiProxy(WebhookService, MondayApiProxy):
    '''
    Concrete WebhookService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: create_webhook
    def create_webhook(self, board_id: str, url: str, event: str, config: str = None) -> dict:
        '''
        Create a webhook on a board.
        '''

        variables = {
            'boardId': int(board_id),
            'url': url,
            'event': event,
        }
        config_param = ''
        config_arg = ''
        if config:
            variables['config'] = config
            config_param = ', $config: JSON'
            config_arg = ', config: $config'

        return self.execute_query(
            query=f"""
                mutation ($boardId: ID!, $url: String!, $event: WebhookEventType!{config_param}) {{
                    create_webhook (board_id: $boardId, url: $url, event: $event{config_arg}) {{
                        id
                        board_id
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('create_webhook', {}),
        )

    # * method: delete_webhook
    def delete_webhook(self, webhook_id: str) -> dict:
        '''
        Delete a webhook.
        '''

        return self.execute_query(
            query="""
                mutation ($webhookId: ID!) {
                    delete_webhook (id: $webhookId) { id }
                }
            """,
            variables={'webhookId': int(webhook_id)},
            start_node=lambda data: data.get('delete_webhook', {}),
        )
