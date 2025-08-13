# *** imports

# ** infra
from tiferet.data import *

# ** app
from ..models.board import *
from ..contracts.board import (
    ColumnContract,
    GroupContract
)

# *** data

# ** data: column_data
class ColumnData(DataObject, Column):
    """
    Represents a column in a Monday.com board.
    """

    class Options():
        """
        Options for the ColumnData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('title'),
            to_data=DataObject.allow()
        )

    # * attribute: name
    name = StringType(
        metadata=dict(
            description='The name of the column.'
        )
    )

    # * attribute: title
    title = StringType(
        required=True,
        metadata=dict(
            description='The title of the column.'
        )
    )

    # * method: map
    def map(self, **kwargs) -> ColumnContract:
        """
        Maps the ColumnData to a ColumnContract.

        :param kwargs: Additional keyword arguments.
        :return: ColumnContract instance.
        """
        return super().map(
            Column,
            name=self.title,
        )

# ** data: group_data
class GroupData(DataObject, Group):
    """
    Represents a group in a Monday.com board.
    """

    class Options():
        """
        Options for the GroupData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.deny('title'),
            to_data=DataObject.allow()
        )

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the group.'
        )
    )

    # * attribute: name
    title = StringType(
        required=True,
        metadata=dict(
            description='The title of the group.'
        )
    )

    # * attribute: position
    position = StringType(
        metadata=dict(
            description='The position of the group in the board.'
        )
    )

    # * method: map
    def map(self, **kwargs) -> GroupContract:
        """
        Maps the GroupData to a GroupContract.

        :param kwargs: Additional keyword arguments.
        :return: GroupContract instance.
        """
        return super().map(
            Group,
            name=self.title,
        )