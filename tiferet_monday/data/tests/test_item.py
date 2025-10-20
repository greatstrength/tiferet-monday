"""Tiferet Monday Item Data Transfer Objects Tests"""

# *** imports

# ** infra
import pytest
from tiferet import DataObject

# ** app
from ...models import (
    Item,
    ItemDetail
)
from ...data import (
    ColumnData,
    ColumnValueData
)
from ..item import (
    ItemBoardData,
    ItemGroupData,
    ItemData,
    ItemDetailData
)

# *** fixtures

# ** fixture: item_board_data
@pytest.fixture
def item_board_data() -> ItemBoardData:
    '''
    Fixture to create a basic ItemBoardData instance.

    :return: An ItemBoardData instance.
    :rtype: ItemBoardData
    '''
    
    # Create and return an ItemBoardData instance.
    return DataObject.from_data(
        ItemBoardData,
        id='board_1'
    )

# ** fixture: item_group_data
@pytest.fixture
def item_group_data() -> ItemGroupData:
    '''
    Fixture to create a basic ItemGroupData instance.

    :return: An ItemGroupData instance.
    :rtype: ItemGroupData
    '''
    
    # Create and return an ItemGroupData instance.
    return DataObject.from_data(
        ItemGroupData,
        id='group_1'
    )

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

# ** fixture: column_value_data
@pytest.fixture
def column_value_data(column_data: ColumnData) -> ColumnValueData:
    '''
    Fixture to create a basic ColumnValueData instance.

    :param column_data: The ColumnData instance to include.
    :type column_data: ColumnData
    :return: A ColumnValueData instance.
    :rtype: ColumnValueData
    '''
    
    # Create and return a ColumnValueData instance.
    return DataObject.from_data(
        ColumnValueData,
        id='status_1',
        type='status',
        column=column_data,
        value='in_progress',
        text='In Progress',
        index=2
    )

# ** fixture: item_data
@pytest.fixture
def item_data(item_board_data: ItemBoardData) -> ItemData:
    '''
    Fixture to create a basic ItemData instance.

    :param item_board_data: The ItemBoardData instance to include.
    :type item_board_data: ItemBoardData
    :return: An ItemData instance.
    :rtype: ItemData
    '''
    
    # Create and return an ItemData instance.
    return DataObject.from_data(
        ItemData,
        id='item_1',
        name='Test Item',
        board=item_board_data,
        updates=[
            {
                'id': 'update_1',
                'creator_id': 'user_1',
                'item_id': 'item_1',
                'body': 'This is an update.',
                'replies': [
                    {
                        'id': 'reply_1',
                        'creator_id': 'user_1',
                        'body': 'This is a reply.'
                    }
                ]
            }
        ]
    )

# ** fixture: item_detail_data
@pytest.fixture
def item_detail_data(
    item_board_data: ItemBoardData,
    item_group_data: ItemGroupData,
    item_data: ItemData,
    column_value_data: ColumnValueData
) -> ItemDetailData:
    '''
    Fixture to create a basic ItemDetailData instance.

    :param item_board_data: The ItemBoardData instance to include.
    :type item_board_data: ItemBoardData
    :param item_group_data: The ItemGroupData instance to include.
    :type item_group_data: ItemGroupData
    :param item_data: The ItemData instance to include as the parent item.
    :type item_data: ItemData
    :param column_value_data: The ColumnValueData instance to include.
    :type column_value_data: ColumnValueData
    :return: An ItemDetailData instance.
    :rtype: ItemDetailData
    '''
    
    # Create and return an ItemDetailData instance.
    return DataObject.from_data(
        ItemDetailData,
        id='item_2',
        name='Test Item Detail',
        board=item_board_data,
        group=item_group_data,
        parent_item=item_data,
        column_values=[column_value_data]
    )

# *** tests

# ** test: item_board_data_instantiation
def test_item_board_data_instantiation(item_board_data: ItemBoardData):
    '''
    Test successful instantiation of an ItemBoardData object.

    :param item_board_data: The ItemBoardData instance to test.
    :type item_board_data: ItemBoardData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_board_data, ItemBoardData)
    assert item_board_data.id == 'board_1'

# ** test: item_group_data_instantiation
def test_item_group_data_instantiation(item_group_data: ItemGroupData):
    '''
    Test successful instantiation of an ItemGroupData object.

    :param item_group_data: The ItemGroupData instance to test.
    :type item_group_data: ItemGroupData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_group_data, ItemGroupData)
    assert item_group_data.id == 'group_1'

