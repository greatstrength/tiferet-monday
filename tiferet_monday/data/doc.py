# *** imports

# ** infra
from tiferet.data import *

# ** app
from ..models.doc import *
from ..contracts.doc import (
    DocumentContract
)

# *** data

# ** data: document_data
class DocumentData(DataObject, Document):
    """
    Represents a document in the Tiferet Monday application.
    """

    class Options():
        """
        Options for the DocumentData class.
        """
        serialize_when_none = False
        roles = dict(
            to_model=DataObject.allow(),
            to_data=DataObject.allow()
        )