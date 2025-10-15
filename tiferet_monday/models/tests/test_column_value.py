"""Tiferet Monday Column Value Models Tests"""

# *** imports

# ** infra
import pytest
from tiferet import ModelObject

# ** app
from ..column_value import (
    ColumnValue,
    StatusValue,
    PeopleValue,
    NumbersValue,
    BoardRelationValue,
    FileValue,
    DocValue
)

# *** fixtures

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
        id='col_1',
        name='Generic Column',
        type='text',
        text='Sample text',
        value='Sample value',
        description='A generic column',
        settings_str='{"format": "text"}'
    )

# ** fixture: status_value
@pytest.fixture
def status_value() -> StatusValue:
    '''
    Fixture to create a basic StatusValue instance.

    :return: A StatusValue instance.
    :rtype: StatusValue
    '''
    
    # Create and return a StatusValue instance.
    return ColumnValue.new(
        id='status_1',
        name='Status',
        type='status',
        text='In Progress',
        value='in_progress',
        index=2
    )

# ** fixture: people_value
@pytest.fixture
def people_value() -> PeopleValue:
    '''
    Fixture to create a basic PeopleValue instance.

    :return: A PeopleValue instance.
    :rtype: PeopleValue
    '''
    
    # Create and return a PeopleValue instance.
    return ColumnValue.new(
        id='people_1',
        name='Assignees',
        type='people',
        persons_and_teams=[
            {'id': 'user_1', 'kind': 'person'},
            {'id': 'team_1', 'kind': 'team'}
        ]
    )

# ** fixture: numbers_value
@pytest.fixture
def numbers_value() -> NumbersValue:
    '''
    Fixture to create a basic NumbersValue instance.

    :return: A NumbersValue instance.
    :rtype: NumbersValue
    '''
    
    # Create and return a NumbersValue instance.
    return ColumnValue.new(
        id='number_1',
        name='Count',
        type='numbers',
        number=42
    )

# ** fixture: board_relation_value
@pytest.fixture
def board_relation_value() -> BoardRelationValue:
    '''
    Fixture to create a basic BoardRelationValue instance.

    :return: A BoardRelationValue instance.
    :rtype: BoardRelationValue
    '''
    
    # Create and return a BoardRelationValue instance.
    return ColumnValue.new(
        id='relation_1',
        name='Related Items',
        type='board_relation',
        linked_item_ids=[101, 102]
    )

# ** fixture: file_value
@pytest.fixture
def file_value() -> FileValue:
    '''
    Fixture to create a basic FileValue instance.

    :return: A FileValue instance.
    :rtype: FileValue
    '''
    
    # Create and return a FileValue instance.
    return ColumnValue.new(
        id='file_1',
        name='Attachments',
        type='file',
        files=[
            {'object_id': 'file_001', 'name': 'doc.pdf'},
            {'object_id': 'file_002', 'name': 'image.png'}
        ]
    )

# ** fixture: doc_value
@pytest.fixture
def doc_value() -> DocValue:
    '''
    Fixture to create a basic DocValue instance.

    :return: A DocValue instance.
    :rtype: DocValue
    '''
    
    # Create and return a DocValue instance.
    return ColumnValue.new(
        id='doc_1',
        name='Document',
        type='doc',
        file={'object_id': 'doc_001', 'name': 'report.pdf'}
    )

# *** tests

# ** test: column_value_instantiation
def test_column_value_instantiation(column_value: ColumnValue):
    '''
    Test successful instantiation of a ColumnValue object.

    :param column_value: The ColumnValue instance to test.
    :type column_value: ColumnValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value, ColumnValue)
    assert column_value.id == 'col_1'
    assert column_value.name == 'Generic Column'
    assert column_value.type == 'text'
    assert column_value.text == 'Sample text'
    assert column_value.value == 'Sample value'
    assert column_value.description == 'A generic column'
    assert column_value.settings_str == '{"format": "text"}'

# ** test: status_value_instantiation
def test_status_value_instantiation(status_value: StatusValue):
    '''
    Test successful instantiation of a StatusValue object.

    :param status_value: The StatusValue instance to test.
    :type status_value: StatusValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(status_value, StatusValue)
    assert isinstance(status_value, ColumnValue)
    assert status_value.id == 'status_1'
    assert status_value.name == 'Status'
    assert status_value.type == 'status'
    assert status_value.text == 'In Progress'
    assert status_value.value == 'in_progress'
    assert status_value.index == 2

