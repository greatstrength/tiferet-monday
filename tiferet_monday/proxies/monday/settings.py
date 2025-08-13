# *** imports

# ** core
from typing import Dict, Any

# ** infra
from tiferet.commands import raise_error

# ** app
from ...commands import *
from ...clients import monday_client


# *** classes

# ** class monday_api_proxy
class MondayApiProxy(object):
    """
    Proxy class for interacting with the Monday.com API.
    """

    # * attribute: api_key
    api_key: str

    # * init
    def __init__(self, monday_api_key: str):
        """
        Initializes the MondayApiProxy with the provided API key.

        :param monday_api_key: The API key for accessing the Monday.com API.
        :type monday_api_key: str
        """
        # Set the API key for the proxy.
        self.api_key = monday_api_key

    # * method: execute_query
    def execute_query(self, query: str, variables: Dict[str, Any] = {}, api_version: str = None, timeout: int = None, start_node = lambda data: data) -> Dict[str, Any]:
        """
        Executes a GraphQL query against the Monday.com API.

        :param query: The GraphQL query string.
        :type query: str
        :param variables: Variables to be used in the query.
        :type variables: Dict[str, Any]
        :param api_version: Optional API version to use.
        :type api_version: str
        :param timeout: Optional timeout for the request.
        :type timeout: int
        :param start_node: Optional function to process the start node of the response.
        :type start_node: function
        :return: The response data from the API.
        :rtype: Dict[str, Any]
        """
        # Call the monday client to execute the query.
        return monday_client.execute_query(
            api_key=self.api_key,
            query=query,
            variables=variables,
            api_version=api_version,
            timeout=timeout,
            handle_response=lambda data: self.handle_response(
                data,
                start_node=start_node
            )
        )
    
    # * method: handle_response
    def handle_response(self, response: Dict[str, Any], start_node: lambda data: data) -> Any:
        """
        Handles the response from the Monday.com API.

        :param response: The response data from the API.
        :type response: Dict[str, Any]
        :param start_node: Optional function to process the start node of the response.
        :type start_node: function
        :return: The processed response data.
        :rtype: Any
        """
        # Check for errors in the response and raise an error if found.
        if 'errors' in response:
            raise_error.execute('MONDAY_API_ERROR', f'A Monday.com API error occurred: {str(response)}', str(response))
        
        # Return the start node of the response data.
        data = response.get('data', {})
        return start_node(data)