"""Tiferet Monday Domain Event Tests"""

# *** imports

# ** infra
import pytest
from unittest.mock import Mock

# ** app
from tiferet_monday.events.board import GetBoard, CreateBoard, QueryBoardColumns, QueryBoardGroups, QueryBoardItems, CreateBoardItem
from tiferet_monday.events.item import GetItems, GetItemDetail, QueryColumnValues, ChangeColumnValue, CreateSubitem, ArchiveItem, CreateItemUpdate
from tiferet_monday.events.user import GetUsers, GetMe, GetTeams, GetAccount
from tiferet_monday.events.update import QueryUpdates, CreateUpdate, CreateNotification, DeleteUpdate
from tiferet_monday.events.workspace import GetWorkspaces, CreateWorkspace, DeleteWorkspace
from tiferet_monday.events.tag import GetTags, CreateOrGetTag
from tiferet_monday.events.webhook import CreateWebhook, DeleteWebhook
from tiferet_monday.domain.board import Board, Column, Group
from tiferet_monday.domain.user import User, Team, Account
from tiferet_monday.domain.workspace import Workspace
from tiferet_monday.domain.tag import Tag
from tiferet_monday.domain.webhook import Webhook
from tiferet_monday.domain.item import Update


# *** tests: board events

# ** test: get_board_found
def test_get_board_found():
    svc = Mock()
    svc.get_boards.return_value = [{'id': '1', 'name': 'Board'}]
    event = GetBoard(board_service=svc)
    result = event.execute(board_id='1')
    assert isinstance(result, Board)
    assert result.id == '1'
    svc.get_boards.assert_called_once_with(ids=['1'], limit=1)


# ** test: get_board_not_found
def test_get_board_not_found():
    svc = Mock()
    svc.get_boards.return_value = []
    event = GetBoard(board_service=svc)
    result = event.execute(board_id='999')
    assert result is None


# ** test: create_board
def test_create_board():
    svc = Mock()
    svc.create_board.return_value = {'id': '2', 'name': 'New', 'board_kind': 'public'}
    event = CreateBoard(board_service=svc)
    result = event.execute(board_name='New', board_kind='public')
    assert isinstance(result, Board)
    assert result.name == 'New'


# ** test: query_board_columns
def test_query_board_columns():
    svc = Mock()
    svc.query_columns.return_value = [{'id': 'c1', 'name': 'Status', 'type': 'status'}]
    event = QueryBoardColumns(board_service=svc)
    result = event.execute(board_id='1')
    assert len(result) == 1
    assert isinstance(result[0], Column)


# ** test: query_board_groups
def test_query_board_groups():
    svc = Mock()
    svc.query_groups.return_value = [{'id': 'g1', 'name': 'Group'}]
    event = QueryBoardGroups(board_service=svc)
    result = event.execute(board_id='1')
    assert isinstance(result[0], Group)


# ** test: query_board_items
def test_query_board_items():
    svc = Mock()
    svc.query_items_page.return_value = [{'id': '10', 'name': 'Item'}]
    event = QueryBoardItems(board_service=svc)
    result = event.execute(board_id='1')
    assert result == [{'id': '10', 'name': 'Item'}]


# ** test: create_board_item
def test_create_board_item():
    svc = Mock()
    svc.create_item.return_value = {'id': '11', 'name': 'New Item'}
    event = CreateBoardItem(board_service=svc)
    result = event.execute(board_id='1', item_name='New Item')
    assert result == {'id': '11', 'name': 'New Item'}


# *** tests: item events

# ** test: get_items
def test_get_items():
    svc = Mock()
    svc.query_items_by_ids.return_value = [{'id': '1', 'name': 'A'}, {'id': '2', 'name': 'B'}]
    event = GetItems(item_service=svc)
    result = event.execute(item_ids=['1', '2'])
    assert len(result) == 2


# ** test: archive_item
def test_archive_item():
    svc = Mock()
    svc.archive_item.return_value = {'id': '1'}
    event = ArchiveItem(item_service=svc)
    result = event.execute(item_id='1')
    assert result == {'id': '1'}


# ** test: create_item_update
def test_create_item_update():
    svc = Mock()
    svc.create_update.return_value = {'id': '500', 'body': 'Hello'}
    event = CreateItemUpdate(item_service=svc)
    result = event.execute(item_id='1', body='Hello')
    assert result == {'id': '500', 'body': 'Hello'}


# *** tests: user events

