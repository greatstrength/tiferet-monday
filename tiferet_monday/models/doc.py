# *** imports

# ** infra
from tiferet.models import *

# *** models

# ** model: document
class Document(Entity):
    """
    Represents a document in the system.
    """

    # * attribute: id
    id = StringType(
        required=True,
        metadata=dict(
            description='The unique identifier of the document.'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The name of the document.'
        )
    )

    # * attribute: object_id
    object_id = StringType(
        required=True,
        metadata=dict(
            description='The identifier of the object associated with the document.'
        )
    )