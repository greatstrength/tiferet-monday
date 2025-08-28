# *** imports

# ** app
from tiferet.models import *

# ** model: column_value
class ColumnValue(ValueObject):
    """
    Represents a column value in a Monday.com item.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the column.'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The column title.'
        )
    )

    # * attribute: type
    type = StringType(
        required=True,
        metadata=dict(
            description='The type of the column value.'
        )
    )

    # * attribute: value
    value = StringType(
        metadata=dict(
            description='The actual value of the column.'
        )
    )

    # * attribute: description
    description = StringType(
        metadata=dict(
            description='A description of the column.'
        )
    )
    
    # * attribute: settings_str
    settings_str = StringType(
        metadata=dict(
            description='A JSON string representing the settings of the column.'
        )
    )

    # * method: new
    @staticmethod
    def new(
        id: str,
        name: str,
        type: str,
        value: str = None,
        description: str = None,
        settings_str: str = None,
        **kwargs
    ) -> 'ColumnValue':
        """
        Creates a new instance of ColumnValue.

        :param id: The unique identifier of the column.
        :type id: str
        :param name: The column title.
        :type name: str
        :param type: The type of the column value.
        :type type: str
        :param value: The actual value of the column.
        :type value: str, optional
        :param description: A description of the column.
        :type description: str, optional
        :param settings_str: A JSON string representing the settings of the column.
        :type settings_str: str, optional
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: A new instance of ColumnValue.
        :rtype: ColumnValue
        """
        
        type_map = {
            'status': StatusValue,
            'numbers': NumbersValue,
            'board_relation': BoardRelationValue,
            'file': FileValue,
        }

        return ModelObject.new(
            type_map.get(type, ColumnValue),
            id=id,
            name=name,
            type=type,
            value=value,
            description=description,
            settings_str=settings_str,
            **kwargs
        )

# ** model: status_value
class StatusValue(ColumnValue):
    """
    Represents a status column value in a Monday.com item.
    """

    # * attribute: index
    index = IntegerType(
        metadata=dict(
            description='The index of the status (for Status columns).'
        )
    )

    # * attribute: text
    text = StringType(
        metadata=dict(
            description='The text representation of the status (for Status columns).'
        )
    )

# ** model: numbers_value
class NumbersValue(ColumnValue):
    """
    Represents a number column value in a Monday.com item.
    """

    # * attribute: number
    number = IntegerType(
        metadata=dict(
            description='The numeric representation of the column value.'
        )
    )

# ** model: board_relation_value
class BoardRelationValue(ColumnValue):
    """
    Represents a board relation column value in a Monday.com item.
    """

    # * attribute: linked_item_ids
    linked_item_ids = ListType(
        IntegerType,
        default=[],
        metadata=dict(
            description='A list of item IDs linked in the board relation column.'
        )
    )

# ** model: file_value
class FileValue(ColumnValue):
    """
    Represents a file column value in a Monday.com item.
    """

    # * attribute: files
    files = ListType(
        DictType(StringType),
        default=[],
        metadata=dict(
            description='A list of files associated with the file column.'
        )
    )

    # * method: get_object_ids
    def get_object_ids(self) -> list[str]:
        """
        Extracts and returns a list of object IDs from the files.

        :return: A list of object IDs.
        :rtype: list[str]
        """
        object_ids = []
        for file in self.files:
            if 'object_id' in file:
                object_ids.append(file['object_id'])
        return object_ids