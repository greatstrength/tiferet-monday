"""Tiferet Monday API Item Requests Proxy Tests"""

# *** imports

# ** infra
import pytest
from unittest.mock import Mock, patch
from tiferet import ModelObject

# ** app
from ....data import (
    ItemData,
    ItemDetailData,
    ColumnValueData
)
from ....models import (
    Item,
    ItemDetail,
    ColumnValue
)
from ..item import ItemMondayApiProxy

# *** fixtures

# ** fixture: item_monday_api_proxy
@pytest.fixture
def item_monday_api_proxy() -> ItemMondayApiProxy:
    '''
    Fixture to create an ItemMondayApiProxy instance.

    :return: An ItemMondayApiProxy instance.
    :rtype: ItemMondayApiProxy
    '''
    
    # Create and return an ItemMondayApiProxy instance.
    return ItemMondayApiProxy(monday_api_key='test_api_key')

# ** fixture: mock_item_data
@pytest.fixture
def mock_item_data() -> ItemData:
    '''
    Fixture to create a mock ItemData instance.

    :return: A mock ItemData instance.
    :rtype: ItemData
    '''
    
    # Create and return a mock ItemData instance.
    item_data = Mock(spec=ItemData)
    item_data.map.return_value = ModelObject.new(
        Item,
        id=1,
        name='Test Item',
        board_id='board_1'
    )
    return item_data

# ** fixture: mock_item_detail_data
@pytest.fixture
def mock_item_detail_data(column_value: ColumnValue) -> ItemDetailData:
    '''
    Fixture to create a mock ItemDetailData instance.

    :param column_value: The ColumnValue instance to include.
    :type column_value: ColumnValue
    :return: A mock ItemDetailData instance.
    :rtype: ItemDetailData
    '''
    
    # Create and return a mock ItemDetailData instance.
    item_detail_data = Mock(spec=ItemDetailData)
    item_detail_data.map.return_value = ModelObject.new(
        ItemDetail,
        id=1,
        name='Test Item Detail',
        board_id='board_1',
        group_id='group_1',
        parent_item_id='item_1',
        column_values=[column_value]
    )
    return item_detail_data

# ** fixture: column_value
@pytest.fixture
def column_value() -> ColumnValue:
    '''
    Fixture to create a basic ColumnValue instance.

    :return: A ColumnValue instance.
    :rtype: ColumnValue
    '''
    
    # Create and return a ColumnValue instance.
    return ModelObject.new(
        ColumnValue,
        id='status_1',
        name='Status',
        type='status',
        value='in_progress'
    )

# ** fixture: mock_column_value_data
@pytest.fixture
def mock_column_value_data(column_value: ColumnValue) -> ColumnValueData:
    '''
    Fixture to create a mock ColumnValueData instance.

    :param column_value: The ColumnValue instance to include.
    :type column_value: ColumnValue
    :return: A mock ColumnValueData instance.
    :rtype: ColumnValueData
    '''
    
    # Create and return a mock ColumnValueData instance.
    column_value_data = Mock(spec=ColumnValueData)
    column_value_data.map.return_value = column_value
    return column_value_data

# *** tests

# ** test: item_monday_api_proxy_instantiation
def test_item_monday_api_proxy_instantiation(item_monday_api_proxy: ItemMondayApiProxy):
    '''
    Test successful instantiation of an ItemMondayApiProxy object.

    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_monday_api_proxy, ItemMondayApiProxy)
    assert item_monday_api_proxy.api_key == 'test_api_key'

# ** test: query_detail_by_id_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.item.ItemDetailData.from_data')
def test_query_detail_by_id_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_item_detail_data: ItemDetailData
):
    '''
    Test successful query of item details by ID using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_item_detail_data: The mock ItemDetailData instance.
    :type mock_item_detail_data: ItemDetailData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'id': 2,
        'name': 'Test Item Detail',
        'board': {'id': 'board_1'},
        'group': {'id': 'group_1'},
        'parent_item': {'id': 'item_1'},
        'column_values': [{'id': 'status_1', 'column': {'title': 'Status', 'description': 'A status column'}, 'type': 'status', 'text': 'In Progress'}]
    }]
    mock_from_data.return_value = mock_item_detail_data
    
    # Query item details.
    result = item_monday_api_proxy.query_detail_by_id(item_id=2)
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'item_id': 2},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, ItemDetail)
    assert result.id == '2'
    assert result.name == 'Test Item Detail'

