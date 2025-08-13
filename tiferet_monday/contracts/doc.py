# *** imports

# ** infra
from tiferet.contracts import *

# *** contracts

# ** contract: document
class DocumentContract(ModelContract):
    """
    Represents a document in the Tiferet Monday application.
    """

    # * attribute: id
    id: str

    # * attribute: name
    name: str

    # * attribute: object_id
    object_id: str

# ** contract: document_repo
class DocumentRepository(Repository):
    """
    Repository for managing document-related operations.
    """

    # * method: create_doc_in_column
    @abstractmethod
    def create_doc_in_column(self, item_id: str | int, column_id: str) -> DocumentContract:
        """
        Creates a document in the specified column of an item.

        :param item_id: ID of the item where the document will be created.
        :type item_id: str | int
        :param column_id: ID of the column where the document will be created.
        :type column_id: str
        :return: The created document.
        :rtype: DocumentContract
        """
        raise NotImplementedError('create_doc_in_column method must be implemented in the board_repo.')