# ** test: get_users
def test_get_users():
    svc = Mock()
    svc.get_users.return_value = [{'id': '1', 'name': 'Alice'}]
    event = GetUsers(user_service=svc)
    result = event.execute()
    assert result == [{'id': '1', 'name': 'Alice'}]


# ** test: get_me
def test_get_me():
    svc = Mock()
    svc.get_me.return_value = {'id': '1', 'name': 'Me'}
    event = GetMe(user_service=svc)
    result = event.execute()
    assert result == {'id': '1', 'name': 'Me'}


# ** test: get_teams
def test_get_teams():
    svc = Mock()
    svc.get_teams.return_value = [{'id': '1', 'name': 'Eng'}]
    event = GetTeams(user_service=svc)
    result = event.execute()
    assert len(result) == 1
    assert isinstance(result[0], Team)


# ** test: get_account
def test_get_account():
    svc = Mock()
    svc.get_account.return_value = {'id': '1', 'name': 'Acme'}
    event = GetAccount(user_service=svc)
    result = event.execute()
    assert isinstance(result, Account)
    assert result.name == 'Acme'


# ** test: get_account_none
def test_get_account_none():
    svc = Mock()
    svc.get_account.return_value = None
    event = GetAccount(user_service=svc)
    assert event.execute() is None


# *** tests: update events

# ** test: query_updates
def test_query_updates():
    svc = Mock()
    svc.query_updates.return_value = [{'id': '1', 'body': 'Hi', 'replies': []}]
    event = QueryUpdates(update_service=svc)
    result = event.execute(item_id='100')
    assert len(result) == 1
    assert isinstance(result[0], Update)


# ** test: create_update_event
def test_create_update_event():
    svc = Mock()
    svc.create_update.return_value = {'id': '2', 'body': 'Comment', 'replies': []}
    event = CreateUpdate(update_service=svc)
    result = event.execute(item_id='100', body='Comment')
    assert isinstance(result, Update)
    assert result.body == 'Comment'


# ** test: create_notification
def test_create_notification():
    svc = Mock()
    svc.create_notification.return_value = {'text': 'Notified'}
    event = CreateNotification(update_service=svc)
    result = event.execute(user_id='1', target_id='100', text='Notified')
    assert result == {'text': 'Notified'}


# ** test: delete_update
def test_delete_update():
    svc = Mock()
    svc.delete_update.return_value = {'id': '1'}
    event = DeleteUpdate(update_service=svc)
    result = event.execute(update_id='1')
    assert result == {'id': '1'}


# *** tests: workspace events

# ** test: get_workspaces
def test_get_workspaces():
    svc = Mock()
    svc.get_workspaces.return_value = [{'id': '1', 'name': 'WS'}]
    event = GetWorkspaces(workspace_service=svc)
    result = event.execute()
    assert isinstance(result[0], Workspace)


# ** test: create_workspace
def test_create_workspace_event():
    svc = Mock()
    svc.create_workspace.return_value = {'id': '2', 'name': 'New WS'}
    event = CreateWorkspace(workspace_service=svc)
    result = event.execute(name='New WS')
    assert isinstance(result, Workspace)


# ** test: delete_workspace
def test_delete_workspace():
    svc = Mock()
    svc.delete_workspace.return_value = {'id': '1'}
    event = DeleteWorkspace(workspace_service=svc)
    result = event.execute(workspace_id='1')
    assert result == {'id': '1'}


# *** tests: tag events

# ** test: get_tags
def test_get_tags():
    svc = Mock()
    svc.get_tags.return_value = [{'id': '1', 'name': 'urgent'}]
    event = GetTags(tag_service=svc)
    result = event.execute()
    assert isinstance(result[0], Tag)


# ** test: create_or_get_tag
def test_create_or_get_tag():
    svc = Mock()
    svc.create_or_get_tag.return_value = {'id': '2', 'name': 'bug'}
    event = CreateOrGetTag(tag_service=svc)
    result = event.execute(tag_name='bug')
    assert isinstance(result, Tag)


# *** tests: webhook events

# ** test: create_webhook
def test_create_webhook():
    svc = Mock()
    svc.create_webhook.return_value = {'id': '1', 'board_id': '100'}
    event = CreateWebhook(webhook_service=svc)
    result = event.execute(board_id='100', url='https://example.com/hook', event='change_column_value')
    assert isinstance(result, Webhook)


# ** test: delete_webhook
def test_delete_webhook():
    svc = Mock()
    svc.delete_webhook.return_value = {'id': '1'}
    event = DeleteWebhook(webhook_service=svc)
    result = event.execute(webhook_id='1')
    assert result == {'id': '1'}
