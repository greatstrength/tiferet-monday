# *** imports

# ** infra
from moncli import api_v2 as api

# ** app
from ...data.item import ItemData, ItemDetailData, DataObject
from ...contracts.item import *
from .settings import MondayApiProxy

# *** proxies

# ** proxy: item_moncli_proxy
class ItemMondayProxy(ItemRepository, MondayApiProxy):
    """
    Proxy for managing item-related operations using the Moncli client.
    """

    # * init
    def __init__(self, monday_api_key: str):
        """
        Initializes the ItemMondayProxy with the Monday.com API key.

        :param monday_api_key: API key for accessing the Monday.com API.
        :type monday_api_key: str
        """
        
        # Initialize the parent class with the API key.
        super().__init__(monday_api_key)

    # * method: query_detail_by_id
    def query_detail_by_id(self, item_id: str | int) -> ItemDetailContract:
        """
        Queries detailed information about an item by its ID using the Moncli client.
        :param item_id: ID of the item to retrieve details for.
        :type item_id: str | int
        :return: Detailed information about the item.
        :rtype: ItemDetailContract
        """

        # Execute the query to retrieve item details.
        data = self.execute_query(
            query="""
                query ($item_id: ID!) {
                    items(ids: [$item_id]) {
                        id
                        name
                        board { id }
                        group { id }
                        column_values {
                            id
                            column {
                                title
                                description
                                settings_str
                            }
                            type
                            value
                        }
                    }
                }
            """,
            variables={'item_id': int(item_id)},
            start_node=lambda data: data.get('items', [])
        )

        # If no data is returned, return None.
        if not data:
            return None

        # Map the retrieved data to the ItemDetailContract.
        return DataObject.from_data(
            ItemDetailData,
            **data[0]
        ).map()

    # * method: query_by_ids
    def query_by_ids(self, item_ids: list[str | int]) -> list[ItemContract]:
        """
        Queries items by their IDs using the Moncli client.

        :param item_ids: List of item IDs to query.
        :type item_ids: list[str | int]
        :return: List of items matching the provided IDs.
        :rtype: list[ItemContract]
        """

        # Execute the query to retrieve items by their IDs.
        data = self.execute_query(
            query="""
                query ($item_ids: [ID!]) {
                    items(ids: $item_ids) {
                        id
                        name
                        board {
                            id
                        }
                    }
                }
            """,
            variables={'item_ids': [int(item_id) for item_id in item_ids]},
            start_node=lambda data: data.get('items', [])
        )

        return [DataObject.from_data(
            ItemData,
            **item
        ).map() for item in data]

    # * method: update_simple_column_value
    def update_simple_column_value(self, item_id: str | int, board_id: str | int, column_id: str, value: str):
        """
        Updates the value of a simple column for the specified item using the Moncli client.

        :param item_id: ID of the item to be updated.
        :type item_id: str | int
        :param board_id: ID of the board to which the item belongs.
        :type board_id: str | int
        :param column_id: ID of the column to be updated.
        :type column_id: str
        :param value: New value for the column.
        :type value: str
        """

        # Import and moncli api_v2 handlers.
        return api.change_simple_column_value(
            api_key=self.api_key,
            item_id=item_id,
            board_id=board_id,
            column_id=column_id,
            value=value
        )
    
    # * method: create_subitem
    def create_subitem(self, parent_item_id: str | int, item_name: str) -> Any:
        """
        Creates a subitem under the specified item using the Moncli client.

        :param parent_item_id: ID of the parent item under which the subitem will be created.
        :type parent_item_id: str | int
        :param item_name: Name of the subitem to be created.
        :type item_name: str
        :return: Result of the subitem creation operation.
        :rtype: Any
        """

        # Import and moncli api_v2 handlers.
        return api.requests.execute_query(
            api_key=self.api_key,
            query="""
                mutation ($parent_item_id: ID!, $item_name: String!) {
                    create_subitem(parent_item_id: $parent_item_id, item_name: $item_name) {
                        id
                        name  
                    }
                }
            """,
            variables={
                'parent_item_id': int(parent_item_id),
                'item_name': item_name
            },
            query_name='create_subitem',
        )
