# *** imports

# ** infra
from moncli import client
from tiferet.commands import raise_error

# ** app
from ...contracts.item import ItemRepository

# *** proxies

# ** proxy: item_moncli_proxy
class ItemMoncliProxy(ItemRepository):
    """
    Proxy for managing item-related operations using the Moncli client.
    """

    # * attribute: monday_api_key
    monday_api_key: str

    def __init__(self, monday_api_key: str):
        """
        Initializes the ItemMoncliProxy with the Monday.com API key.

        :param monday_api_key: API key for accessing the Monday.com API.
        :type monday_api_key: str
        """
        self.monday_api_key = monday_api_key

    def update_simple_column_value(self, item_id: str | int, column_id: str, value: str):
        """
        Updates the value of a simple column for the specified item using the Moncli client.

        :param item_id: ID of the item to be updated.
        :type item_id: str | int
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param value: New value for the column.
        :type value: str
        """

        # Set the api key to the client.
        client.api_key = self.monday_api_key

        # Execute the change simple column value method from the client.
        try:
            item = client.get_items(
                ids=[item_id]
            )[0]
        except IndexError:
            raise_error.execute('ITEM_NOT_FOUND', f'Item with ID {item_id} not found.', item_id)

        # Import and moncli api_v2 handlers.
        from moncli import api_v2 as api
        return api.change_simple_column_value(
            api_key=self.monday_api_key,
            item_id=item_id,
            column_id=column_id,
            board_id=item.board.id,
            value=value
        )
