from tiferet_monday.models import (
    ItemDetail,
    StatusValue
)
from monday_app import app

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
    return task_id

def retrieve_task_details(task_id: str) -> ItemDetail:
    '''
    Retrieve the details of a task by its ID.
    :param task_id: The ID of the task to retrieve.
    :return: An ItemDetail object containing the task details.
    '''
    print('Retrieving task details...')
    task = ItemDetail.new(
        **app.run('item.query_detail_by_id', data=dict(
            item_id=task_id
        ))
    )
    return task

def list_subtasks(task: ItemDetail) -> list[ItemDetail]:
    '''
    List all subtasks of a given task.
    :param task: The ItemDetail object representing the task.
    :return: A list of ItemDetail objects representing the subtasks.
    '''
    print('Listing subtasks...')
    subtasks_data = app.run('item.query_subitems', data=dict(
        parent_item_id=task.id
    ))
    return [
        ItemDetail.new(**s) for s in subtasks_data
    ]

def get_task_status(task: ItemDetail) -> StatusValue:
    '''
    Get the status of a task.
    :param task: The ItemDetail object representing the task.
    :return: The status text of the task.
    '''

    # 
    print('Retrieving task status...')
    task_status = task.get_column_value('Status')
    task_status = app.run('item.query_column_values', data=dict(
        item_id=task.id,
        column_ids=[task_status.id]
    ))[0]
    return task_status

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