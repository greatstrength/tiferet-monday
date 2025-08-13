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