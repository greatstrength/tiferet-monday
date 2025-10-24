"""Tiferet Monday Document Data Objects Tests"""

# *** imports

# ** infra
import pytest
from tiferet import DataObject, ModelObject

# ** app
from ..doc import DocumentData
from ...models import Document, DocumentBlock

# *** fixtures

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

# ** fixture: document_data
@pytest.fixture
def document_data(document_block: DocumentBlock) -> DocumentData:
    '''
    Fixture to create a basic DocumentData instance with a document block.

    :param document_block: The DocumentBlock instance to include.
    :type document_block: DocumentBlock
    :return: A DocumentData instance.
    :rtype: DocumentData
    '''
    
    # Create and return a DocumentData instance.
    return DataObject.from_data(
        DocumentData,
        id='doc_1',
        name='Test Document',
        object_id='obj_1',
        blocks=[document_block]
    )

# *** tests

# ** test: document_data_instantiation
def test_document_data_instantiation(document_data: DocumentData):
    '''
    Test successful instantiation of a DocumentData object.

    :param document_data: The DocumentData instance to test.
    :type document_data: DocumentData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(document_data, DocumentData)
    assert document_data.id == 'doc_1'
    assert document_data.name == 'Test Document'
    assert document_data.object_id == 'obj_1'
    assert len(document_data.blocks) == 1
    assert isinstance(document_data.blocks[0], DocumentBlock)
    assert document_data.blocks[0].id == 'block_1'

# ** test: document_data_instantiation_empty_blocks
def test_document_data_instantiation_empty_blocks():
    '''
    Test instantiation of a DocumentData object with an empty blocks list.
    '''
    
    # Create a DocumentData with an empty blocks list.
    document_data = DataObject.from_data(
        DocumentData,
        id='doc_2',
        name='Empty Document',
        object_id='obj_2'
    )
    
    # Verify the instance type and attributes.
    assert isinstance(document_data, DocumentData)
    assert document_data.id == 'doc_2'
    assert document_data.name == 'Empty Document'
    assert document_data.object_id == 'obj_2'
    assert document_data.blocks == []

# ** test: document_data_map
def test_document_data_map(document_data: DocumentData):
    '''
    Test mapping a DocumentData object to a Document model.

    :param document_data: The DocumentData instance to test.
    :type document_data: DocumentData
    '''
    
    # Map to a Document model.
    mapped = document_data.map()
    
    # Verify the mapped instance.
    assert isinstance(mapped, Document)
    assert mapped.id == 'doc_1'
    assert mapped.name == 'Test Document'
    assert mapped.object_id == 'obj_1'
    assert len(mapped.blocks) == 1

# ** test: document_data_to_primitive
def test_document_data_to_primitive(document_data: DocumentData):
    '''
    Test converting a DocumentData object to a primitive dictionary.

    :param document_data: The DocumentData instance to test.
    :type document_data: DocumentData
    '''
    
    # Convert to primitive dictionary with 'to_data' role.
    primitive = document_data.to_primitive(role='to_data')
    
    # Verify the primitive dictionary.
    assert isinstance(primitive, dict)
    assert primitive['id'] == 'doc_1'
    assert primitive['name'] == 'Test Document'
    assert primitive['object_id'] == 'obj_1'
    assert primitive['blocks'][0]['id'] == 'block_1'