"""Tiferet Monday Workspace Repos"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayApiProxy
from ..interfaces.workspace import WorkspaceService


# *** repos

# ** repo: workspace_api_proxy
class WorkspaceApiProxy(WorkspaceService, MondayApiProxy):
    '''
    Concrete WorkspaceService implementation using the Monday.com GraphQL API.
    '''

    # * init
    def __init__(self, monday_api_key: str):
        MondayApiProxy.__init__(self, monday_api_key)

    # * method: get_workspaces
    def get_workspaces(self, ids: List[str] = None, kind: str = None, limit: int = 25, page: int = 1) -> List[dict]:
        '''
        Query workspaces from the Monday.com API.
        '''

        # Build variables and dynamic params.
        variables = {'limit': limit, 'page': page}
        params = ['$limit: Int!', '$page: Int!']
        args = ['limit: $limit', 'page: $page']

        if ids:
            variables['ids'] = [int(i) for i in ids]
            params.append('$ids: [ID!]')
            args.append('ids: $ids')

        if kind:
            variables['kind'] = kind
            params.append('$kind: WorkspaceKind')
            args.append('kind: $kind')

        params_str = ', '.join(params)
        args_str = ', '.join(args)

        return self.execute_query(
            query=f"""
                query ({params_str}) {{
                    workspaces ({args_str}) {{
                        id
                        name
                        kind
                        description
                        state
                        created_at
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('workspaces', []),
        )

    # * method: create_workspace
    def create_workspace(self, name: str, kind: str = 'open', description: str = None) -> dict:
        '''
        Create a new workspace.
        '''

        variables = {'name': name, 'kind': kind}
        desc_param = ''
        desc_arg = ''
        if description:
            variables['description'] = description
            desc_param = ', $description: String'
            desc_arg = ', description: $description'

        return self.execute_query(
            query=f"""
                mutation ($name: String!, $kind: WorkspaceKind!{desc_param}) {{
                    create_workspace (name: $name, kind: $kind{desc_arg}) {{
                        id
                        name
                        kind
                        description
                    }}
                }}
            """,
            variables=variables,
            start_node=lambda data: data.get('create_workspace', {}),
        )

    # * method: delete_workspace
    def delete_workspace(self, workspace_id: str) -> dict:
        '''
        Delete a workspace.
        '''

        return self.execute_query(
            query="""
                mutation ($workspaceId: ID!) {
                    delete_workspace (workspace_id: $workspaceId) { id }
                }
            """,
            variables={'workspaceId': int(workspace_id)},
            start_node=lambda data: data.get('delete_workspace', {}),
        )
