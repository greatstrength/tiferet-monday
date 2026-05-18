"""Tiferet Monday Column Value Dispatch Tests"""

# *** imports

# ** infra
import pytest
import pydantic
from typing import List

# ** app
from tiferet_monday.mappers.column_value import (
    ColumnValueType,
    COLUMN_VALUE_REGISTRY,
    get_column_value_fragments,
    ColumnValueMondayObject,
)
from tiferet_monday.domain.column_value import *


# *** helpers

class _Wrapper(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra='ignore')
    cvs: List[ColumnValueType] = []


def _dispatch(cv_data: dict):
    '''Dispatch a single column value dict through the discriminated union.'''
    wrapper = _Wrapper.model_validate({'cvs': [cv_data]})
    return wrapper.cvs[0]


# *** tests

# ** test: all_registered_types
EXPECTED_TYPES = [
    'status', 'people', 'numbers', 'board_relation', 'file', 'doc',
    'checkbox', 'date', 'dropdown', 'email', 'link', 'phone', 'rating',
    'long_text', 'timeline', 'tags', 'color_picker', 'country', 'formula',
    'mirror', 'connect_boards', 'dependency', 'time_tracking', 'vote',
    'world_clock', 'creation_log', 'last_updated',
]


def test_all_types_registered():
    '''All 27 column value types should be registered.'''
    for t in EXPECTED_TYPES:
        assert t in COLUMN_VALUE_REGISTRY, f'{t} not registered'
    assert len(COLUMN_VALUE_REGISTRY) == 27


# ** test: dispatch_status
def test_dispatch_status():
    cv = _dispatch({'id': 'c1', 'name': 'Status', 'type': 'status', 'index': 1, 'text': 'Done'})
    assert isinstance(cv, StatusValue)
    assert cv.index == 1


# ** test: dispatch_people
def test_dispatch_people():
    cv = _dispatch({'id': 'c2', 'name': 'Owner', 'type': 'people', 'persons_and_teams': [{'id': 1, 'kind': 'person'}]})
    assert isinstance(cv, PeopleValue)
    assert cv.get_person_ids() == [1]


# ** test: dispatch_numbers
def test_dispatch_numbers():
    cv = _dispatch({'id': 'c3', 'name': 'Points', 'type': 'numbers', 'number': 42.5})
    assert isinstance(cv, NumbersValue)
    assert cv.number == 42.5


# ** test: dispatch_checkbox
def test_dispatch_checkbox():
    cv = _dispatch({'id': 'c4', 'name': 'Done', 'type': 'checkbox', 'checked': True})
    assert isinstance(cv, CheckboxValue)
    assert cv.checked is True


# ** test: dispatch_date
def test_dispatch_date():
    cv = _dispatch({'id': 'c5', 'name': 'Due', 'type': 'date', 'date': '2026-01-01', 'time': '10:00:00'})
    assert isinstance(cv, DateValue)
    assert cv.date == '2026-01-01'


# ** test: dispatch_email
def test_dispatch_email():
    cv = _dispatch({'id': 'c6', 'name': 'Email', 'type': 'email', 'email': 'a@b.com', 'label': 'Work'})
    assert isinstance(cv, EmailValue)
    assert cv.email == 'a@b.com'


# ** test: dispatch_link
def test_dispatch_link():
    cv = _dispatch({'id': 'c7', 'name': 'Link', 'type': 'link', 'url': 'https://x.com', 'url_text': 'X'})
    assert isinstance(cv, LinkValue)
    assert cv.url == 'https://x.com'


# ** test: dispatch_phone
def test_dispatch_phone():
    cv = _dispatch({'id': 'c8', 'name': 'Phone', 'type': 'phone', 'phone': '555-0100', 'country_short_name': 'US'})
    assert isinstance(cv, PhoneValue)
    assert cv.country_short_name == 'US'


# ** test: dispatch_rating
def test_dispatch_rating():
    cv = _dispatch({'id': 'c9', 'name': 'Rating', 'type': 'rating', 'rating': 4})
    assert isinstance(cv, RatingValue)
    assert cv.rating == 4


# ** test: dispatch_timeline
def test_dispatch_timeline():
    cv = _dispatch({'id': 'c10', 'name': 'Timeline', 'type': 'timeline', 'from_date': '2026-01-01', 'to_date': '2026-02-01'})
    assert isinstance(cv, TimelineValue)


# ** test: dispatch_tags
def test_dispatch_tags():
    cv = _dispatch({'id': 'c11', 'name': 'Tags', 'type': 'tags', 'tag_ids': [1, 2, 3]})
    assert isinstance(cv, TagsValue)
    assert cv.tag_ids == [1, 2, 3]


# ** test: dispatch_color_picker
def test_dispatch_color_picker():
    cv = _dispatch({'id': 'c12', 'name': 'Color', 'type': 'color_picker', 'color': '#FF0000'})
    assert isinstance(cv, ColorPickerValue)
    assert cv.color == '#FF0000'


# ** test: dispatch_country
def test_dispatch_country():
    cv = _dispatch({'id': 'c13', 'name': 'Country', 'type': 'country', 'country_code': 'US', 'country_name': 'United States'})
    assert isinstance(cv, CountryValue)
    assert cv.country_code == 'US'


# ** test: dispatch_time_tracking
def test_dispatch_time_tracking():
    cv = _dispatch({'id': 'c14', 'name': 'Time', 'type': 'time_tracking', 'duration': 3600, 'running': False})
    assert isinstance(cv, TimeTrackingValue)
    assert cv.duration == 3600


# ** test: dispatch_vote
def test_dispatch_vote():
    cv = _dispatch({'id': 'c15', 'name': 'Vote', 'type': 'vote', 'voter_ids': [1, 2]})
    assert isinstance(cv, VoteValue)
    assert cv.voter_ids == [1, 2]


# ** test: dispatch_world_clock
def test_dispatch_world_clock():
    cv = _dispatch({'id': 'c16', 'name': 'Clock', 'type': 'world_clock', 'timezone': 'America/New_York'})
    assert isinstance(cv, WorldClockValue)
    assert cv.timezone == 'America/New_York'


# ** test: dispatch_creation_log
def test_dispatch_creation_log():
    cv = _dispatch({'id': 'c17', 'name': 'Created', 'type': 'creation_log', 'created_at': '2026-01-01T00:00:00Z', 'creator_id': '10'})
    assert isinstance(cv, CreationLogValue)
    assert cv.creator_id == '10'


# ** test: dispatch_last_updated
def test_dispatch_last_updated():
    cv = _dispatch({'id': 'c18', 'name': 'Updated', 'type': 'last_updated', 'updated_at': '2026-01-02T00:00:00Z', 'updater_id': '11'})
    assert isinstance(cv, LastUpdatedValue)
    assert cv.updater_id == '11'


# ** test: dispatch_unknown_type_falls_back_to_default
def test_dispatch_unknown_falls_back():
    cv = _dispatch({'id': 'c99', 'name': 'Unknown', 'type': 'some_future_type'})
    assert isinstance(cv, ColumnValueMondayObject)
    assert cv.type == 'some_future_type'


# ** test: get_column_value_fragments_count
def test_fragments_count():
    '''Fragments should exist for most types (excluding formula and long_text which have None).'''
    fragments = get_column_value_fragments()
    # 27 types - 2 with None fragments (formula, long_text) = 25
    assert len(fragments) == 25
