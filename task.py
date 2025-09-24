from tiferet_monday.models import (
    ItemDetail,
    StatusValue
)
from monday_app import app
from typing import List, Callable, Any, Tuple
from tiferet import ModelObject
from tiferet_monday.models import Item

def task_id_input() -> str:
    '''
    Prompt the user for a task ID, allowing them to exit by pressing Enter.
    :param prompt: The prompt message to display.
    :return: The entered task ID, or exits if Enter is pressed.
    '''
    
    print('Enter the sprint task ID (or press Enter to exit): ')
    task_id = input('> ')
    if task_id == '':
        print('Exiting...')
        exit(0)
    print('')
    return task_id

def retrieve_task_details(task_id: str, is_subtask: bool = False) -> ItemDetail:
    '''
    Retrieve the details of a task by its ID.
    :param task_id: The ID of the task to retrieve.
    :return: An ItemDetail object containing the task details.
    '''
    print('Retrieving subtask details...') if is_subtask else print('Retrieving task details...\n')
    task = ItemDetail.new(
        **app.run('item.query_detail_by_id', data=dict(
            item_id=task_id
        ))
    )
    return task

def list_subtasks(task_id) -> list[ItemDetail]:
    '''
    List all subtasks of a given task.

    :param task_id: The ID of the parent task.
    :type task_id: str
    :return: A list of ItemDetail objects representing the subtasks.
    :rtype: list[ItemDetail]
    '''

    print('\nRetrieving subtasks...\n')
    subtasks_data = app.run('item.query_subitems', data=dict(
        parent_item_id=task_id
    ))
    return [
        ModelObject.new(
            Item,
            **s) for s in subtasks_data
    ]

def retrieve_subtask_details(subtask_id: str, column_ids: list[str]) -> Tuple[Any]:
    return app.run('item.query_column_values', data=dict(
    item_id=subtask_id,
    column_ids=column_ids
))

def get_status_text(task: ItemDetail) -> str:
    '''
    Get the status text of a task.

    :param task: The ItemDetail object representing the task.
    :type task: ItemDetail
    :return: The status text of the task.
    :rtype: str
    '''
    status_column = task.get_column_value('Status')
    if not status_column:
        raise ValueError('Status column not found in the task.')
    return status_column.text

def begin_subtask(subtask: ItemDetail, owner_column_id: str, owner_id: str, status_column_id: str):
    
    print('Assigning subtask to yourself...')
    app.run('item.update_simple_column_value', data=dict(
        item_id=subtask.id,
        column_id=owner_column_id,
        value=owner_id)
    )


    print('Updating subtask status to Working on it...') # Delete This
    app.run('item.update_simple_column_value', data=dict(
        item_id=subtask.id,
        column_id=status_column_id,
        value='Working on it')
    )

def get_branch_name(task: ItemDetail) -> str:
    '''
    Generate a git branch name based on the task name and ID.
    :param task: The ItemDetail object representing the task.
    :param task_id: The ID of the task.
    :return: A string representing the git branch name.
    '''

    # Lowercase the task name.
    git_branch = task.name.lower()

    # Remove any special characters and replace spaces with dashes.
    git_branch = ''.join(e for e in git_branch if e.isalnum() or e == ' ').replace(' ', '-')

    # Append the task ID to ensure uniqueness.
    # Return the branch name.
    git_branch += f'-{task.id}'
    return git_branch

def update_subtask_status_to_done(subtask: ItemDetail, subtask_status: StatusValue):
    
    # Update the status to Done.
    print('Updating subtask status to Done...')
    app.run('item.update_simple_column_value', data=dict(
        item_id=subtask.id,
        column_id=subtask_status.id,
        value='Done')
    )