"""Tiferet Monday Contexts Settings"""

# *** imports

# ** core
from typing import Any

# ** app
from ..repos.settings import MondayApiProxy
from ..repos.board import BoardApiProxy
from ..repos.item import ItemApiProxy
from ..repos.user import UserApiProxy
from ..repos.update import UpdateApiProxy


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

    # * attribute: _user_service
    _user_service: UserApiProxy

    # * attribute: _update_service
    _update_service: UpdateApiProxy

    # * init
    def __init__(self,
                 api_key: str,
                 board_service: BoardApiProxy = None,
                 item_service: ItemApiProxy = None,
                 user_service: UserApiProxy = None,
                 update_service: UpdateApiProxy = None):
        '''
        Initialize the Monday context.

        :param api_key: The Monday.com API key.
        :type api_key: str
        :param board_service: Optional pre-initialized board service.
        :type board_service: BoardApiProxy
        :param item_service: Optional pre-initialized item service.
        :type item_service: ItemApiProxy
        :param user_service: Optional pre-initialized user service.
        :type user_service: UserApiProxy
        :param update_service: Optional pre-initialized update service.
        :type update_service: UpdateApiProxy
        '''

        # Set the API key.
        self._api_key = api_key

        # Set or lazily initialize services.
        self._board_service = board_service or BoardApiProxy(api_key)
        self._item_service = item_service or ItemApiProxy(api_key)
        self._user_service = user_service or UserApiProxy(api_key)
        self._update_service = update_service or UpdateApiProxy(api_key)
