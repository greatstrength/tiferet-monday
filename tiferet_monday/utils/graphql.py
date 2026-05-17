"""Tiferet Monday GraphQL Utilities"""

# *** imports

# ** core
import json
from enum import Enum
from typing import Any, Dict, List, Optional


# *** constants

# ** constant: operation_type
class OperationType(Enum):
    '''GraphQL query operation type.'''
    QUERY = 'query'
    MUTATION = 'mutation'


# *** utils

# ** util: argument_value
class ArgumentValue:
    '''Base GraphQL argument value.'''

    # * init
    def __init__(self, value: Any):
        '''
        Initialize the argument value.

        :param value: The raw value.
        :type value: Any
        '''

        # Set the value.
        self.value = value

    # * method: format
    def format(self) -> str:
        '''
        Format the value for use in a GraphQL query string.

        :return: The formatted value string.
        :rtype: str
        '''

        # Return the value as-is.
        return str(self.value)


# ** util: string_value
class StringValue(ArgumentValue):
    '''GraphQL string argument value.'''

    # * method: format
    def format(self) -> str:
        '''
        Format as a quoted string.

        :return: The quoted string value.
        :rtype: str
        '''

        # Return the value wrapped in quotes.
        return '"{}"'.format(self.value)


# ** util: int_value
class IntValue(ArgumentValue):
    '''GraphQL integer argument value.'''

    # * init
    def __init__(self, value: Any):
        '''
        Initialize the integer argument value.

        :param value: The value to convert to integer.
        :type value: Any
        '''

        # Convert and set the integer value.
        super().__init__(int(value))


# ** util: bool_value
class BoolValue(ArgumentValue):
    '''GraphQL boolean argument value.'''

    # * method: format
    def format(self) -> str:
        '''
        Format as a lowercase boolean string.

        :return: The boolean string.
        :rtype: str
        '''

        # Return lowercase boolean.
        return str(self.value).lower()


# ** util: enum_value
class EnumValue(ArgumentValue):
    '''GraphQL enum argument value.'''

    # * method: format
    def format(self) -> str:
        '''
        Format as an unquoted enum name.

        :return: The enum name.
        :rtype: str
        '''

        # Return the enum name if it's an Enum, otherwise the raw value.
        if isinstance(self.value, Enum):
            return self.value.name
        return str(self.value)


# ** util: list_value
class ListValue(ArgumentValue):
    '''GraphQL list argument value.'''

    # * method: format
    def format(self) -> str:
        '''
        Format as a GraphQL list.

        :return: The formatted list string.
        :rtype: str
        '''

        # Format each item in the list.
        items = []
        for item in self.value:
            if isinstance(item, str):
                items.append('"{}"'.format(item))
            elif isinstance(item, ArgumentValue):
                items.append(item.format())
            else:
                items.append(str(item))

        # Return formatted list.
        return '[{}]'.format(', '.join(items))


# ** util: json_value
class JsonValue(ArgumentValue):
    '''GraphQL JSON argument value.'''

    # * method: format
    def format(self) -> str:
        '''
        Format as a double-encoded JSON string.

        :return: The JSON string.
        :rtype: str
        '''

        # Double-encode the JSON value.
        return json.dumps(json.dumps(self.value))


