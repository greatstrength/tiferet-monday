"""Tiferet Monday Feature Context Tests"""

# *** imports

# ** infra
import pytest
from unittest.mock import Mock, patch
from tiferet import Command, TiferetError
from tiferet.contexts import (
    FeatureContext,
    ContainerContext,
    RequestContext
)
from tiferet.contexts.feature import FeatureService

# ** app
from ..feature import MondayFeatureContext

# *** fixtures

# ** fixture: feature_service
@pytest.fixture
def feature_service() -> FeatureService:
    '''
    Fixture to provide a mock FeatureService.

    :return: A mock FeatureService instance.
    :rtype: FeatureService
    '''
    
    # Create a mock FeatureService.
    service = Mock(spec=FeatureService)
    
    # Return the mock FeatureService.
    return service

# ** fixture: container_context
@pytest.fixture
def container_context(test_command: Command) -> ContainerContext:
    '''
    Fixture to provide a mock ContainerContext.

    :param test_command: The mock Command instance to return as a dependency.
    :type test_command: Command
    :return: A mock ContainerContext instance.
    :rtype: ContainerContext
    '''
    
    # Create a mock ContainerContext.
    container_context = Mock(spec=ContainerContext)
    
    # Set the container service to return the test command when requested.
    container_context.get_dependency.return_value = test_command
    
    # Return the mock ContainerContext.
    return container_context

# ** fixture: monday_feature_context
@pytest.fixture
def monday_feature_context(feature_service: FeatureService, container_context: ContainerContext) -> MondayFeatureContext:
    '''
    Fixture to provide an instance of MondayFeatureContext.

    :param feature_service: The mock FeatureService instance.
    :type feature_service: FeatureService
    :param container_context: The mock ContainerContext instance.
    :type container_context: ContainerContext
    :return: A MondayFeatureContext instance.
    :rtype: MondayFeatureContext
    '''
    
    # Create an instance of MondayFeatureContext with mock dependencies.
    return MondayFeatureContext(
        feature_service=feature_service,
        container=container_context
    )

# ** fixture: test_command
@pytest.fixture
def test_command() -> Command:
    '''
    Fixture to provide a mock Command instance.

    :return: A mock Command instance.
    :rtype: Command
    '''
    
    # Create and return a mock Command instance.
    return Mock(spec=Command)

# ** fixture: request_context
@pytest.fixture
def request_context() -> RequestContext:
    '''
    Fixture to provide a mock RequestContext instance.

    :return: A mock RequestContext instance.
    :rtype: RequestContext
    '''
    
    # Create and return a mock RequestContext instance.
    return Mock(spec=RequestContext)

# *** tests