# ** test: item_data_instantiation
def test_item_data_instantiation(item_data: ItemData):
    '''
    Test successful instantiation of an ItemData object.

    :param item_data: The ItemData instance to test.
    :type item_data: ItemData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_data, ItemData)
    assert item_data.id == 'item_1'
    assert item_data.name == 'Test Item'
    assert isinstance(item_data.board, ItemBoardData)
    assert item_data.board.id == 'board_1'
    assert len(item_data.updates) == 1
    assert item_data.updates[0].id == 'update_1'
    assert len(item_data.updates[0].replies) == 1

# ** test: item_data_to_primitive
def test_item_data_to_primitive(item_data: ItemData):
    '''
    Test converting an ItemData object to a primitive dictionary.

    :param item_data: The ItemData instance to test.
    :type item_data: ItemData
    '''
    
    # Convert to primitive dictionary with 'to_data' role.
    primitive = item_data.to_primitive(role='to_data')
    
    # Verify the primitive dictionary.
    assert isinstance(primitive, dict)
    assert primitive['id'] == 'item_1'
    assert primitive['name'] == 'Test Item'
    assert isinstance(primitive['board'], dict)
    assert primitive['board']['id'] == 'board_1'
    assert len(primitive['updates']) == 1
    assert primitive['updates'][0]['id'] == 'update_1'
    assert len(primitive['updates'][0]['replies']) == 1

# ** test: item_data_map
def test_item_data_map(item_data: ItemData):
    '''
    Test mapping an ItemData object to an Item model.

    :param item_data: The ItemData instance to test.
    :type item_data: ItemData
    '''
    
    # Map to an Item model.
    mapped = item_data.map()
    
    # Verify the mapped instance.
    assert isinstance(mapped, Item)
    assert mapped.id == 'item_1'
    assert mapped.name == 'Test Item'
    assert mapped.board_id == 'board_1'
    assert len(mapped.updates) == 1
    assert mapped.updates[0].id == 'update_1'

# ** test: item_detail_data_instantiation
def test_item_detail_data_instantiation(item_detail_data: ItemDetailData):
    '''
    Test successful instantiation of an ItemDetailData object.

    :param item_detail_data: The ItemDetailData instance to test.
    :type item_detail_data: ItemDetailData
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_detail_data, ItemDetailData)
    assert item_detail_data.id == 'item_2'
    assert item_detail_data.name == 'Test Item Detail'
    assert isinstance(item_detail_data.board, ItemBoardData)
    assert item_detail_data.board.id == 'board_1'
    assert isinstance(item_detail_data.group, ItemGroupData)
    assert item_detail_data.group.id == 'group_1'
    assert isinstance(item_detail_data.parent_item, ItemData)
    assert item_detail_data.parent_item.id == 'item_1'
    assert len(item_detail_data.column_values) == 1
    assert isinstance(item_detail_data.column_values[0], ColumnValueData)

# ** test: item_detail_data_to_primitive
def test_item_detail_data_to_primitive(item_detail_data: ItemDetailData):
    '''
    Test converting an ItemDetailData object to a primitive dictionary.

    :param item_detail_data: The ItemDetailData instance to test.
    :type item_detail_data: ItemDetailData
    '''
    
    # Convert to primitive dictionary with 'to_data' role.
    primitive = item_detail_data.to_primitive(role='to_data')
    
    # Verify the primitive dictionary.
    assert isinstance(primitive, dict)
    assert primitive['id'] == 'item_2'
    assert primitive['name'] == 'Test Item Detail'
    assert isinstance(primitive['board'], dict)
    assert primitive['board']['id'] == 'board_1'
    assert isinstance(primitive['group'], dict)
    assert primitive['group']['id'] == 'group_1'
    assert isinstance(primitive['parent_item'], dict)
    assert primitive['parent_item']['id'] == 'item_1'
    assert len(primitive['column_values']) == 1
    assert primitive['column_values'][0]['id'] == 'status_1'

# ** test: item_detail_data_map
def test_item_detail_data_map(item_detail_data: ItemDetailData):
    '''
    Test mapping an ItemDetailData object to an ItemDetail model.

    :param item_detail_data: The ItemDetailData instance to test.
    :type item_detail_data: ItemDetailData
    '''
    
    # Map to an ItemDetail model.
    mapped = item_detail_data.map()
    
    # Verify the mapped instance.
    assert isinstance(mapped, ItemDetail)
    assert mapped.id == 'item_2'
    assert mapped.name == 'Test Item Detail'
    assert mapped.board_id == 'board_1'
    assert mapped.group_id == 'group_1'
    assert mapped.parent_item_id == 'item_1'
    assert len(mapped.column_values) == 1
    assert mapped.column_values[0].id == 'status_1'