"""Tiferet Monday Tag Interfaces"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List

# ** app
from .settings import MondayService


# *** interfaces

# ** interface: tag_service
class TagService(MondayService):
    '''
    Service interface for tag-related Monday.com API operations.
    '''

    # * method: get_tags
    @abstractmethod
    def get_tags(self, ids: List[str] = None) -> List[dict]:
        '''
        Query tags, optionally filtered by IDs.

        :param ids: Optional list of tag IDs.
        :type ids: List[str]
        :return: List of tag data dicts.
        :rtype: List[dict]
        '''
        raise NotImplementedError()

    # * method: create_or_get_tag
    @abstractmethod
    def create_or_get_tag(self, tag_name: str, board_id: str = None) -> dict:
        '''
        Create a tag or get it if it already exists.

        :param tag_name: The tag name.
        :type tag_name: str
        :param board_id: Optional board ID to scope the tag.
        :type board_id: str
        :return: The tag data.
        :rtype: dict
        '''
        raise NotImplementedError()
