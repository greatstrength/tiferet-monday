"""Tiferet Monday Workspace Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List, Optional

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: workspace_service
class WorkspaceService(MondayService):
    '''
    Service interface for workspace-related Monday.com API operations.
    '''

    # * method: get_workspaces
    @abstractmethod
    def get_workspaces(self, ids: List[str] = None, kind: str = None, limit: int = 25, page: int = 1) -> List[dict]:
        '''
        Query workspaces, optionally filtered by IDs or kind.

        :param ids: Optional list of workspace IDs.
        :type ids: List[str]
        :param kind: Optional workspace kind filter (open / closed).
        :type kind: str
        :param limit: Number of workspaces to retrieve.
        :type limit: int
        :param page: Page number.
        :type page: int
        :return: List of workspace data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_workspace
    @abstractmethod
    def create_workspace(self, name: str, kind: str = 'open', description: str = None) -> dict:
        '''
        Create a new workspace.

        :param name: The workspace name.
        :type name: str
        :param kind: The workspace kind (open / closed).
        :type kind: str
        :param description: Optional workspace description.
        :type description: str
        :return: The created workspace data.
        :rtype: dict
        '''
        raise NotImplementedError()

    # * method: delete_workspace
    @abstractmethod
    def delete_workspace(self, workspace_id: str) -> dict:
        '''
        Delete a workspace.

        :param workspace_id: The workspace ID.
        :type workspace_id: str
        :return: The deleted workspace data.
        :rtype: dict
        '''
        raise NotImplementedError()
