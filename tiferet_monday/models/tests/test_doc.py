"""Tiferet Monday Document Models Tests"""

# *** imports

# ** infra
import pytest
from tiferet import ModelObject

# ** app
from ..doc import DocumentBlock, Document

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

# ** fixture: document
@pytest.fixture
def document(document_block: DocumentBlock) -> Document:
    '''
    Fixture to create a basic Document instance with a document block.

    :param document_block: The DocumentBlock instance to include.
    :type document_block: DocumentBlock
    :return: A Document instance.
    :rtype: Document
    '''
    
    # Create and return a Document instance.
    return ModelObject.new(
        Document,
        id='doc_1',
        name='Test Document',
        object_id='obj_1',
        blocks=[document_block]
    )

# *** tests

# ** test: document_block_instantiation
def test_document_block_instantiation(document_block: DocumentBlock):
    '''
    Test successful instantiation of a DocumentBlock object.

    :param document_block: The DocumentBlock instance to test.
    :type document_block: DocumentBlock
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(document_block, DocumentBlock)
    assert document_block.id == 'block_1'
    assert document_block.type == 'text'
    assert document_block.content == 'This is a text block.'

# ** test: document_block_instantiation_defaults
def test_document_block_instantiation_defaults():
    '''
    Test instantiation of a DocumentBlock object with default values.
    '''
    
    # Create a DocumentBlock with only the required id.
    document_block = ModelObject.new(
        DocumentBlock,
        id='block_2'
    )
    
    # Verify the instance type and default attributes.
    assert isinstance(document_block, DocumentBlock)
    assert document_block.id == 'block_2'
    assert document_block.type == 'text'  # Default value
    assert document_block.content == ''    # Default value

# ** test: document_instantiation
def test_document_instantiation(document: Document):
    '''
    Test successful instantiation of a Document object.

    :param document: The Document instance to test.
    :type document: Document
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(document, Document)
    assert document.id == 'doc_1'
    assert document.name == 'Test Document'
    assert document.object_id == 'obj_1'
    assert len(document.blocks) == 1
    assert isinstance(document.blocks[0], DocumentBlock)
    assert document.blocks[0].id == 'block_1'

# ** test: document_instantiation_missing_required
def test_document_instantiation_missing_required():
    '''
    Test instantiation of a Document object with missing required fields raises an error.
    '''
    
    # Attempt to create a Document without required fields and expect an Exception.
    with pytest.raises(Exception):
        ModelObject.new(Document, id='doc_1')

# ** test: document_instantiation_empty_blocks
def test_document_instantiation_empty_blocks():
    '''
    Test instantiation of a Document object with an empty blocks list.
    '''
    
    # Create a Document with an empty blocks list.
    document = ModelObject.new(
        Document,
        id='doc_2',
        name='Empty Document',
        object_id='obj_2'
    )
    
    # Verify the instance type and attributes.
    assert isinstance(document, Document)
    assert document.id == 'doc_2'
    assert document.name == 'Empty Document'
    assert document.object_id == 'obj_2'
    assert document.blocks == []