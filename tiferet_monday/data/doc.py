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

    # * method: map
    def map(self) -> DocumentContract:
        """
        Maps the DocumentData instance to a DocumentContract.

        :return: The mapped DocumentContract instance.
        :rtype: DocumentContract
        """
        
        return super().map(Document)