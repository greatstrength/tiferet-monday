# *** imports

# ** infra
from tiferet.commands import Command

# ** app
from ..models.doc import *
from ..contracts.doc import *

# *** commands

# ** command: create_doc_in_column
class CreateDocInColumn(Command):
    """
    Command to create a document in a specified column.
    """

    # * attribute: document_repo
    document_repo: DocumentRepository

    # * init
    def __init__(self, document_repo: DocumentRepository):
        """
        Initializes the CreateDocInColumn command with the document repository.

        :param document_repo: The repository for managing document operations.
        :type document_repo: DocumentRepository
        """

        # Assign the document repository to the command instance.
        self.document_repo = document_repo

    # * method: execute
    def execute(self, item_id: str | int, column_id: str, **kwargs) -> Document:
        """
        Executes the command to create a document in the specified column.

        :param item_id: ID of the item where the document will be created.
        :type item_id: str | int
        :param column_id: ID of the column where the document will be created.
        :type column_id: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The created document.
        :rtype: DocumentContract
        """
        
        # Call the repository method to create a document in the specified column.
        return self.document_repo.create_doc_in_column(item_id=item_id, column_id=column_id)
    
# ** command: update_doc_name
class UpdateDocName(Command):
    """
    Command to update the name of a specified document.
    """

    # * attribute: document_repo
    document_repo: DocumentRepository

    # * init
    def __init__(self, document_repo: DocumentRepository):
        """
        Initializes the UpdateDocName command with the document repository.

        :param document_repo: The repository for managing document operations.
        :type document_repo: DocumentRepository
        """

        # Assign the document repository to the command instance.
        self.document_repo = document_repo

    # * method: execute
    def execute(self, doc_id: str | int, name: str, **kwargs):
        """
        Executes the command to update the name of a specified document.

        :param doc_id: ID of the document to rename.
        :type doc_id: str | int
        :param name: New name for the document.
        :type name: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        
        # Call the repository method to update the document name.
        self.document_repo.update_doc_name(doc_id=doc_id, name=name)

# ** command: query_doc_blocks
class QueryDocBlocks(Command):
    """
    Command to read the blocks of a specified document.
    """

    # * attribute: document_repo
    document_repo: DocumentRepository

    # * init
    def __init__(self, document_repo: DocumentRepository):
        """
        Initializes the QueryDocBlocks command with the document repository.

        :param document_repo: The repository for managing document operations.
        :type document_repo: DocumentRepository
        """
        
        # Assign the document repository to the command instance.
        self.document_repo = document_repo

    # * method: execute
    def execute(self, doc_id: str | int, limit: int = 25, page: int = 1, **kwargs) -> List[DocumentBlock]:
        """
        Executes the command to read blocks from a specified document.

        :param doc_id: ID of the document to read blocks from.
        :type doc_id: str | int
        :param limit: Maximum number of blocks to read (default is 25).
        :type limit: int
        :param page: Page number for pagination (default is 1).
        :type page: int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: List of blocks in the document.
        :rtype: List[DocumentBlockContract]
        """
        
        # Call the repository method to read the document blocks.
        return self.document_repo.query_doc_blocks(
            doc_id=doc_id,
            limit=limit,
            page=page
        )
    
# ** command: create_doc_block
class CreateDocBlock(Command):
    """
    Command to create a block in a specified document.
    """

    # * attribute: document_repo
    document_repo: DocumentRepository

    # * init
    def __init__(self, document_repo: DocumentRepository):
        """
        Initializes the CreateDocBlock command with the document repository.

        :param document_repo: The repository for managing document operations.
        :type document_repo: DocumentRepository
        """
        
        # Assign the document repository to the command instance.
        self.document_repo = document_repo

    # * method: execute
    def execute(self, doc_id: str | int, type: str, content: dict, after_block_id: str = None, **kwargs) -> str:
        """
        Executes the command to create a block in the specified document.

        :param doc_id: ID of the document where the block will be created.
        :type doc_id: str | int
        :param type: Type of the block to be created.
        :type type: str
        :param content: Content of the block.
        :type content: dict
        :param after_block_id: ID of the block after which the new block will be inserted
        :type after_block_id: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The id of the created document block.
        :rtype: str
        """
        
        # Call the repository method to create a block in the specified document.
        return self.document_repo.create_doc_block(
            doc_id=doc_id, 
            type=type, 
            content=content, 
            after_block_id=after_block_id)