# ** test: query_detail_by_id_no_data
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
def test_query_detail_by_id_no_data(
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy
):
    '''
    Test query_detail_by_id returns None when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = []
    
    # Query item details.
    result = item_monday_api_proxy.query_detail_by_id(item_id=3)
    
    # Verify the result is None.
    assert result is None

# ** test: query_by_ids_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.item.ItemData.from_data')
def test_query_by_ids_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_item_data: ItemData
):
    '''
    Test successful query of items by IDs using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_item_data: The mock ItemData instance.
    :type mock_item_data: ItemData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'id': '1',
        'name': 'Test Item',
        'board': {'id': 'board_1'},
        'updates': []
    }]
    mock_from_data.return_value = mock_item_data
    
    # Query items by IDs.
    result = item_monday_api_proxy.query_by_ids(item_ids=['1'])
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'item_ids': [1]},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Item)
    assert result[0].id == '1'

# ** test: query_by_ids_no_data
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
def test_query_by_ids_no_data(
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy
):
    '''
    Test query_by_ids returns an empty list when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = []
    
    # Query items by IDs.
    result = item_monday_api_proxy.query_by_ids(item_ids=['999'])
    
    # Verify the result is an empty list.
    assert result == []

# ** test: query_column_values_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.column_value.ColumnValueData.from_data')
def test_query_column_values_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_column_value_data: ColumnValueData
):
    '''
    Test successful query of column values for an item using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_column_value_data: The mock ColumnValueData instance.
    :type mock_column_value_data: ColumnValueData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'id': 'status_1',
        'column': {'title': 'Status', 'description': 'A status column', 'settings_str': '{}'},
        'type': 'status',
        'value': 'in_progress'
    }]
    mock_from_data.return_value = mock_column_value_data
    
    # Query column values.
    result = item_monday_api_proxy.query_column_values(item_id='2', column_ids=['status_1'])
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'item_id': 2, 'column_ids': ['status_1']},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], ColumnValue)
    assert result[0].id == 'status_1'

# ** test: query_column_values_no_data
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
def test_query_column_values_no_data(
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy
):
    '''
    Test query_column_values returns an empty tuple when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = []
    
    # Query column values.
    result = item_monday_api_proxy.query_column_values(item_id='2', column_ids=['status_unknown'])
    
    # Verify the result is an empty tuple.
    assert result == []

# ** test: query_subitems_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.item.ItemData.from_data')
def test_query_subitems_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_item_data: ItemData
):
    '''
    Test successful query of subitems for a parent item using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_item_data: The mock ItemData instance.
    :type mock_item_data: ItemData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'id': '3',
        'name': 'Test Subitem',
        'board': {'id': 'board_1'},
        'updates': []
    }]
    mock_from_data.return_value = mock_item_data
    
    # Query subitems.
    result = item_monday_api_proxy.query_subitems(parent_item_id='1')
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'parent_item_id': 1},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Item)
    assert result[0].id == '3'

# ** test: query_subitems_no_data
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
def test_query_subitems_no_data(
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy
):
    '''
    Test query_subitems returns an empty list when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = []
    
    # Query subitems.
    result = item_monday_api_proxy.query_subitems(parent_item_id='4')
    
    # Verify the result is an empty list.
    assert result == []

# ** test: update_simple_column_value_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.item.ItemData.from_data')
def test_update_simple_column_value_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_item_data: ItemData
):
    '''
    Test successful update of a simple column value using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_item_data: The mock ItemData instance.
    :type mock_item_data: ItemData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = {
        'id': '1',
        'name': 'Test Item',
        'board': {'id': 'board_1'}
    }
    mock_from_data.return_value = mock_item_data
    
    # Update simple column value.
    result = item_monday_api_proxy.update_simple_column_value(
        item_id='1',
        board_id='1',
        column_id='status_1',
        value='done'
    )
    
    # Verify the mutation was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={
            'item_id': 1,
            'board_id': 1,
            'column_id': 'status_1',
            'value': 'done'
        },
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, Item)
    assert result.id == '1'

# ** test: create_subitem_success
@patch('tiferet_monday.proxies.requests.item.ItemMondayApiProxy.execute_query')
@patch('tiferet_monday.data.item.ItemData.from_data')
def test_create_subitem_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    item_monday_api_proxy: ItemMondayApiProxy,
    mock_item_data: ItemData
):
    '''
    Test successful creation of a subitem using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param item_monday_api_proxy: The ItemMondayApiProxy instance to test.
    :type item_monday_api_proxy: ItemMondayApiProxy
    :param mock_item_data: The mock ItemData instance.
    :type mock_item_data: ItemData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = {
        'id': '3',
        'name': 'Test Subitem',
        'board': {'id': 'board_1'}
    }
    mock_from_data.return_value = mock_item_data
    
    # Create subitem.
    result = item_monday_api_proxy.create_subitem(
        parent_item_id='1',
        item_name='Test Subitem',
        column_values={'status_1': 'in_progress'}
    )
    
    # Verify the mutation was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={
            'parent_item_id': 1,
            'item_name': 'Test Subitem',
            'column_values': '{"status_1": "in_progress"}'
        },
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, Item)
    assert result.id == '3'
