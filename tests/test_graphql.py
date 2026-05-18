"""Tiferet Monday GraphQL Builder Tests"""

# *** imports

# ** infra
import pytest

# ** app
from tiferet_monday.utils.graphql import (
    GraphQLField,
    GraphQLOperation,
    InlineFragment,
    OperationType,
    StringValue,
    IntValue,
    BoolValue,
    EnumValue,
    ListValue,
    JsonValue,
    ArgumentValue,
)


# *** tests: argument values

# ** test: string_value_format
def test_string_value_format():
    assert StringValue('hello').format() == '"hello"'


# ** test: int_value_format
def test_int_value_format():
    assert IntValue('42').format() == '42'
    assert IntValue(42).format() == '42'


# ** test: bool_value_format
def test_bool_value_format():
    assert BoolValue(True).format() == 'true'
    assert BoolValue(False).format() == 'false'


# ** test: enum_value_format
def test_enum_value_format():
    assert EnumValue('public').format() == 'public'
    assert EnumValue(OperationType.QUERY).format() == 'QUERY'


# ** test: list_value_format
def test_list_value_format():
    assert ListValue([1, 2, 3]).format() == '[1, 2, 3]'
    assert ListValue(['a', 'b']).format() == '["a", "b"]'
    assert ListValue([IntValue(1), StringValue('x')]).format() == '[1, "x"]'


# ** test: json_value_format
def test_json_value_format():
    result = JsonValue({'key': 'val'}).format()
    # JsonValue double-encodes: json.dumps(json.dumps(value))
    # Result is a quoted JSON string with escaped inner quotes.
    assert 'key' in result
    assert 'val' in result
    assert result.startswith('"')


# *** tests: graphql_field

# ** test: simple_field
def test_simple_field():
    f = GraphQLField('id')
    assert f.format_body() == 'id'


# ** test: field_with_children
def test_field_with_children():
    f = GraphQLField('boards', 'id', 'name')
    body = f.format_body()
    assert 'boards' in body
    assert 'id' in body
    assert 'name' in body


# ** test: field_with_arguments
def test_field_with_arguments():
    f = GraphQLField('boards', 'id', 'name', limit=IntValue(25))
    body = f.format_body()
    assert 'limit:25' in body


# ** test: field_dot_notation_nesting
def test_field_dot_notation():
    f = GraphQLField('items', 'id', 'board.id')
    body = f.format_body()
    assert 'board { id }' in body


# *** tests: graphql_operation

# ** test: query_operation
def test_query_operation():
    op = GraphQLOperation(OperationType.QUERY, 'boards', 'id', 'name')
    body = op.format_body()
    assert body.startswith('query')
    assert 'boards' in body


# ** test: mutation_operation
def test_mutation_operation():
    op = GraphQLOperation(OperationType.MUTATION, 'create_board', 'id')
    op.add_query_variable('name', 'String!')
    op.add_arguments(name=StringValue('New Board'))
    body = op.format_body()
    assert body.startswith('mutation')
    assert '$name: String!' in body


# ** test: operation_with_variables
def test_operation_with_variables():
    op = GraphQLOperation(OperationType.QUERY, 'boards', 'id', 'name')
    op.add_query_variable('limit', 'Int!')
    op.add_query_variable('ids', '[ID!]')
    op.add_arguments(limit=IntValue(25), ids=ListValue([1, 2]))
    body = op.format_body()
    assert '$limit: Int!' in body
    assert '$ids: [ID!]' in body


# *** tests: inline_fragment

# ** test: inline_fragment
def test_inline_fragment():
    frag = InlineFragment('StatusValue', 'index', 'text')
    assert frag.format_body() == '... on StatusValue { index text }'


# ** test: inline_fragment_single_field
def test_inline_fragment_single():
    frag = InlineFragment('CheckboxValue', 'checked')
    assert frag.format_body() == '... on CheckboxValue { checked }'
