"""Tiferet Monday Repos Settings"""

# *** imports

# ** core
from typing import Any, Callable, Dict, Optional

# ** infra
import requests

# ** app
from ..assets import const


# *** repos

# ** repo: monday_api_proxy
class MondayApiProxy:
    '''
    Base proxy for executing GraphQL queries against the Monday.com API.
    Handles authentication, response parsing, and complexity budget errors.
    '''

    # * attribute: api_key
    api_key: str

    # * init
    def __init__(self, monday_api_key: str):
        '''
        Initialize the proxy with the Monday.com API key.

        :param monday_api_key: The API key for authentication.
        :type monday_api_key: str
        '''

        # Set the API key.
        self.api_key = monday_api_key

    # * method: execute_query
    def execute_query(self,
                      query: str,
                      variables: Dict[str, Any] = None,
                      api_version: str = None,
                      timeout: int = None,
                      start_node: Callable = lambda data: data) -> Any:
        '''
        Execute a GraphQL query against the Monday.com API.

        :param query: The GraphQL query string.
        :type query: str
        :param variables: Optional query variables.
        :type variables: Dict[str, Any]
        :param api_version: Optional API version header.
        :type api_version: str
        :param timeout: Optional request timeout.
        :type timeout: int
        :param start_node: Function to navigate the response data.
        :type start_node: Callable
        :return: The response data.
        :rtype: Any
        '''

        # Build request headers.
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
        }

        # Add API version header if specified.
        if api_version:
            headers[const.MONDAY_API_VERSION_HEADER] = api_version

        # Execute the POST request.
        response = requests.post(
            url=const.MONDAY_API_BASE_URL,
            json={'query': query, 'variables': variables or {}},
            headers=headers,
            timeout=timeout,
        )

        # Parse and return the response.
        return self._handle_response(response.json(), start_node=start_node)

    # * method: _handle_response
    def _handle_response(self, response: Dict[str, Any], start_node: Callable) -> Any:
        '''
        Handle the API response, checking for errors.

        :param response: The raw JSON response.
        :type response: Dict[str, Any]
        :param start_node: Function to navigate the response data.
        :type start_node: Callable
        :return: The processed response data.
        :rtype: Any
        '''

        # Check for errors in the response.
        if 'errors' in response:

            # Check for complexity budget exhausted error.
            complexity_error = next(
                (e for e in response['errors']
                 if e.get('extensions', {}).get('code') == const.COMPLEXITY_BUDGET_EXHAUSTED_ID),
                None
            )

            # Raise a structured error for non-complexity errors.
            if not complexity_error:
                raise MondayApiError(
                    const.MONDAY_API_ERROR_ID,
                    str(response),
                )

            # Raise complexity budget error with retry hint.
            retry_seconds = complexity_error.get('extensions', {}).get('retry_in_seconds', 60)
            raise MondayApiError(
                const.COMPLEXITY_BUDGET_EXHAUSTED_ID,
                str(response),
                retry_seconds,
            )

        # Return the navigated response data.
        data = response.get('data', {})
        return start_node(data)


# ** class: monday_api_error
class MondayApiError(Exception):
    '''
    Structured error for Monday.com API failures.
    '''

    # * init
    def __init__(self, error_code: str, message: str, *args):
        '''
        Initialize the API error.

        :param error_code: The error code constant.
        :type error_code: str
        :param message: The error message.
        :type message: str
        '''

        # Set the error code and call super.
        self.error_code = error_code
        super().__init__(message, *args)
