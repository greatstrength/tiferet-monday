# *** imports

# ** core
from typing import Any, Dict

# ** infra
import requests

# *** functions

# ** function: execute_query
def execute_query(api_key: str, query: str, variables: Dict[str, Any] = {}, api_version: str = None, timeout: int = None, handle_response = lambda data: data) -> Dict[str, Any]:
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
    
    return handle_response(response.json())
