"""Tiferet Monday Column Value Data Objects Tests"""

# *** imports

# ** infra
import pytest
from tiferet import DataObject

# ** app
from ...models import (
    ColumnValue,
    StatusValue,
    PeopleValue,
    NumbersValue,
    BoardRelationValue,
    FileValue,
    DocValue
)
from ...data import (
    ColumnData,
    ColumnValueData
)

# *** fixtures

# ** fixture: column_data
@pytest.fixture
def column_data() -> ColumnData:
    '''
    Fixture to create a basic ColumnData instance.

    :return: A ColumnData instance.
    :rtype: ColumnData
    '''
    
    # Create and return a ColumnData instance.
    return DataObject.from_data(
        ColumnData,
        title='Status',
        description='A status column',
        settings_str='{"labels": ["In Progress", "Done"]}'
    )

# ** fixture: column_value_data_status
@pytest.fixture
def column_value_data_status(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a status column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for status.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for status.
    return DataObject.from_data(
        ColumnValueData,
        id='status_1',
        type='status',
        column=column_data,
        index=2,
        text='In Progress',
        value='in_progress'
    )

# ** fixture: column_value_data_people
@pytest.fixture
def column_value_data_people(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a people column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for people.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for people.
    return DataObject.from_data(
        ColumnValueData,
        id='people_1',
        type='people',
        column=column_data,
        persons_and_teams=[
            {'id': 'user_1', 'kind': 'person'},
            {'id': 'team_1', 'kind': 'team'}
        ]
    )

# ** fixture: column_value_data_numbers
@pytest.fixture
def column_value_data_numbers(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a numbers column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for numbers.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for numbers.
    return DataObject.from_data(
        ColumnValueData,
        id='number_1',
        type='numbers',
        column=column_data,
        number=42
    )

# ** fixture: column_value_data_board_relation
@pytest.fixture
def column_value_data_board_relation(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a board relation column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for board relation.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for board relation.
    return DataObject.from_data(
        ColumnValueData,
        id='relation_1',
        type='board_relation',
        column=column_data,
        linked_item_ids=[101, 102]
    )

# ** fixture: column_value_data_file
@pytest.fixture
def column_value_data_file(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a file column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for file.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for file.
    return DataObject.from_data(
        ColumnValueData,
        id='file_1',
        type='file',
        column=column_data,
        files=[
            {'object_id': 'file_001', 'name': 'doc.pdf'},
            {'object_id': 'file_002', 'name': 'image.png'}
        ]
    )

# ** fixture: column_value_data_doc
@pytest.fixture
def column_value_data_doc(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a ColumnValueData instance for a doc column.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance for doc.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance for doc.
    return DataObject.from_data(
        ColumnValueData,
        id='doc_1',
        type='doc',
        column=column_data,
        file={'object_id': 'doc_001', 'name': 'report.pdf'}
    )

# ** fixure: column_value_data_generic
@pytest.fixture
def column_value_data_generic(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a generic ColumnValueData instance.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A generic ColumnValueData instance.
    :rtype: ColumnValueData
    '''

    # Update column title to ensure clarity in tests.
    column_data.title = 'Unknown Column Type'
    
    # Create and return a generic ColumnValueData instance.
    value = DataObject.from_data(
        ColumnValueData,
        id='unknown_1',
        type='unknown',
        column=column_data,
        value='some_value'
    )

    return value

# *** tests

# ** test: column_data_instantiation
def test_column_data_instantiation(column_data: ColumnData):
    '''
    Test successful instantiation of a ColumnData object.

    :param column_data: The ColumnData instance to test.
    :type column_data: ColumnData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_data, ColumnData)
    assert column_data.title == 'Status'
    assert column_data.description == 'A status column'
    assert column_data.settings_str == '{"labels": ["In Progress", "Done"]}'

# ** test: column_value_data_status_instantiation
def test_column_value_data_status_instantiation(column_value_data_status: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a status column.

    :param column_value_data_status: The ColumnValueData instance to test.
    :type column_value_data_status: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_status, ColumnValueData)
    assert column_value_data_status.id == 'status_1'
    assert column_value_data_status.type == 'status'
    assert isinstance(column_value_data_status.column, ColumnData)
    assert column_value_data_status.index == 2
    assert column_value_data_status.text == 'In Progress'
    assert column_value_data_status.value == 'in_progress'

# ** test: column_value_data_status_map
def test_column_value_data_status_map(column_value_data_status: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a status column to a StatusValue model.

    :param column_value_data_status: The ColumnValueData instance to test.
    :type column_value_data_status: ColumnValueData
    '''
    
    # Map to a StatusValue model.
    mapped = column_value_data_status.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, StatusValue)
    assert mapped.id == 'status_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'status'
    assert mapped.index == 2
    assert mapped.text == 'In Progress'
    assert mapped.value == 'in_progress'
    assert mapped.description == 'A status column'
    assert mapped.settings_str == '{"labels": ["In Progress", "Done"]}'

# ** test: column_value_data_people_instantiation
def test_column_value_data_people_instantiation(column_value_data_people: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a people column.

    :param column_value_data_people: The ColumnValueData instance to test.
    :type column_value_data_people: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_people, ColumnValueData)
    assert column_value_data_people.id == 'people_1'
    assert column_value_data_people.type == 'people'
    assert isinstance(column_value_data_people.column, ColumnData)
    assert column_value_data_people.persons_and_teams == [
        {'id': 'user_1', 'kind': 'person'},
        {'id': 'team_1', 'kind': 'team'}
    ]

# ** test: column_value_data_people_map
def test_column_value_data_people_map(column_value_data_people: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a people column to a PeopleValue model.

    :param column_value_data_people: The ColumnValueData instance to test.
    :type column_value_data_people: ColumnValueData
    '''
    
    # Map to a PeopleValue model.
    mapped = column_value_data_people.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, PeopleValue)
    assert mapped.id == 'people_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'people'
    assert mapped.persons_and_teams == [
        {'id': 'user_1', 'kind': 'person'},
        {'id': 'team_1', 'kind': 'team'}
    ]

# ** test: column_value_data_numbers_instantiation
def test_column_value_data_numbers_instantiation(column_value_data_numbers: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a numbers column.

    :param column_value_data_numbers: The ColumnValueData instance to test.
    :type column_value_data_numbers: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_numbers, ColumnValueData)
    assert column_value_data_numbers.id == 'number_1'
    assert column_value_data_numbers.type == 'numbers'
    assert isinstance(column_value_data_numbers.column, ColumnData)
    assert column_value_data_numbers.number == 42

# ** test: column_value_data_numbers_map
def test_column_value_data_numbers_map(column_value_data_numbers: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a numbers column to a NumbersValue model.

    :param column_value_data_numbers: The ColumnValueData instance to test.
    :type column_value_data_numbers: ColumnValueData
    '''
    
    # Map to a NumbersValue model.
    mapped = column_value_data_numbers.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, NumbersValue)
    assert mapped.id == 'number_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'numbers'
    assert mapped.number == 42

# ** test: column_value_data_board_relation_instantiation
def test_column_value_data_board_relation_instantiation(column_value_data_board_relation: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a board relation column.

    :param column_value_data_board_relation: The ColumnValueData instance to test.
    :type column_value_data_board_relation: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_board_relation, ColumnValueData)
    assert column_value_data_board_relation.id == 'relation_1'
    assert column_value_data_board_relation.type == 'board_relation'
    assert isinstance(column_value_data_board_relation.column, ColumnData)
    assert column_value_data_board_relation.linked_item_ids == [101, 102]

# ** test: column_value_data_board_relation_map
def test_column_value_data_board_relation_map(column_value_data_board_relation: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a board relation column to a BoardRelationValue model.

    :param column_value_data_board_relation: The ColumnValueData instance to test.
    :type column_value_data_board_relation: ColumnValueData
    '''
    
    # Map to a BoardRelationValue model.
    mapped = column_value_data_board_relation.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, BoardRelationValue)
    assert mapped.id == 'relation_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'board_relation'
    assert mapped.linked_item_ids == [101, 102]

# ** test: column_value_data_file_instantiation
def test_column_value_data_file_instantiation(column_value_data_file: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a file column.

    :param column_value_data_file: The ColumnValueData instance to test.
    :type column_value_data_file: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_file, ColumnValueData)
    assert column_value_data_file.id == 'file_1'
    assert column_value_data_file.type == 'file'
    assert isinstance(column_value_data_file.column, ColumnData)
    assert column_value_data_file.files == [
        {'object_id': 'file_001', 'name': 'doc.pdf'},
        {'object_id': 'file_002', 'name': 'image.png'}
    ]

# ** test: column_value_data_file_map
def test_column_value_data_file_map(column_value_data_file: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a file column to a FileValue model.

    :param column_value_data_file: The ColumnValueData instance to test.
    :type column_value_data_file: ColumnValueData
    '''
    
    # Map to a FileValue model.
    mapped = column_value_data_file.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, FileValue)
    assert mapped.id == 'file_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'file'
    assert mapped.files == [
        {'object_id': 'file_001', 'name': 'doc.pdf'},
        {'object_id': 'file_002', 'name': 'image.png'}
    ]

# ** test: column_value_data_doc_instantiation
def test_column_value_data_doc_instantiation(column_value_data_doc: ColumnValueData):
    '''
    Test successful instantiation of a ColumnValueData object for a doc column.

    :param column_value_data_doc: The ColumnValueData instance to test.
    :type column_value_data_doc: ColumnValueData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(column_value_data_doc, ColumnValueData)
    assert column_value_data_doc.id == 'doc_1'
    assert column_value_data_doc.type == 'doc'
    assert isinstance(column_value_data_doc.column, ColumnData)
    assert column_value_data_doc.file == {'object_id': 'doc_001', 'name': 'report.pdf'}

# ** test: column_value_data_doc_map
def test_column_value_data_doc_map(column_value_data_doc: ColumnValueData):
    '''
    Test mapping a ColumnValueData object for a doc column to a DocValue model.

    :param column_value_data_doc: The ColumnValueData instance to test.
    :type column_value_data_doc: ColumnValueData
    '''
    
    # Map to a DocValue model.
    mapped = column_value_data_doc.map(map_to_type=True)
    
    # Verify the mapped instance.
    assert isinstance(mapped, DocValue)
    assert mapped.id == 'doc_1'
    assert mapped.name == 'Status'
    assert mapped.type == 'doc'
    assert mapped.file == {'object_id': 'doc_001', 'name': 'report.pdf'}

# ** test: column_value_data_generic_map
def test_column_value_data_generic_map(column_value_data_generic: ColumnValueData):
    '''
    Test mapping a t to a generic ColumnValue model when map_to_type is False.

    :param column_value_data_status: The ColumnValueData instance to test.
    :type column_value_data_status: ColumnValueData
    '''
    
    # Map to a generic ColumnValue model.
    mapped = column_value_data_generic.map(map_to_type=False)
    
    # Assert the mapped instance is a generic ColumnValue.
    assert isinstance(mapped, ColumnValue)

    # Assert it is not a specific subtype.
    assert not isinstance(mapped, StatusValue)
    assert not isinstance(mapped, PeopleValue)
    assert not isinstance(mapped, NumbersValue)
    assert not isinstance(mapped, BoardRelationValue)
    assert not isinstance(mapped, FileValue)
    assert not isinstance(mapped, DocValue)

    # Verify the mapped instance attributes.
    assert mapped.id == 'unknown_1'
    assert mapped.name == 'Unknown Column Type'
    assert mapped.type == 'unknown'

    # Ensure no subtype-specific attributes are present.
    assert not hasattr(mapped, 'index')
    assert not hasattr(mapped, 'persons_and_teams')
    assert not hasattr(mapped, 'number')
    assert not hasattr(mapped, 'linked_item_ids')
    assert not hasattr(mapped, 'file')
    assert not hasattr(mapped, 'files')