# ** util: graphql_field
class GraphQLField:
    '''
    A composable GraphQL field node with optional arguments and child fields.
    '''

    # * init
    def __init__(self, name: str, *fields: str, **kwargs: ArgumentValue):
        '''
        Initialize a GraphQL field.

        :param name: The field name.
        :type name: str
        :param fields: Child field names or GraphQLField instances.
        :type fields: str
        :param kwargs: Argument name-value pairs.
        :type kwargs: ArgumentValue
        '''

        # Set the field name.
        self.name = name

        # Initialize children and arguments.
        self._children: Dict[str, 'GraphQLField'] = {}
        self._arguments: Dict[str, ArgumentValue] = {}

        # Add child fields and arguments.
        self.add_fields(*fields)
        self.add_arguments(**kwargs)

    # * method: add_fields
    def add_fields(self, *fields) -> None:
        '''
        Add child fields to this node.

        :param fields: Child field names or GraphQLField instances.
        :type fields: str or GraphQLField
        '''

        # Iterate over each field.
        for field in fields:

            # Skip empty fields.
            if not field:
                continue

            # Handle string field names (with dot notation for nesting).
            if isinstance(field, str):
                parts = field.split('.', 1)
                parent_name = parts[0]

                # Get or create the parent field.
                existing = self._children.get(parent_name)
                if not existing:
                    existing = GraphQLField(parent_name)
                    self._children[parent_name] = existing

                # If there are remaining parts, add them as children.
                if len(parts) > 1:
                    existing.add_fields(parts[1])

            # Handle GraphQLField instances.
            elif isinstance(field, GraphQLField):
                self._children[field.name] = field

    # * method: add_arguments
    def add_arguments(self, **kwargs: ArgumentValue) -> None:
        '''
        Add arguments to this field.

        :param kwargs: Argument name-value pairs.
        :type kwargs: ArgumentValue
        '''

        # Add each argument.
        for key, value in kwargs.items():
            if isinstance(value, ArgumentValue) and value.format() is not None:
                self._arguments[key] = value

    # * method: format_body
    def format_body(self) -> str:
        '''
        Format this field into a GraphQL query string.

        :return: The formatted field string.
        :rtype: str
        '''

        # Start with the field name.
        body = self.name

        # Append arguments if present.
        if self._arguments:
            args_str = ', '.join(
                '{}:{}'.format(k, v.format())
                for k, v in self._arguments.items()
            )
            body = '{} ({})'.format(body, args_str)

        # Append children if present.
        if self._children:
            children_str = ' '.join(
                child.format_body()
                for child in self._children.values()
            )
            body = '{} {{ {} }}'.format(body, children_str)

        # Return the formatted body.
        return body


# ** util: graphql_operation
class GraphQLOperation(GraphQLField):
    '''
    A top-level GraphQL operation (query or mutation) with variable support.
    '''

    # * init
    def __init__(self,
                 operation_type: OperationType,
                 name: str,
                 *fields: str,
                 **kwargs: ArgumentValue):
        '''
        Initialize a GraphQL operation.

        :param operation_type: The operation type (query or mutation).
        :type operation_type: OperationType
        :param name: The operation name (e.g., 'boards', 'create_item').
        :type name: str
        :param fields: Return fields for the operation.
        :type fields: str
        :param kwargs: Arguments for the operation.
        :type kwargs: ArgumentValue
        '''

        # Set the operation type.
        self.operation_type = operation_type

        # Initialize query variables.
        self.query_variables: Dict[str, str] = {}

        # Initialize the parent field.
        super().__init__(name, *fields, **kwargs)

    # * method: add_query_variable
    def add_query_variable(self, key: str, graphql_type: str) -> None:
        '''
        Add a query variable declaration.

        :param key: The variable name (without $).
        :type key: str
        :param graphql_type: The GraphQL type string (e.g., 'ID!', '[String!]').
        :type graphql_type: str
        '''

        # Add the variable to the query variables.
        self.query_variables[key] = graphql_type

    # * method: format_body
    def format_body(self) -> str:
        '''
        Format the complete operation into a GraphQL query string.

        :return: The formatted operation string.
        :rtype: str
        '''

        # Format the inner field body.
        inner = super().format_body()

        # Wrap with operation type and variables.
        if self.query_variables:
            var_list = ['${}: {}'.format(k, v) for k, v in self.query_variables.items()]
            var_str = '({})'.format(', '.join(var_list))
            return '{} {} {{ {} }}'.format(self.operation_type.value, var_str, inner)

        # Return without variables.
        return '{} {{ {} }}'.format(self.operation_type.value, inner)


# ** util: inline_fragment
class InlineFragment:
    '''
    A GraphQL inline fragment (e.g., ... on StatusValue { index text }).
    '''

    # * init
    def __init__(self, type_name: str, *fields: str):
        '''
        Initialize an inline fragment.

        :param type_name: The GraphQL type name.
        :type type_name: str
        :param fields: The fields to select.
        :type fields: str
        '''

        # Set the type name and fields.
        self.type_name = type_name
        self.fields = fields

    # * method: format_body
    def format_body(self) -> str:
        '''
        Format as a GraphQL inline fragment string.

        :return: The formatted fragment.
        :rtype: str
        '''

        # Format the fields.
        fields_str = ' '.join(self.fields)

        # Return the formatted inline fragment.
        return '... on {} {{ {} }}'.format(self.type_name, fields_str)
