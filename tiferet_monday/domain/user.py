"""Tiferet Monday User Domain Objects"""

# *** imports

# ** core
from typing import Optional, List

# ** infra
from pydantic import Field

# ** app
from .settings import MondayDomainObject


# *** models

# ** model: account
class Account(MondayDomainObject):
    '''
    Represents a Monday.com account.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the account.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the account.'
    )

    # * attribute: slug
    slug: Optional[str] = Field(
        default=None,
        description='The account slug.'
    )

    # * attribute: tier
    tier: Optional[str] = Field(
        default=None,
        description='The account tier.'
    )

    # * attribute: show_timeline_weekends
    show_timeline_weekends: Optional[bool] = Field(
        default=None,
        description='Whether weekends are shown in the timeline.'
    )

    # * attribute: country_code
    country_code: Optional[str] = Field(
        default=None,
        description='The account country code (ISO3166).'
    )

    # * attribute: logo
    logo: Optional[str] = Field(
        default=None,
        description='The account logo URL.'
    )


# ** model: team
class Team(MondayDomainObject):
    '''
    Represents a team in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the team.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the team.'
    )

    # * attribute: picture_url
    picture_url: Optional[str] = Field(
        default=None,
        description='The team picture URL.'
    )


# ** model: user
class User(MondayDomainObject):
    '''
    Represents a user in Monday.com.
    '''

    # * attribute: id
    id: str = Field(
        ...,
        description='The unique identifier of the user.'
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The user name.'
    )

    # * attribute: email
    email: Optional[str] = Field(
        default=None,
        description='The user email address.'
    )

    # * attribute: phone
    phone: Optional[str] = Field(
        default=None,
        description='The user phone number.'
    )

    # * attribute: mobile_phone
    mobile_phone: Optional[str] = Field(
        default=None,
        description='The user mobile phone number.'
    )

    # * attribute: photo_original
    photo_original: Optional[str] = Field(
        default=None,
        description='The URL of the user photo in original size.'
    )

    # * attribute: photo_thumb
    photo_thumb: Optional[str] = Field(
        default=None,
        description='The URL of the user photo in thumbnail size.'
    )

    # * attribute: title
    title: Optional[str] = Field(
        default=None,
        description='The user title.'
    )

    # * attribute: birthday
    birthday: Optional[str] = Field(
        default=None,
        description='The user birthday (YYYY-MM-DD).'
    )

    # * attribute: country_code
    country_code: Optional[str] = Field(
        default=None,
        description='The user country code.'
    )

    # * attribute: location
    location: Optional[str] = Field(
        default=None,
        description='The user location.'
    )

    # * attribute: time_zone_identifier
    time_zone_identifier: Optional[str] = Field(
        default=None,
        description='The user timezone identifier.'
    )

    # * attribute: is_guest
    is_guest: Optional[bool] = Field(
        default=None,
        description='Whether the user is a guest.'
    )

    # * attribute: is_admin
    is_admin: Optional[bool] = Field(
        default=None,
        description='Whether the user is an admin.'
    )

    # * attribute: is_view_only
    is_view_only: Optional[bool] = Field(
        default=None,
        description='Whether the user is view-only.'
    )

    # * attribute: is_pending
    is_pending: Optional[bool] = Field(
        default=None,
        description='Whether the user has not confirmed their email.'
    )

    # * attribute: enabled
    enabled: Optional[bool] = Field(
        default=None,
        description='Whether the user is enabled.'
    )

    # * attribute: created_at
    created_at: Optional[str] = Field(
        default=None,
        description='The user creation date (ISO8601).'
    )

    # * attribute: url
    url: Optional[str] = Field(
        default=None,
        description='The user profile URL.'
    )
