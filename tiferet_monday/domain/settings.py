"""Tiferet Monday Domain Settings"""

# *** imports

# ** infra
from pydantic import BaseModel, ConfigDict, Field


# *** classes

# ** class: monday_domain_object
class MondayDomainObject(BaseModel):
    '''
    Base domain object for Monday.com entities.
    Extends pydantic BaseModel with shared configuration.
    '''

    # * attribute: model_config
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        coerce_numbers_to_str=True,
    )