# ** test: monday_feature_context_instantiation
def test_monday_feature_context_instantiation(monday_feature_context: MondayFeatureContext):
    '''
    Test successful instantiation of a MondayFeatureContext object.

    :param monday_feature_context: The MondayFeatureContext instance to test.
    :type monday_feature_context: MondayFeatureContext
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(monday_feature_context, MondayFeatureContext)
    assert isinstance(monday_feature_context.feature_service, FeatureService)
    assert isinstance(monday_feature_context.container, ContainerContext)

# ** test: handle_retry_success
@patch('tiferet_monday.contexts.feature.sleep')
def test_handle_retry_success(
    mock_sleep: Mock,
    monday_feature_context: MondayFeatureContext,
):
    '''
    Test successful retry handling in MondayFeatureContext.

    :param mock_sleep: The mocked sleep function.
    :type mock_sleep: Mock
    :param monday_feature_context: The MondayFeatureContext instance to test.
    :type monday_feature_context: MondayFeatureContext
    :param test_command: The mock Command instance.
    :type test_command: Command
    :param feature: The Feature instance.
    :type feature: Feature
    '''
    
    # Create a handler that executes the command.
    handler = Mock(return_value={"status": "success", "data": {"key": "value"}})
    
    # Call handle_retry with a retry duration and handler.
    result = monday_feature_context.handle_retry(retry_in_seconds=30, handler=handler)
    
    # Verify the sleep function was called with the correct duration.
    mock_sleep.assert_called_once_with(30)
    
    # Verify the handler was called and the result is correct.
    handler.assert_called_once()
    assert result == {"status": "success", "data": {"key": "value"}}

# ** test: handle_command_success
def test_handle_command_success(
    monday_feature_context: MondayFeatureContext,
    test_command: Command,
    request: RequestContext
):
    '''
    Test successful command handling in MondayFeatureContext.

    :param monday_feature_context: The MondayFeatureContext instance to test.
    :type monday_feature_context: MondayFeatureContext
    :param test_command: The mock Command instance.
    :type test_command: Command
    :param request: The mock RequestContext instance.
    :type request: RequestContext
    '''
    
    # Create a mock request.
    request = RequestContext(data={"key": "value"})

    # Mock the base FeatureContext's handle_command method to return a success response.
    with patch.object(FeatureContext, 'handle_command', return_value={"status": "success", "data": {"key": "value"}}) as mock_super_handle:
    
        # Handle the command.
        result = monday_feature_context.handle_command(test_command, request)

        # Verify the parent handle_command was called once.
        mock_super_handle.assert_called_once_with(
            command=test_command, 
            request=request,
            data_key=None,
            pass_on_error=False
        )
        
        # Verify the result.
        assert result == {"status": "success", "data": {"key": "value"}}

# ** test: handle_command_complexity_error_retry
@patch('tiferet_monday.contexts.feature.sleep')
def test_handle_command_complexity_error_retry(
    mock_sleep: Mock,
    monday_feature_context: MondayFeatureContext,
    test_command: Command,
    request: RequestContext
):
    '''
    Test handling a complexity budget exhausted error with retry in MondayFeatureContext.

    :param mock_sleep: The mocked sleep function.
    :type mock_sleep: Mock
    :param monday_feature_context: The MondayFeatureContext instance to test.
    :type monday_feature_context: MondayFeatureContext
    :param test_command: The mock Command instance.
    :type test_command: Command
    :param request: The mock RequestContext instance.
    :type request: RequestContext
    '''
    
    # Mock the parent handle_command to raise a complexity error on first call and succeed on retry.
    with patch.object(FeatureContext, 'handle_command') as mock_super_handle:
        mock_super_handle.side_effect = [
            TiferetError('COMPLEXITY_BUDGET_EXHAUSTED', 'Complexity budget exhausted', 30),
            {"status": "success", "data": {"key": "value"}}
        ]
        
        # Handle the command.
        result = monday_feature_context.handle_command(test_command, request)
        
        # Verify the sleep function was called with the retry duration.
        mock_sleep.assert_called_once_with(30)
        
        # Verify the parent handle_command was called twice (first failure, then retry).
        assert mock_super_handle.call_count == 2
        
        # Verify the result.
        assert result == {"status": "success", "data": {"key": "value"}}

# ** test: handle_command_non_complexity_error
def test_handle_command_non_complexity_error(
    monday_feature_context: MondayFeatureContext,
    test_command: Command,
    request: RequestContext
):
    '''
    Test handling a non-complexity error in MondayFeatureContext raises the error.

    :param monday_feature_context: The MondayFeatureContext instance to test.
    :type monday_feature_context: MondayFeatureContext
    :param test_command: The mock Command instance.
    :type test_command: Command
    :param request: The mock RequestContext instance.
    :type request: RequestContext
    '''

    
    # Expect the non-complexity error to be raised without retry.
    with pytest.raises(TiferetError) as exc_info:

        # Mock the execution of the base FeatureContext's handle_command to raise a non-complexity error.
        with patch.object(FeatureContext, 'handle_command', side_effect=TiferetError('KEY_NOT_FOUND', 'No key provided for command execution.')):
            
            # Handle the command.
            monday_feature_context.handle_command(test_command, request)
    
    # Verify the error details.
    assert exc_info.value.error_code == 'KEY_NOT_FOUND'
    assert 'No key provided for command execution.' in str(exc_info.value)