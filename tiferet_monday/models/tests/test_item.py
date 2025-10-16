"""Tiferet Monday Item Models Tests"""

# *** imports

# ** infra
import pytest
from tiferet import ModelObject

# ** app
from ..column_value import ColumnValue
from ..item import (
    Reply,
    Update,
    Item,
    ItemDetail
)

# *** fixtures

# ** fixture: reply
@pytest.fixture
def reply() -> Reply:
    '''
    Fixture to create a basic Reply instance.
    '''
    
    # Create and return a Reply instance.
    return ModelObject.new(
        Reply,
        id='reply_1',
        creator_id='user_1',
        body='This is a reply.'
    )

# ** fixture: update
@pytest.fixture
def update(reply: Reply) -> Update:
    '''
    Fixture to create a basic Update instance with a reply.

    :param reply: A Reply instance to include in the Update.
    :type reply: Reply
    :return: An Update instance.
    :rtype: Update
    '''
    
    # Create and return an Update instance.
    return ModelObject.new(
        Update,
        id='update_1',
        creator_id='user_1',
        item_id='item_1',
        body='This is an update.',
        replies=[reply]
    )

# ** fixture: item
@pytest.fixture
def item(update: Update) -> Item:
    '''
    Fixture to create a basic Item instance with an update.

    :param update: An Update instance to include in the Item.
    :type update: Update
    :return: An Item instance.
    :rtype: Item
    '''
    
    # Create and return an Item instance.
    return ModelObject.new(
        Item,
        id='item_1',
        name='Test Item',
        board_id='board_1',
        updates=[update]
    )

# ** fixture: column_value_1
@pytest.fixture
def column_value_1() -> ColumnValue:
    '''
    Fixture to create a basic ColumnValue instance.

    :return: A ColumnValue instance.
    :rtype: ColumnValue
    '''
    
    # Create and return a ColumnValue instance.
    return ColumnValue.new(
        id='status_1',
        name='Status',
        type='status',
        value='Working on it',
    )

# ** fixture: column_value_2
@pytest.fixture
def column_value_2() -> ColumnValue:
    '''
    Fixture to create another basic ColumnValue instance.

    :return: A ColumnValue instance.
    :rtype: ColumnValue
    '''
    
    # Create and return a ColumnValue instance.
    return ColumnValue.new(
        id='priority_1',
        name='Priority',
        type='dropdown',
        value='High',
    )

