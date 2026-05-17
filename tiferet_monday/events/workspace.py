"""Tiferet Monday Workspace Events"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from .settings import MondayEvent
from ..interfaces.workspace import WorkspaceService
from ..domain.workspace import Workspace


# *** events

# ** event: get_workspaces
class GetWorkspaces(MondayEvent):
    '''
    Event to retrieve workspaces from Monday.com.
    '''

    # * attribute: workspace_service
    workspace_service: WorkspaceService

    # * init
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    # * method: execute
    def execute(self, ids: List[str] = None, kind: str = None, limit: int = 25, **kwargs) -> List[Workspace]:
        '''
        Retrieve workspaces.

        :param ids: Optional list of workspace IDs.
        :type ids: List[str]
        :param kind: Optional workspace kind filter.
        :type kind: str
        :param limit: Number of workspaces.
        :type limit: int
        :return: List of Workspace domain objects.
        :rtype: List[Workspace]
        '''

        # Query workspaces from the service.
        data = self.workspace_service.get_workspaces(ids=ids, kind=kind, limit=limit)

        # Return workspace domain objects.
        return [Workspace.model_validate(w) for w in data]


# ** event: create_workspace
class CreateWorkspace(MondayEvent):
    '''
    Event to create a new workspace.
    '''

    # * attribute: workspace_service
    workspace_service: WorkspaceService

    # * init
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    # * method: execute
    def execute(self, name: str, kind: str = 'open', description: str = None, **kwargs) -> Workspace:
        '''
        Create a new workspace.

        :param name: The workspace name.
        :type name: str
        :param kind: The workspace kind.
        :type kind: str
        :param description: Optional description.
        :type description: str
        :return: The created Workspace domain object.
        :rtype: Workspace
        '''

        # Create the workspace via the service.
        data = self.workspace_service.create_workspace(name=name, kind=kind, description=description)

        # Return the workspace domain object.
        return Workspace.model_validate(data)


# ** event: delete_workspace
class DeleteWorkspace(MondayEvent):
    '''
    Event to delete a workspace.
    '''

    # * attribute: workspace_service
    workspace_service: WorkspaceService

    # * init
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    # * method: execute
    def execute(self, workspace_id: str, **kwargs) -> dict:
        '''
        Delete a workspace.

        :param workspace_id: The workspace ID.
        :type workspace_id: str
        :return: The deleted workspace data.
        :rtype: dict
        '''

        # Delete the workspace via the service.
        return self.workspace_service.delete_workspace(workspace_id=workspace_id)
