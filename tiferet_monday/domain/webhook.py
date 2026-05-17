"""Tiferet Monday Webhook Domain Objects"""

# *** imports

# ** core
from typing import Optional

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: webhook
class Webhook(MondayDomainObject):
    '''
    Represents a webhook in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the webhook.'
    )

    # * attribute: board_id
    board_id: Optional[str] = Field(
        default=None,
        description='The board ID this webhook is attached to.'
    )

    # * attribute: event
    event: Optional[str] = Field(
        default=None,
        description='The event type that triggers the webhook.'
    )

    # * attribute: config
    config: Optional[str] = Field(
        default=None,
        description='The webhook configuration (JSON string).'
    )