# ** fixture: item_detail
@pytest.fixture
def item_detail(
    column_value_1: ColumnValue,
    column_value_2: ColumnValue
) -> ItemDetail:
    '''
    Fixture to create a basic ItemDetail instance using the custom new method.

    :param column_value_1: A ColumnValue instance to include in the ItemDetail.
    :type column_value_1: ColumnValue
    :param column_value_2: Another ColumnValue instance to include in the ItemDetail.
    :type column_value_2: ColumnValue
    :return: An ItemDetail instance.
    :rtype: ItemDetail
    '''
    
    # Create and return an ItemDetail instance.
    return ItemDetail.new(
        id='item_1',
        name='Test Item Detail',
        board_id='board_1',
        group_id='group_1',
        parent_item_id='parent_1',
        column_values=[
            column_value_1.to_primitive(),
            column_value_2.to_primitive()
        ],
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

# *** tests

# ** test: reply_instantiation
def test_reply_instantiation(reply: Reply):
    '''
    Test successful instantiation of a Reply object.

    :param reply: The Reply instance to test.
    :type reply: Reply
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(reply, Reply)
    assert reply.id == 'reply_1'
    assert reply.creator_id == 'user_1'
    assert reply.body == 'This is a reply.'

# ** test: update_instantiation
def test_update_instantiation(update: Update):
    '''
    Test successful instantiation of an Update object.

    :param update: The Update instance to test.
    :type update: Update
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(update, Update)
    assert update.id == 'update_1'
    assert update.creator_id == 'user_1'
    assert update.item_id == 'item_1'
    assert update.body == 'This is an update.'
    assert len(update.replies) == 1
    assert isinstance(update.replies[0], Reply)

# ** test: item_instantiation
def test_item_instantiation(item: Item):
    '''
    Test successful instantiation of an Item object.

    :param item: The Item instance to test.
    :type item: Item
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item, Item)
    assert item.id == 'item_1'
    assert item.name == 'Test Item'
    assert item.board_id == 'board_1'
    assert len(item.updates) == 1
    assert isinstance(item.updates[0], Update)

# ** test: item_detail_new_success
def test_item_detail_new_success(item_detail: ItemDetail):
    '''
    Test successful creation of an ItemDetail object using the custom new method.

    :param item_detail: The ItemDetail instance to test.
    :type item_detail: ItemDetail
    '''
    
    # Verify the instance type and attributes.
    assert isinstance(item_detail, ItemDetail)
    assert item_detail.id == 'item_1'
    assert item_detail.name == 'Test Item Detail'
    assert item_detail.board_id == 'board_1'
    assert item_detail.group_id == 'group_1'
    assert item_detail.parent_item_id == 'parent_1'
    assert len(item_detail.column_values) == 2
    assert all(isinstance(cv, ColumnValue) for cv in item_detail.column_values)
    assert len(item_detail.updates) == 1
    assert isinstance(item_detail.updates[0], Update)
    assert len(item_detail.updates[0].replies) == 1
    assert isinstance(item_detail.updates[0].replies[0], Reply)

# ** test: item_detail_get_column_value_by_id
def test_item_detail_get_column_value_by_id(item_detail: ItemDetail):
    '''
    Test retrieving a column value by ID from ItemDetail.

    :param item_detail: The ItemDetail instance to test.
    :type item_detail: ItemDetail
    '''
    
    # Retrieve and verify the column value by ID.
    cv = item_detail.get_column_value('status_1')
    assert cv is not None
    assert cv.id == 'status_1'
    assert cv.name == 'Status'
    assert cv.value == 'Working on it'

# ** test: item_detail_get_column_value_by_title
def test_item_detail_get_column_value_by_title(item_detail: ItemDetail):
    '''
    Test retrieving a column value by title from ItemDetail.

    :param item_detail: The ItemDetail instance to test.
    :type item_detail: ItemDetail
    '''
    
    # Retrieve and verify the column value by title.
    cv = item_detail.get_column_value('Priority')
    assert cv is not None
    assert cv.id == 'priority_1'
    assert cv.name == 'Priority'
    assert cv.value == 'High'

# ** test: item_detail_get_column_value_not_found
def test_item_detail_get_column_value_not_found(item_detail: ItemDetail):
    '''
    Test retrieving a non-existent column value from ItemDetail returns None.

    :param item_detail: The ItemDetail instance to test.
    :type item_detail: ItemDetail
    '''
    
    # Verify that a non-existent column returns None.
    cv = item_detail.get_column_value('non_existent')
    assert cv is None

# ** test: item_detail_get_column_values
def test_item_detail_get_column_values(item_detail: ItemDetail):
    '''
    Test retrieving multiple column values by IDs or titles from ItemDetail.

    :param item_detail: The ItemDetail instance to test.
    :type item_detail: ItemDetail
    '''
    
    # Retrieve and verify multiple column values by mixed IDs and titles.
    cvs = item_detail.get_column_values(['status_1', 'Priority'])
    assert len(cvs) == 2
    assert cvs[0].id == 'status_1'
    assert cvs[1].id == 'priority_1'

# ** test: item_detail_get_column_values_partial_not_found
def test_item_detail_get_column_values_partial_not_found(item_detail: ItemDetail):
    '''
    Test retrieving multiple column values with a non-existent one raises KeyError.
    '''
    
    # Retrieve and verify that no column value is returned for the non-existent ID.
    cvs = item_detail.get_column_values(['status_1', 'non_existent'])
    assert len(cvs) == 1
    assert cvs[0].id == 'status_1'