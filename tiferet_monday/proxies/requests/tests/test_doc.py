"""Tiferet Monday Document Proxy Tests"""

# *** imports

# ** infra
import pytest
from unittest.mock import Mock, patch
from tiferet import ModelObject

# ** app
from ....data import DocumentData
from ....models import Document, DocumentBlock
from ..doc import DocumentMondayApiProxy

# *** fixtures

# ** fixture: document_monday_api_proxy
@pytest.fixture
def document_monday_api_proxy() -> DocumentMondayApiProxy:
    '''
    Fixture to create a DocumentMondayApiProxy instance.

    :return: A DocumentMondayApiProxy instance.
    :rtype: DocumentMondayApiProxy
    '''
    
    # Create and return a DocumentMondayApiProxy instance.
    return DocumentMondayApiProxy(monday_api_key='test_api_key')

# ** fixture: mock_document_data
@pytest.fixture
def mock_document_data() -> DocumentData:
    '''
    Fixture to create a mock DocumentData instance.

    :return: A mock DocumentData instance.
    :rtype: DocumentData
    '''
    
    # Create and return a mock DocumentData instance.
    document_data = Mock(spec=DocumentData)
    document_data.map.return_value = ModelObject.new(
        Document,
        id='doc_1',
        name='Test Document',
        object_id='obj_1'
    )
    return document_data

# ** fixture: document_block
@pytest.fixture
def document_block() -> DocumentBlock:
    '''
    Fixture to create a basic DocumentBlock instance.

    :return: A DocumentBlock instance.
    :rtype: DocumentBlock
    '''
    
    # Create and return a DocumentBlock instance.
    return ModelObject.new(
        DocumentBlock,
        id='block_1',
        type='text',
        content='This is a text block.'
    )

# ** fixture: mock_document_data_with_blocks
@pytest.fixture
def mock_document_data_with_blocks(document_block: DocumentBlock) -> DocumentData:
    '''
    Fixture to create a mock DocumentData instance with blocks.

    :param document_block: The DocumentBlock instance to include.
    :type document_block: DocumentBlock
    :return: A mock DocumentData instance.
    :rtype: DocumentData
    '''
    
    # Create and return a mock DocumentData instance with blocks.
    document_data = Mock(spec=DocumentData)
    document_data.blocks = [document_block]
    return document_data

# *** tests

# ** test: document_monday_api_proxy_instantiation
def test_document_monday_api_proxy_instantiation(document_monday_api_proxy: DocumentMondayApiProxy):
    '''
    Test successful instantiation of a DocumentMondayApiProxy object.

    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(document_monday_api_proxy, DocumentMondayApiProxy)
    assert document_monday_api_proxy.api_key == 'test_api_key'

# ** test: create_doc_in_column_success
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
@patch('tiferet_monday.data.doc.DocumentData.from_data')
def test_create_doc_in_column_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy,
    mock_document_data: DocumentData
):
    '''
    Test successful creation of a document in a column using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    :param mock_document_data: The mock DocumentData instance.
    :type mock_document_data: DocumentData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = {
        'id': 'doc_1',
        'name': 'Test Document',
        'object_id': '1'
    }
    mock_from_data.return_value = mock_document_data
    
    # Create document in column.
    result = document_monday_api_proxy.create_doc_in_column(item_id='1', column_id='col_1')
    
    # Verify the mutation was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, Document)
    assert result.id == 'doc_1'

# ** test: query_by_object_ids_success
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
@patch('tiferet_monday.data.doc.DocumentData.from_data')
def test_query_by_object_ids_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy,
    mock_document_data: DocumentData
):
    '''
    Test successful query of documents by object IDs using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    :param mock_document_data: The mock DocumentData instance.
    :type mock_document_data: DocumentData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'id': '1',
        'name': 'Test Document',
        'object_id': '1',
        'blocks': []
    }]
    mock_from_data.return_value = mock_document_data
    
    # Query documents by object IDs.
    result = document_monday_api_proxy.query_by_object_ids(object_ids=['1'])
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'objectIds': [1]},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Document)
    assert result[0].id == '1'

# ** test: query_by_object_ids_no_data
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
def test_query_by_object_ids_no_data(
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy
):
    '''
    Test query_by_object_ids returns an empty list when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = []
    
    # Query documents by object IDs.
    result = document_monday_api_proxy.query_by_object_ids(object_ids=['1'])
    
    # Verify the result is an empty list.
    assert result == []

