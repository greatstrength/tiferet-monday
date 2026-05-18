"""Tiferet Monday Repository Integration Tests (mock API)"""

# *** imports

# ** infra
import pytest
from unittest.mock import patch, Mock

# ** app
from tiferet_monday.repos.board import BoardApiProxy
from tiferet_monday.repos.item import ItemApiProxy
from tiferet_monday.repos.user import UserApiProxy
from tiferet_monday.repos.update import UpdateApiProxy
from tiferet_monday.repos.workspace import WorkspaceApiProxy
from tiferet_monday.repos.tag import TagApiProxy
from tiferet_monday.repos.webhook import WebhookApiProxy
from tiferet_monday.repos.settings import MondayApiError
from tiferet_monday.assets import const


# *** helpers

def _mock_response(data: dict):
    '''Create a mock requests.post response with the given data payload.'''
    mock_resp = Mock()
    mock_resp.json.return_value = {'data': data}
    return mock_resp


def _mock_error_response(errors: list):
    '''Create a mock error response.'''
    mock_resp = Mock()
    mock_resp.json.return_value = {'errors': errors}
    return mock_resp


# *** tests: board_api_proxy

# ** test: get_boards
@patch('tiferet_monday.repos.settings.requests.post')
def test_board_get_boards(mock_post):
    mock_post.return_value = _mock_response({'boards': [{'id': '1', 'name': 'Board 1'}]})
    proxy = BoardApiProxy('test_key')
    result = proxy.get_boards(limit=10)
    assert len(result) == 1
    assert result[0]['id'] == '1'
    mock_post.assert_called_once()


# ** test: create_board
@patch('tiferet_monday.repos.settings.requests.post')
def test_board_create(mock_post):
    mock_post.return_value = _mock_response({'create_board': {'id': '2', 'name': 'New'}})
    proxy = BoardApiProxy('test_key')
    result = proxy.create_board(board_name='New', board_kind='public')
    assert result['id'] == '2'


# ** test: query_columns
@patch('tiferet_monday.repos.settings.requests.post')
def test_board_query_columns(mock_post):
    mock_post.return_value = _mock_response({'boards': [{'columns': [{'id': 'c1', 'title': 'Status', 'type': 'status'}]}]})
    proxy = BoardApiProxy('test_key')
    result = proxy.query_columns(board_id='1')
    assert len(result) == 1


# *** tests: item_api_proxy

# ** test: query_items_by_ids
@patch('tiferet_monday.repos.settings.requests.post')
def test_item_query_by_ids(mock_post):
    mock_post.return_value = _mock_response({'items': [{'id': '10', 'name': 'Task'}]})
    proxy = ItemApiProxy('test_key')
    result = proxy.query_items_by_ids(item_ids=['10'])
    assert result[0]['id'] == '10'


# ** test: archive_item
@patch('tiferet_monday.repos.settings.requests.post')
def test_item_archive(mock_post):
    mock_post.return_value = _mock_response({'archive_item': {'id': '10'}})
    proxy = ItemApiProxy('test_key')
    result = proxy.archive_item(item_id='10')
    assert result['id'] == '10'


# *** tests: user_api_proxy

# ** test: get_users
@patch('tiferet_monday.repos.settings.requests.post')
def test_user_get_users(mock_post):
    mock_post.return_value = _mock_response({'users': [{'id': '1', 'name': 'Alice'}]})
    proxy = UserApiProxy('test_key')
    result = proxy.get_users(limit=10)
    assert result[0]['name'] == 'Alice'


# ** test: get_me
@patch('tiferet_monday.repos.settings.requests.post')
def test_user_get_me(mock_post):
    mock_post.return_value = _mock_response({'me': {'id': '1', 'name': 'Me'}})
    proxy = UserApiProxy('test_key')
    result = proxy.get_me()
    assert result['id'] == '1'


# ** test: get_teams
@patch('tiferet_monday.repos.settings.requests.post')
def test_user_get_teams(mock_post):
    mock_post.return_value = _mock_response({'teams': [{'id': '1', 'name': 'Eng'}]})
    proxy = UserApiProxy('test_key')
    result = proxy.get_teams()
    assert result[0]['name'] == 'Eng'


# ** test: get_account
@patch('tiferet_monday.repos.settings.requests.post')
def test_user_get_account(mock_post):
    mock_post.return_value = _mock_response({'me': {'account': {'id': '1', 'name': 'Acme'}}})
    proxy = UserApiProxy('test_key')
    result = proxy.get_account()
    assert result['name'] == 'Acme'


# *** tests: update_api_proxy

