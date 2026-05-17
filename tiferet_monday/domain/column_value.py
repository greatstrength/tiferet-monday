"""Tiferet Monday Column Value Domain Objects"""

# *** imports

# ** core
from typing import Optional, List, Literal

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: column_value
class ColumnValue(MondayDomainObject):
    '''
    Base column value in a Monday.com item.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the column.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The column title.'
    )

    # * attribute: type
    type: str = Field(
        ...,
        description='The type of the column value.'
    )

    # * attribute: text
    text: Optional[str] = Field(
        default=None,
        description='The text representation of the column value.'
    )

    # * attribute: value
    value: Optional[str] = Field(
        default=None,
        description='The raw JSON value of the column.'
    )

    # * attribute: description
    description: Optional[str] = Field(
        default=None,
        description='A description of the column.'
    )

    # * attribute: settings_str
    settings_str: Optional[str] = Field(
        default=None,
        description='A JSON string representing the column settings.'
    )


# ** model: status_value
class StatusValue(ColumnValue):
    '''
    A status column value.
    '''

    # * attribute: type
    type: Literal['status'] = 'status'

    # * attribute: index
    index: Optional[int] = Field(
        default=None,
        description='The index of the status label.'
    )


# ** model: people_value
class PeopleValue(ColumnValue):
    '''
    A people column value.
    '''

    # * attribute: type
    type: Literal['people'] = 'people'

    # * attribute: persons_and_teams
    persons_and_teams: List[dict] = Field(
        default_factory=list,
        description='A list of persons and teams assigned.'
    )

    # * method: get_person_ids
    def get_person_ids(self) -> List[str]:
        '''
        Extract person IDs from the persons_and_teams list.

        :return: A list of person IDs.
        :rtype: List[str]
        '''

        # Filter for person kind and extract IDs.
        return [
            entry['id'] for entry in self.persons_and_teams
            if entry.get('kind') == 'person'
        ]


# ** model: numbers_value
class NumbersValue(ColumnValue):
    '''
    A numbers column value.
    '''

    # * attribute: type
    type: Literal['numbers'] = 'numbers'

    # * attribute: number
    number: Optional[float] = Field(
        default=None,
        description='The numeric value.'
    )


# ** model: board_relation_value
class BoardRelationValue(ColumnValue):
    '''
    A board relation column value.
    '''

    # * attribute: type
    type: Literal['board_relation'] = 'board_relation'

    # * attribute: linked_item_ids
    linked_item_ids: List[int] = Field(
        default_factory=list,
        description='A list of linked item IDs.'
    )


# ** model: file_value
class FileValue(ColumnValue):
    '''
    A file column value.
    '''

    # * attribute: type
    type: Literal['file'] = 'file'

    # * attribute: files
    files: List[dict] = Field(
        default_factory=list,
        description='A list of files associated with this column.'
    )

    # * method: get_object_ids
    def get_object_ids(self) -> List[str]:
        '''
        Extract object IDs from the files list.

        :return: A list of object IDs.
        :rtype: List[str]
        '''

        # Extract object_id from each file dictionary.
        return [
            f['object_id'] for f in self.files
            if 'object_id' in f
        ]


# ** model: doc_value
class DocValue(ColumnValue):
    '''
    A document column value.
    '''

    # * attribute: type
    type: Literal['doc'] = 'doc'

    # * attribute: file
    file: Optional[dict] = Field(
        default=None,
        description='The file reference for this doc column.'
    )

    # * method: get_object_id
    def get_object_id(self) -> Optional[str]:
        '''
        Extract the object ID from the file reference.

        :return: The object ID, or None.
        :rtype: Optional[str]
        '''

        # Return the object_id from the file dictionary.
        if self.file:
            return self.file.get('object_id')
        return None


# ** model: checkbox_value
class CheckboxValue(ColumnValue):
    '''
    A checkbox column value.
    '''

    # * attribute: type
    type: Literal['checkbox'] = 'checkbox'

    # * attribute: checked
    checked: Optional[bool] = Field(
        default=None,
        description='Whether the checkbox is checked.'
    )


# ** model: date_value
class DateValue(ColumnValue):
    '''
    A date column value.
    '''

    # * attribute: type
    type: Literal['date'] = 'date'

    # * attribute: date
    date: Optional[str] = Field(
        default=None,
        description='The date string (YYYY-MM-DD).'
    )

    # * attribute: time
    time: Optional[str] = Field(
        default=None,
        description='The time string (HH:MM:SS).'
    )


# ** model: dropdown_value
class DropdownValue(ColumnValue):
    '''
    A dropdown column value.
    '''

    # * attribute: type
    type: Literal['dropdown'] = 'dropdown'

    # * attribute: values
    values: List[dict] = Field(
        default_factory=list,
        description='The selected dropdown values.'
    )


# ** model: email_value
class EmailValue(ColumnValue):
    '''
    An email column value.
    '''

    # * attribute: type
    type: Literal['email'] = 'email'

    # * attribute: email
    email: Optional[str] = Field(
        default=None,
        description='The email address.'
    )

    # * attribute: label
    label: Optional[str] = Field(
        default=None,
        description='The display label for the email.'
    )


# ** model: link_value
class LinkValue(ColumnValue):
    '''
    A link column value.
    '''

    # * attribute: type
    type: Literal['link'] = 'link'

    # * attribute: url
    url: Optional[str] = Field(
        default=None,
        description='The URL.'
    )

    # * attribute: url_text
    url_text: Optional[str] = Field(
        default=None,
        description='The display text for the URL.'
    )


# ** model: phone_value
class PhoneValue(ColumnValue):
    '''
    A phone column value.
    '''

    # * attribute: type
    type: Literal['phone'] = 'phone'

    # * attribute: phone
    phone: Optional[str] = Field(
        default=None,
        description='The phone number.'
    )

    # * attribute: country_short_name
    country_short_name: Optional[str] = Field(
        default=None,
        description='The country short code.'
    )


# ** model: rating_value
class RatingValue(ColumnValue):
    '''
    A rating column value.
    '''

    # * attribute: type
    type: Literal['rating'] = 'rating'

    # * attribute: rating
    rating: Optional[int] = Field(
        default=None,
        description='The rating value (1-5).'
    )


# ** model: long_text_value
class LongTextValue(ColumnValue):
    '''
    A long text column value.
    '''

    # * attribute: type
    type: Literal['long_text'] = 'long_text'


# ** model: timeline_value
class TimelineValue(ColumnValue):
    '''
    A timeline column value.
    '''

    # * attribute: type
    type: Literal['timeline'] = 'timeline'

    # * attribute: from_date
    from_date: Optional[str] = Field(
        default=None,
        description='The start date of the timeline.'
    )

    # * attribute: to_date
    to_date: Optional[str] = Field(
        default=None,
        description='The end date of the timeline.'
    )
