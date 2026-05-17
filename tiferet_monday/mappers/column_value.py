"""Tiferet Monday Column Value Mappers"""

# *** imports

# ** core
from typing import Annotated, Any, ClassVar, Dict, Optional, Union

# ** infra
from pydantic import Discriminator, Tag, Field

# ** app
from .settings import MondayObject
from ..domain.column_value import (
    ColumnValue,
    StatusValue,
    PeopleValue,
    NumbersValue,
    BoardRelationValue,
    FileValue,
    DocValue,
    CheckboxValue,
    DateValue,
    DropdownValue,
    EmailValue,
    LinkValue,
    PhoneValue,
    RatingValue,
    LongTextValue,
    TimelineValue,
)


# *** constants

# ** constant: column_value_registry
COLUMN_VALUE_REGISTRY: Dict[str, type] = {}


# *** functions

# ** function: monday_column_type
def monday_column_type(type_name: str):
    '''
    Decorator that registers a ColumnValue MondayObject subclass
    for discriminated union dispatch.

    :param type_name: The Monday.com column type string (e.g., 'status', 'people').
    :type type_name: str
    '''

    def decorator(cls):

        # Register the class in the column value registry.
        COLUMN_VALUE_REGISTRY[type_name] = cls
        return cls

    return decorator


# ** function: column_value_discriminator
def column_value_discriminator(v: Any) -> str:
    '''
    Extract the Monday column type string from raw data or a model instance.
    Returns 'default' for unregistered types to fall back to the base ColumnValueMondayObject.

    :param v: The raw data dict or model instance.
    :type v: Any
    :return: The column type string for dispatch.
    :rtype: str
    '''

    # Extract the type string.
    if isinstance(v, dict):
        type_str = v.get('type', 'default')
    else:
        type_str = getattr(v, 'type', 'default')

    # Return the type if registered, otherwise fall back to default.
    if type_str in COLUMN_VALUE_REGISTRY:
        return type_str
    return 'default'


# ** function: build_column_value_type
def build_column_value_type() -> type:
    '''
    Build the Pydantic discriminated union from all registered column types.
    Must be called after all @monday_column_type decorators have executed.

    :return: An Annotated Union type for use in Pydantic model fields.
    :rtype: type
    '''

    # Build tagged types from the registry.
    tagged = [
        Annotated[cls, Tag(name)]
        for name, cls in COLUMN_VALUE_REGISTRY.items()
    ]

    # Add the default fallback.
    tagged.append(Annotated[ColumnValueMondayObject, Tag('default')])

    # Return the discriminated union.
    return Annotated[Union[tuple(tagged)], Discriminator(column_value_discriminator)]


# *** mappers

# ** mapper: column_value_monday_object
class ColumnValueMondayObject(ColumnValue, MondayObject):
    '''
    Default MondayObject for column values without a specific typed mapper.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[Optional[str]] = None

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: status_value_monday_object
@monday_column_type('status')
class StatusValueMondayObject(StatusValue, MondayObject):
    '''
    MondayObject for status column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on StatusValue { index text }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: people_value_monday_object
@monday_column_type('people')
class PeopleValueMondayObject(PeopleValue, MondayObject):
    '''
    MondayObject for people column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on PeopleValue { persons_and_teams { id kind } }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: numbers_value_monday_object
@monday_column_type('numbers')
class NumbersValueMondayObject(NumbersValue, MondayObject):
    '''
    MondayObject for numbers column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on NumbersValue { number }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: board_relation_value_monday_object
@monday_column_type('board_relation')
class BoardRelationValueMondayObject(BoardRelationValue, MondayObject):
    '''
    MondayObject for board relation column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on BoardRelationValue { linked_item_ids }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: file_value_monday_object
@monday_column_type('file')
class FileValueMondayObject(FileValue, MondayObject):
    '''
    MondayObject for file column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = (
        '... on FileValue { files { '
        '... on FileDocValue { object_id } '
        '... on FileLinkValue { file_id } '
        '... on FileAssetValue { asset_id } } }'
    )

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: doc_value_monday_object
@monday_column_type('doc')
class DocValueMondayObject(DocValue, MondayObject):
    '''
    MondayObject for document column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on DocValue { file { ... on FileDocValue { object_id } } }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: checkbox_value_monday_object
@monday_column_type('checkbox')
class CheckboxValueMondayObject(CheckboxValue, MondayObject):
    '''
    MondayObject for checkbox column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on CheckboxValue { checked }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: date_value_monday_object
@monday_column_type('date')
class DateValueMondayObject(DateValue, MondayObject):
    '''
    MondayObject for date column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on DateValue { date time }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: dropdown_value_monday_object
@monday_column_type('dropdown')
class DropdownValueMondayObject(DropdownValue, MondayObject):
    '''
    MondayObject for dropdown column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on DropdownValue { values { id name } }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: email_value_monday_object
@monday_column_type('email')
class EmailValueMondayObject(EmailValue, MondayObject):
    '''
    MondayObject for email column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on EmailValue { email label }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: link_value_monday_object
@monday_column_type('link')
class LinkValueMondayObject(LinkValue, MondayObject):
    '''
    MondayObject for link column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on LinkValue { url url_text }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: phone_value_monday_object
@monday_column_type('phone')
class PhoneValueMondayObject(PhoneValue, MondayObject):
    '''
    MondayObject for phone column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on PhoneValue { phone country_short_name }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: rating_value_monday_object
@monday_column_type('rating')
class RatingValueMondayObject(RatingValue, MondayObject):
    '''
    MondayObject for rating column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on RatingValue { rating }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: long_text_value_monday_object
@monday_column_type('long_text')
class LongTextValueMondayObject(LongTextValue, MondayObject):
    '''
    MondayObject for long text column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[Optional[str]] = None

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# ** mapper: timeline_value_monday_object
@monday_column_type('timeline')
class TimelineValueMondayObject(TimelineValue, MondayObject):
    '''
    MondayObject for timeline column values.
    '''

    # * attribute: _GRAPHQL_FRAGMENT
    _GRAPHQL_FRAGMENT: ClassVar[str] = '... on TimelineValue { from_date to_date }'

    # * attribute: name
    name: str = Field(
        default='',
        description='The column title.'
    )


# *** types

# ** type: column_value_type
ColumnValueType = build_column_value_type()


# *** functions (helpers)

# ** function: get_column_value_fragments
def get_column_value_fragments() -> list[str]:
    '''
    Collect all non-None GraphQL inline fragments from registered column types.
    Used by repos to dynamically assemble column_values queries.

    :return: List of GraphQL inline fragment strings.
    :rtype: list[str]
    '''

    # Iterate over registered types and collect fragments.
    fragments = []
    for cls in COLUMN_VALUE_REGISTRY.values():
        fragment = getattr(cls, '_GRAPHQL_FRAGMENT', None)
        if fragment:
            fragments.append(fragment)

    return fragments
