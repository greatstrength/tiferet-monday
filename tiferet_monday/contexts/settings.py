"""Tiferet Monday Contexts Settings"""

# *** imports

# ** core
from typing import Any

# ** app
from ..repos.settings import MondayApiProxy
from ..repos.board import BoardApiProxy
from ..repos.item import ItemApiProxy


# *** contexts

# ** context: monday_context
class MondayContext:
    '''
    Base context for Monday.com context-as-client objects.
    Holds a reference to the API key and lazily-initialized service proxies.
    '''

    # * attribute: _api_key
    _api_key: str

    # * attribute: _board_service
    _board_service: BoardApiProxy

    # * attribute: _item_service
    _item_service: ItemApiProxy

    # * init
    def __init__(self, api_key: str, board_service: BoardApiProxy = None, item_service: ItemApiProxy = None):
        '''
        Initialize the Monday context.

        :param api_key: The Monday.com API key.
        :type api_key: str
        :param board_service: Optional pre-initialized board service.
        :type board_service: BoardApiProxy
        :param item_service: Optional pre-initialized item service.
        :type item_service: ItemApiProxy
        '''

        # Set the API key.
        self._api_key = api_key

        # Set or lazily initialize services.
        self._board_service = board_service or BoardApiProxy(api_key)
        self._item_service = item_service or ItemApiProxy(api_key)
