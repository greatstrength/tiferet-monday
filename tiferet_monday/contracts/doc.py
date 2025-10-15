# *** imports

# ** core
from abc import abstractmethod
from typing import List

# ** infra
from tiferet.contracts import (
    ModelContract,
    Repository
)

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
    
    # * method: query_by_object_ids
    @abstractmethod
    def query_by_object_ids(self, object_ids: List[str]) -> List[DocumentContract]:
        """
        Queries documents by their object IDs.

        :param object_ids: List of object IDs of the documents to retrieve.
        :type object_ids: List[str]
        :return: List of documents matching the specified object IDs.
        :rtype: List[DocumentContract]
        """
        raise NotImplementedError('query_by_object_ids method must be implemented in the board_repo.')
    
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
    
    # * method: query_doc_blocks
    @abstractmethod
    def query_doc_blocks(self, doc_id: str | int, limit: int = 25, page: int = 1) -> List[DocumentBlockContract]:
        """
        Reads the blocks of a specified document.

        :param doc_id: ID of the document to read blocks from.
        :type doc_id: str | int
        :param limit: Maximum number of blocks to read (default is 25).
        :type limit: int
        :param page: Page number for pagination (default is 1).
        :type page: int
        :return: List of blocks in the document.
        :rtype: List[DocumentBlockContract]
        """
        raise NotImplementedError('query_doc_blocks method must be implemented in the board_repo.')
    
    # * method: create_doc_block
    @abstractmethod
    def create_doc_block(self, doc_id: str | int, type: str, content: str, after_block_id: str = None) -> DocumentBlockContract:
        """
        Creates a new block in the specified document.

        :param doc_id: ID of the document where the block will be created.
        :type doc_id: str | int
        :param type: Type of the block to be created.
        :type type: str
        :param content: Content of the block.
        :type content: str
        :param after_block_id: ID of the block after which the new block will be inserted (optional).
        :type after_block_id: str
        :return: The created document block.
        :rtype: DocumentBlockContract
        """
        raise NotImplementedError('create_doc_block method must be implemented in the board_repo.')