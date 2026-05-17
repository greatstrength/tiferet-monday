"""Tiferet Monday Tag Events"""

# *** imports

# ** core
from typing import List

# ** app
from .settings import MondayEvent
from ..interfaces.tag import TagService
from ..domain.tag import Tag


# *** events

# ** event: get_tags
class GetTags(MondayEvent):
    '''
    Event to retrieve tags from Monday.com.
    '''

    # * attribute: tag_service
    tag_service: TagService

    # * init
    def __init__(self, tag_service: TagService):
        self.tag_service = tag_service

    # * method: execute
    def execute(self, ids: List[str] = None, **kwargs) -> List[Tag]:
        '''
        Retrieve tags.

        :param ids: Optional list of tag IDs.
        :type ids: List[str]
        :return: List of Tag domain objects.
        :rtype: List[Tag]
        '''

        # Query tags from the service.
        data = self.tag_service.get_tags(ids=ids)

        # Return tag domain objects.
        return [Tag.model_validate(t) for t in data]


# ** event: create_or_get_tag
class CreateOrGetTag(MondayEvent):
    '''
    Event to create or get an existing tag.
    '''

    # * attribute: tag_service
    tag_service: TagService

    # * init
    def __init__(self, tag_service: TagService):
        self.tag_service = tag_service

    # * method: execute
    def execute(self, tag_name: str, board_id: str = None, **kwargs) -> Tag:
        '''
        Create or get a tag.

        :param tag_name: The tag name.
        :type tag_name: str
        :param board_id: Optional board ID.
        :type board_id: str
        :return: The Tag domain object.
        :rtype: Tag
        '''

        # Create or get the tag via the service.
        data = self.tag_service.create_or_get_tag(tag_name=tag_name, board_id=board_id)

        # Return the tag domain object.
        return Tag.model_validate(data)
