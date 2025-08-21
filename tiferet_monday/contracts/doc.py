# *** imports

# ** core
from typing import List

# ** infra
from tiferet.contracts import *

# *** contracts

# ** contract: document_block
class DocumentBlockContract(ModelContract):
    """
    Represents a block of content within a document.
    """

    # * attribute: id
    id: str

    # * attribute: type
    type: str

    # * attribute: content
    content: str

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

    # * attribute: blocks
    blocks: List[DocumentBlockContract]

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
    
    # * method: update_doc_name
    @abstractmethod
    def update_doc_name(self, doc_id: str | int, name: str):
        """
        Updates the name of a specified monday.com document.

        :param doc_id: ID of the document to rename.
        :type doc_id: str | int
        :param name: New name for the document.
        :type name: str
        """
        raise NotImplementedError('update_doc_name method must be implemented in the board_repo.')