# ** test: people_value_instantiation
def test_people_value_instantiation(people_value: PeopleValue):
    '''
    Test successful instantiation of a PeopleValue object.

    :param people_value: The PeopleValue instance to test.
    :type people_value: PeopleValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(people_value, PeopleValue)
    assert isinstance(people_value, ColumnValue)
    assert people_value.id == 'people_1'
    assert people_value.name == 'Assignees'
    assert people_value.type == 'people'
    assert people_value.persons_and_teams == [
        {'id': 'user_1', 'kind': 'person'},
        {'id': 'team_1', 'kind': 'team'}
    ]

# ** test: people_value_get_person_ids
def test_people_value_get_person_ids(people_value: PeopleValue):
    '''
    Test retrieving person IDs from a PeopleValue object.

    :param people_value: The PeopleValue instance to test.
    :type people_value: PeopleValue
    '''
    
    # Retrieve and verify person IDs.
    person_ids = people_value.get_person_ids()
    assert person_ids == ['user_1']

# ** test: numbers_value_instantiation
def test_numbers_value_instantiation(numbers_value: NumbersValue):
    '''
    Test successful instantiation of a NumbersValue object.

    :param numbers_value: The NumbersValue instance to test.
    :type numbers_value: NumbersValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(numbers_value, NumbersValue)
    assert isinstance(numbers_value, ColumnValue)
    assert numbers_value.id == 'number_1'
    assert numbers_value.name == 'Count'
    assert numbers_value.type == 'numbers'
    assert numbers_value.number == 42

# ** test: board_relation_value_instantiation
def test_board_relation_value_instantiation(board_relation_value: BoardRelationValue):
    '''
    Test successful instantiation of a BoardRelationValue object.

    :param board_relation_value: The BoardRelationValue instance to test.
    :type board_relation_value: BoardRelationValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(board_relation_value, BoardRelationValue)
    assert isinstance(board_relation_value, ColumnValue)
    assert board_relation_value.id == 'relation_1'
    assert board_relation_value.name == 'Related Items'
    assert board_relation_value.type == 'board_relation'
    assert board_relation_value.linked_item_ids == [101, 102]

# ** test: file_value_instantiation
def test_file_value_instantiation(file_value: FileValue):
    '''
    Test successful instantiation of a FileValue object.

    :param file_value: The FileValue instance to test.
    :type file_value: FileValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(file_value, FileValue)
    assert isinstance(file_value, ColumnValue)
    assert file_value.id == 'file_1'
    assert file_value.name == 'Attachments'
    assert file_value.type == 'file'
    assert file_value.files == [
        {'object_id': 'file_001', 'name': 'doc.pdf'},
        {'object_id': 'file_002', 'name': 'image.png'}
    ]

# ** test: file_value_get_object_ids
def test_file_value_get_object_ids(file_value: FileValue):
    '''
    Test retrieving object IDs from a FileValue object.

    :param file_value: The FileValue instance to test.
    :type file_value: FileValue
    '''
    
    # Retrieve and verify object IDs.
    object_ids = file_value.get_object_ids()
    assert object_ids == ['file_001', 'file_002']

# ** test: doc_value_instantiation
def test_doc_value_instantiation(doc_value: DocValue):
    '''
    Test successful instantiation of a DocValue object.

    :param doc_value: The DocValue instance to test.
    :type doc_value: DocValue
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(doc_value, DocValue)
    assert isinstance(doc_value, ColumnValue)
    assert doc_value.id == 'doc_1'
    assert doc_value.name == 'Document'
    assert doc_value.type == 'doc'
    assert doc_value.file == {'object_id': 'doc_001', 'name': 'report.pdf'}

# ** test: doc_value_get_object_id
def test_doc_value_get_object_id(doc_value: DocValue):
    '''
    Test retrieving the object ID from a DocValue object.

    :param doc_value: The DocValue instance to test.
    :type doc_value: DocValue
    '''
    
    # Retrieve and verify the object ID.
    object_id = doc_value.get_object_id()
    assert object_id == 'doc_001'

# ** test: doc_value_get_object_id_none
def test_doc_value_get_object_id_none():
    '''
    Test retrieving the object ID from a DocValue object with an empty file.
    '''
    
    # Create a DocValue with an empty file dictionary.
    doc_value = ColumnValue.new(
        id='doc_2',
        name='Empty Doc',
        type='doc',
        file={}
    )
    
    # Verify that get_object_id returns None.
    object_id = doc_value.get_object_id()
    assert object_id is None