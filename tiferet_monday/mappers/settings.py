"""Tiferet Monday Mappers Settings"""

# *** imports

# ** infra
from pydantic import ConfigDict

# ** app
from ..domain.settings import MondayDomainObject


# *** classes

# ** class: monday_object
class MondayObject(MondayDomainObject):
    '''
    Base transfer object for Monday.com API JSON responses.
    Extends MondayDomainObject with lenient config for API data mapping.

    The MondayObject suffix communicates that the data source is the
    Monday.com GraphQL API (JSON responses), not YAML configuration files.
    '''

    # * attribute: model_config
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        validate_assignment=False,
        arbitrary_types_allowed=True,
        coerce_numbers_to_str=True,
    )
