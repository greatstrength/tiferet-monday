# *** imports

# ** core
from typing import Dict, Any

# ** infra
from tiferet.commands import raise_error
import requests

# *** constants

# *** classes

# ** class monday_api_requests_proxy
class MondayApiRequestsProxy(object):
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
    def execute_query(self, api_key: str, query: str, variables: Dict[str, Any] = {}, api_version: str = None, timeout: int = None, handle_response = lambda data: data) -> Dict[str, Any]:
        """
        Executes a GraphQL query against the Monday.com API.

        :param api_key: The API key for accessing the Monday.com API.
        :type api_key: str
        :param query: The GraphQL query string.
        :type query: str
        :param variables: Variables to be used in the query.
        :type variables: Dict[str, Any]
        :param api_version: Optional API version to use.
        :type api_version: str
        :param timeout: Optional timeout for the request.
        :type timeout: int
        :param handle_response: Optional function to process the response data.
        :type handle_response: function
        :return: The response data from the API.
        :rtype: Dict[str, Any]
        """
        
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }

        # Add the API version to the headers if provided.
        if api_version:
            headers['API-Version'] = api_version

        
        response = requests.post(
            url='https://api.monday.com/v2',
            json={'query': query, 'variables': variables},
            headers=headers,
            timeout=timeout
        )
        
        return self.handle_response(response.json())
    
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
            
            # Retrieve the complexity limit error if present.
            complexity_limit_error = next((error for error in response['errors'] if error.get('extensions', {}).get('code') == 'COMPLEXITY_BUDGET_EXHAUSTED'), None)
            if complexity_limit_error:
                raise_error.execute(
                    'COMPLEXITY_BUDGET_EXHAUSTED', 
                    str(response),
                    complexity_limit_error.get('extensions', {}).get('retry_in_seconds', 60))
            
            # Raise a general Monday.com API error.
            raise_error.execute('MONDAY_API_ERROR', f'A Monday.com API error occurred: {str(response)}')
        
        # Return the start node of the response data.
        data = response.get('data', {})
        return start_node(data)