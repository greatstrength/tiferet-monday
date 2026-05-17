"""Tiferet Monday Tag Repos"""

# *** imports

# ** core
from typing import List

# ** app
from .settings import MondayApiProxy
from ..interfaces.tag import TagService


# *** repos

# ** repo: tag_api_proxy
class TagApiProxy(TagService, MondayApiProxy):
    '''
    Concrete TagService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: get_tags
    def get_tags(self, ids: List[str] = None) -> List[dict]:
        '''
        Query tags from the Monday.com API.
        '''

        variables = {}
        id_param = ''
        id_arg = ''
        if ids:
            variables['ids'] = [int(i) for i in ids]
            id_param = '$ids: [ID!]'
            id_arg = 'ids: $ids'

        param_block = f'({id_param})' if id_param else ''
        arg_block = f'({id_arg})' if id_arg else ''

        return self.execute_query(
            query=f"""
                query {param_block} {{
                    tags {arg_block} {{
                        id
                        name
                        color
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('tags', []),
        )

    # * method: create_or_get_tag
    def create_or_get_tag(self, tag_name: str, board_id: str = None) -> dict:
        '''
        Create a tag or get it if it already exists.
        '''

        variables = {'tagName': tag_name}
        params = '$tagName: String!'
        args = 'tag_name: $tagName'
        if board_id:
            variables['boardId'] = int(board_id)
            params += ', $boardId: ID'
            args += ', board_id: $boardId'

        return self.execute_query(
            query=f"""
                mutation ({params}) {{
                    create_or_get_tag ({args}) {{
                        id
                        name
                        color
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('create_or_get_tag', {}),
        )
