"""Tiferet Monday API Proxy Tests"""

# *** imports

# ** infra
import pytest
from unittest.mock import (
    Mock,
    patch
)
from tiferet import TiferetError

# ** app
from ..settings import (
    MondayApiRequestsProxy,
    MONDAY_API_VERSION_HEADER,
    MONDAY_API_BASE_URL,
    COMPLEXITY_BUDGET_EXHAUSTED_ERROR_CODE,
    MONDAY_API_ERROR_CODE
)

# *** fixtures

# ** fixture: monday_api_requests_proxy
@pytest.fixture
def monday_api_requests_proxy() -> MondayApiRequestsProxy:
    '''
    Fixture to create a MondayApiRequestsProxy instance.

    :return: A MondayApiRequestsProxy instance.
    :rtype: MondayApiRequestsProxy
    '''
    
    # Create and return a MondayApiRequestsProxy instance.
    return MondayApiRequestsProxy(monday_api_key='test_api_key')

# ** fixture: mock_response
@pytest.fixture
def mock_response():
    '''
    Fixture to create a mock response object for requests.post.

    :return: A mock response object.
    :rtype: Mock
    '''
    
    # Create and return a mock response object.
    response = Mock()
    response.json.return_value = {'data': {'result': 'success'}}
    return response

# *** tests

# ** test: monday_api_requests_proxy_instantiation
def test_monday_api_requests_proxy_instantiation(monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test successful instantiation of a MondayApiRequestsProxy object.

    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(monday_api_requests_proxy, MondayApiRequestsProxy)
    assert monday_api_requests_proxy.api_key == 'test_api_key'

# ** test: execute_query_success
@patch('requests.post')
def test_execute_query_success(mock_post: Mock, monday_api_requests_proxy: MondayApiRequestsProxy, mock_response: Mock):
    '''
    Test successful execution of a GraphQL query.

    :param mock_post: The mocked requests.post function.
    :type mock_post: Mock
    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    :param mock_response: The mock response object.
    :type mock_response: Mock
    '''
    
    # Set up the mock response.
    mock_post.return_value = mock_response
    
    # Execute the query.
    query = 'query { boards { id } }'
    variables = {'var': 'value'}
    result = monday_api_requests_proxy.execute_query(query, variables, api_version='2023-10')
    
    # Verify the request was made correctly.
    mock_post.assert_called_once_with(
        url=MONDAY_API_BASE_URL,
        json={'query': query, 'variables': variables},
        headers={
            'Authorization': 'test_api_key',
            'Content-Type': 'application/json',
            MONDAY_API_VERSION_HEADER: '2023-10'
        },
        timeout=None
    )
    
    # Verify the result.
    assert result == {'result': 'success'}

# ** test: execute_query_no_api_version
@patch('requests.post')
def test_execute_query_no_api_version(mock_post: Mock, monday_api_requests_proxy: MondayApiRequestsProxy, mock_response: Mock):
    '''
    Test execution of a GraphQL query without specifying an API version.

    :param mock_post: The mocked requests.post function.
    :type mock_post: Mock
    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    :param mock_response: The mock response object.
    :type mock_response: Mock
    '''
    
    # Set up the mock response.
    mock_post.return_value = mock_response
    
    # Execute the query without api_version.
    query = 'query { boards { id } }'
    result = monday_api_requests_proxy.execute_query(query)
    
    # Verify the request was made correctly without API version header.
    mock_post.assert_called_once_with(
        url=MONDAY_API_BASE_URL,
        json={'query': query, 'variables': {}},
        headers={
            'Authorization': 'test_api_key',
            'Content-Type': 'application/json'
        },
        timeout=None
    )
    
    # Verify the result.
    assert result == {'result': 'success'}

# ** test: handle_response_success
def test_handle_response_success(monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test successful handling of a Monday.com API response.

    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''
    
    # Create a mock response with valid data.
    response = {'data': {'result': 'success'}}
    start_node = lambda data: data['result']
    
    # Handle the response.
    result = monday_api_requests_proxy.handle_response(response, start_node=start_node)
    
    # Verify the result.
    assert result == 'success'

# ** test: handle_response_complexity_error
@patch('tiferet.raise_error.execute')
def test_handle_response_complexity_error(mock_raise_error: Mock, monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test handling of a complexity budget exhausted error in the API response.

    :param mock_raise_error: The mocked raise_error.execute function.
    :type mock_raise_error: Mock
    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''

    # Set up the mock to raise a TiferetError.
    mock_raise_error.side_effect = TiferetError(COMPLEXITY_BUDGET_EXHAUSTED_ERROR_CODE, 'Complexity budget exhausted', 30)
    
    # Create a mock response with a complexity error.
    response = {
        'errors': [
            {
                'message': 'Complexity budget exhausted',
                'extensions': {
                    'code': COMPLEXITY_BUDGET_EXHAUSTED_ERROR_CODE,
                    'retry_in_seconds': 30
                }
            }
        ]
    }
    
    # Handle the response and expect an error to be raised.
    with pytest.raises(TiferetError):
        monday_api_requests_proxy.handle_response(response, start_node=lambda data: data)
    
    # Verify the error was raised correctly.
    mock_raise_error.assert_called_once_with(
        COMPLEXITY_BUDGET_EXHAUSTED_ERROR_CODE,
        str(response),
        30
    )

# ** test: handle_response_general_error
@patch('tiferet.raise_error.execute')
def test_handle_response_general_error(mock_raise_error: Mock, monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test handling of a general Monday.com API error in the response.

    :param mock_raise_error: The mocked raise_error.execute function.
    :type mock_raise_error: Mock
    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''
    
    # Create a mock response with a general error.
    response = {
        'errors': [
            {'message': 'Invalid query'}
        ]
    }

    # Set up the mock to raise a TiferetError.
    mock_raise_error.side_effect = TiferetError(MONDAY_API_ERROR_CODE, f'A Monday.com API error occurred: {str(response)}')
    
    # Handle the response and expect an error to be raised.
    with pytest.raises(Exception):
        monday_api_requests_proxy.handle_response(response, start_node=lambda data: data)
    
    # Verify the error was raised correctly.
    mock_raise_error.assert_called_once_with(
        MONDAY_API_ERROR_CODE,
        f'A Monday.com API error occurred: {str(response)}'
    )

# ** test: is_complexity_budget_exhausted_true
def test_is_complexity_budget_exhausted_true(monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test checking for a complexity budget exhausted error returns True.

    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''
    
    # Create an error with complexity budget exhausted code.
    error = {
        'extensions': {
            'code': COMPLEXITY_BUDGET_EXHAUSTED_ERROR_CODE
        }
    }
    
    # Verify the method returns True.
    assert monday_api_requests_proxy.is_complexity_budget_exhausted(error) is True

# ** test: is_complexity_budget_exhausted_false
def test_is_complexity_budget_exhausted_false(monday_api_requests_proxy: MondayApiRequestsProxy):
    '''
    Test checking for a non-complexity error returns False.

    :param monday_api_requests_proxy: The MondayApiRequestsProxy instance to test.
    :type monday_api_requests_proxy: MondayApiRequestsProxy
    '''
    
    # Create an error without complexity budget exhausted code.
    error = {
        'extensions': {
            'code': 'OTHER_ERROR'
        }
    }
    
    # Verify the method returns False.
    assert monday_api_requests_proxy.is_complexity_budget_exhausted(error) is False

    error = {
        'message': 'Some error without extensions'
    }

    # Verify the method returns False for error without extensions.
    assert monday_api_requests_proxy.is_complexity_budget_exhausted(error) is False