# ** test: query_updates_global
@patch('tiferet_monday.repos.settings.requests.post')
def test_update_query_global(mock_post):
    mock_post.return_value = _mock_response({'updates': [{'id': '1', 'body': 'Hi'}]})
    proxy = UpdateApiProxy('test_key')
    result = proxy.query_updates(limit=5)
    assert result[0]['id'] == '1'


# ** test: query_updates_by_item
@patch('tiferet_monday.repos.settings.requests.post')
def test_update_query_by_item(mock_post):
    mock_post.return_value = _mock_response({'items': [{'updates': [{'id': '2', 'body': 'Comment'}]}]})
    proxy = UpdateApiProxy('test_key')
    result = proxy.query_updates(item_id='100', limit=5)
    assert result[0]['id'] == '2'


# ** test: create_notification
@patch('tiferet_monday.repos.settings.requests.post')
def test_update_create_notification(mock_post):
    mock_post.return_value = _mock_response({'create_notification': {'text': 'Notified'}})
    proxy = UpdateApiProxy('test_key')
    result = proxy.create_notification(user_id='1', target_id='100', text='Notified')
    assert result['text'] == 'Notified'


# *** tests: workspace_api_proxy

# ** test: get_workspaces
@patch('tiferet_monday.repos.settings.requests.post')
def test_workspace_get(mock_post):
    mock_post.return_value = _mock_response({'workspaces': [{'id': '1', 'name': 'WS'}]})
    proxy = WorkspaceApiProxy('test_key')
    result = proxy.get_workspaces()
    assert result[0]['name'] == 'WS'


# ** test: create_workspace
@patch('tiferet_monday.repos.settings.requests.post')
def test_workspace_create(mock_post):
    mock_post.return_value = _mock_response({'create_workspace': {'id': '2', 'name': 'New'}})
    proxy = WorkspaceApiProxy('test_key')
    result = proxy.create_workspace(name='New')
    assert result['id'] == '2'


# *** tests: tag_api_proxy

# ** test: get_tags
@patch('tiferet_monday.repos.settings.requests.post')
def test_tag_get(mock_post):
    mock_post.return_value = _mock_response({'tags': [{'id': '1', 'name': 'urgent'}]})
    proxy = TagApiProxy('test_key')
    result = proxy.get_tags()
    assert result[0]['name'] == 'urgent'


# ** test: create_or_get_tag
@patch('tiferet_monday.repos.settings.requests.post')
def test_tag_create_or_get(mock_post):
    mock_post.return_value = _mock_response({'create_or_get_tag': {'id': '2', 'name': 'bug'}})
    proxy = TagApiProxy('test_key')
    result = proxy.create_or_get_tag(tag_name='bug')
    assert result['name'] == 'bug'


# *** tests: webhook_api_proxy

# ** test: create_webhook
@patch('tiferet_monday.repos.settings.requests.post')
def test_webhook_create(mock_post):
    mock_post.return_value = _mock_response({'create_webhook': {'id': '1', 'board_id': '100'}})
    proxy = WebhookApiProxy('test_key')
    result = proxy.create_webhook(board_id='100', url='https://example.com/hook', event='change_column_value')
    assert result['id'] == '1'


# ** test: delete_webhook
@patch('tiferet_monday.repos.settings.requests.post')
def test_webhook_delete(mock_post):
    mock_post.return_value = _mock_response({'delete_webhook': {'id': '1'}})
    proxy = WebhookApiProxy('test_key')
    result = proxy.delete_webhook(webhook_id='1')
    assert result['id'] == '1'


# *** tests: error handling

# ** test: api_error_on_errors
@patch('tiferet_monday.repos.settings.requests.post')
def test_api_error_raised(mock_post):
    mock_post.return_value = _mock_error_response([{'message': 'Something went wrong'}])
    proxy = BoardApiProxy('test_key')
    with pytest.raises(MondayApiError) as exc_info:
        proxy.get_boards()
    assert exc_info.value.error_code == const.MONDAY_API_ERROR_ID


# ** test: complexity_budget_error
@patch('tiferet_monday.repos.settings.requests.post')
def test_complexity_budget_error(mock_post):
    mock_post.return_value = _mock_error_response([{
        'message': 'Budget exhausted',
        'extensions': {'code': const.COMPLEXITY_BUDGET_EXHAUSTED_ID, 'retry_in_seconds': 30}
    }])
    proxy = BoardApiProxy('test_key')
    with pytest.raises(MondayApiError) as exc_info:
        proxy.get_boards()
    assert exc_info.value.error_code == const.COMPLEXITY_BUDGET_EXHAUSTED_ID
