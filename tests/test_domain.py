"""Tiferet Monday Domain Object Tests"""

# *** imports

# ** infra
import pytest

# ** app
from tiferet_monday.domain.board import Board, Column, Group
from tiferet_monday.domain.item import Item, Update, Reply
from tiferet_monday.domain.user import User, Team, Account
from tiferet_monday.domain.workspace import Workspace
from tiferet_monday.domain.tag import Tag
from tiferet_monday.domain.webhook import Webhook


# *** tests

# ** test: board
def test_board():
    board = Board.model_validate({'id': '1', 'name': 'My Board', 'board_kind': 'public', 'state': 'active'})
    assert board.id == '1'
    assert board.name == 'My Board'
    assert board.board_kind == 'public'


# ** test: column
def test_column():
    col = Column.model_validate({'id': 'status', 'name': 'Status', 'type': 'status'})
    assert col.id == 'status'
    assert col.type == 'status'


# ** test: group
def test_group():
    grp = Group.model_validate({'id': 'new_group', 'name': 'New Group', 'color': '#FF0000'})
    assert grp.id == 'new_group'
    assert grp.color == '#FF0000'


# ** test: item
def test_item():
    item = Item.model_validate({'id': '100', 'name': 'Task 1', 'board_id': '1', 'state': 'active'})
    assert item.id == '100'
    assert item.board_id == '1'


# ** test: update
def test_update():
    update = Update.model_validate({'id': '200', 'body': '<p>Hello</p>', 'text_body': 'Hello', 'replies': []})
    assert update.id == '200'
    assert update.text_body == 'Hello'


# ** test: reply
def test_reply():
    reply = Reply.model_validate({'id': '300', 'body': 'Thanks!'})
    assert reply.id == '300'


# ** test: update_with_replies
def test_update_with_replies():
    update = Update.model_validate({
        'id': '200', 'body': 'Comment',
        'replies': [{'id': '301', 'body': 'Reply 1'}, {'id': '302', 'body': 'Reply 2'}]
    })
    assert len(update.replies) == 2
    assert update.replies[0].id == '301'


# ** test: user
def test_user():
    user = User.model_validate({'id': '10', 'name': 'Alice', 'email': 'alice@example.com', 'is_admin': True})
    assert user.name == 'Alice'
    assert user.is_admin is True


# ** test: team
def test_team():
    team = Team.model_validate({'id': '20', 'name': 'Engineering'})
    assert team.name == 'Engineering'


# ** test: account
def test_account():
    acct = Account.model_validate({'id': '30', 'name': 'Acme Corp', 'slug': 'acme', 'tier': 'enterprise'})
    assert acct.slug == 'acme'
    assert acct.tier == 'enterprise'


# ** test: workspace
def test_workspace():
    ws = Workspace.model_validate({'id': '40', 'name': 'Marketing', 'kind': 'open'})
    assert ws.kind == 'open'


# ** test: tag
def test_tag():
    tag = Tag.model_validate({'id': '50', 'name': 'urgent', 'color': '#FF0000'})
    assert tag.name == 'urgent'


# ** test: webhook
def test_webhook():
    wh = Webhook.model_validate({'id': '60', 'board_id': '1', 'event': 'change_column_value'})
    assert wh.event == 'change_column_value'


# ** test: domain_objects_ignore_extra_fields
def test_domain_objects_ignore_extra_fields():
    '''All domain objects use extra=ignore and should silently drop unknown fields.'''
    board = Board.model_validate({'id': '1', 'name': 'B', 'unknown_field': 'xyz'})
    assert board.id == '1'
    assert not hasattr(board, 'unknown_field')
