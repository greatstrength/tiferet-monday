# *** imports

# ** core
from typing import Any, Dict

# ** infra
import requests

# *** functions

# ** function: execute_query
def execute_query(api_key: str, query: str, variables: Dict[str, Any] = {}, timeout: int = None) -> Dict[str, Any]:
    """
    Executes a GraphQL query against the Monday.com API.

    :param api_key: The API key for authentication.
    :param query_name: The name of the query to execute.
    :param query: The GraphQL query string.
    :param variables: Variables to be used in the query.
    :param timeout: Optional timeout for the request.
    :type api_key: str
    :return: The response data from the API.
    :rtype: Dict[str, Any]
    """
    
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        url='https://api.monday.com/v2',
        json={'query': query, 'variables': variables},
        headers=headers,
        timeout=timeout
    )
    
    return response.json()