# ** test: update_doc_name_success
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
def test_update_doc_name_success(
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy
):
    '''
    Test successful update of a document name using the Monday.com API.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Set up the mock response to return None (mutation does not return data).
    mock_execute_query.return_value = None
    
    # Update document name.
    document_monday_api_proxy.update_doc_name(doc_id='1', name='New Document Name')
    
    # Verify the mutation was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'docId': 1, 'name': 'New Document Name'},
        api_version='2025-10'
    )

# ** test: query_doc_blocks_success
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
@patch('tiferet_monday.data.doc.DocumentData.from_data')
def test_query_doc_blocks_success(
    mock_from_data: Mock,
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy,
    mock_document_data_with_blocks: DocumentData
):
    '''
    Test successful query of document blocks using the Monday.com API.

    :param mock_from_data: The mocked DataObject.from_data function.
    :type mock_from_data: Mock
    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    :param mock_document_data_with_blocks: The mock DocumentData instance with blocks.
    :type mock_document_data_with_blocks: DocumentData
    '''
    
    # Set up the mock response and data mapping.
    mock_execute_query.return_value = [{
        'blocks': [
            {'id': 'block_1', 'type': 'text', 'content': 'This is a text block.'}
        ]
    }]
    mock_from_data.return_value = mock_document_data_with_blocks
    
    # Query document blocks.
    result = document_monday_api_proxy.query_doc_blocks(doc_id='1', limit=25, page=1)
    
    # Verify the query was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={'docId': 1, 'limit': 25, 'page': 1},
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], DocumentBlock)
    assert result[0].id == 'block_1'

# ** test: query_doc_blocks_no_data
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
def test_query_doc_blocks_no_data(
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy
):
    '''
    Test query_doc_blocks returns an empty list when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Set up the mock response to return an empty list.
    mock_execute_query.return_value = [{}]
    
    # Query document blocks.
    result = document_monday_api_proxy.query_doc_blocks(doc_id='1')
    
    # Verify the result is an empty list.
    assert result == []

# ** test: create_doc_block_success
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
def test_create_doc_block_success(
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy
):
    '''
    Test successful creation of a document block using the Monday.com API.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Set up the mock response.
    mock_execute_query.return_value = {'id': 'block_2'}
    
    # Create document block.
    result = document_monday_api_proxy.create_doc_block(
        doc_id='1',
        type='text',
        content='New block content',
        after_block_id='block_1'
    )
    
    # Verify the mutation was executed with the correct parameters.
    mock_execute_query.assert_called_once_with(
        query=mock_execute_query.call_args[1]['query'],
        variables={
            'docId': 1,
            'type': 'text',
            'content': 'New block content',
            'afterBlockId': 'block_1'
        },
        start_node=mock_execute_query.call_args[1]['start_node']
    )
    
    # Verify the result.
    assert result == 'block_2'

# ** test: create_doc_block_no_data
@patch('tiferet_monday.proxies.requests.doc.DocumentMondayApiProxy.execute_query')
def test_create_doc_block_no_data(
    mock_execute_query: Mock,
    document_monday_api_proxy: DocumentMondayApiProxy
):
    '''
    Test create_doc_block returns None when no data is returned.

    :param mock_execute_query: The mocked execute_query method.
    :type mock_execute_query: Mock
    :param document_monday_api_proxy: The DocumentMondayApiProxy instance to test.
    :type document_monday_api_proxy: DocumentMondayApiProxy
    '''
    
    # Set up the mock response to return an empty dictionary.
    mock_execute_query.return_value = {}
    
    # Create document block.
    result = document_monday_api_proxy.create_doc_block(
        doc_id='1',
        type='text',
        content='New block content'
    )
    
    # Verify the result is None.
    assert result is None