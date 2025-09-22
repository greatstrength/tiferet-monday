from monday_app import app
import os
from typing import Callable

from tiferet_monday.models.item import ItemDetail, StatusValue

from git import (
    pull_latest_from_base_branch,
    create_and_push_branch,
    checkout_branch,
    delete_local_branch
)
from task import (
    task_id_input,
    retrieve_task_details,
    get_task_status,
    get_branch_name,
    update_subtask_status_to_done
)

ROOT_PATH = os.getcwd()

GITHUB_BASE_BRANCH = 'main'

def create_dev_branch(task: ItemDetail, back: Callable = lambda d: d):
    '''
    Create and push a new development branch for a subtask if the task is ready to start.
    '''

    # Navigate to the project root and pull the latest code.
    print('Setting up git branch...')
    project_root = os.getenv('TIFERET_APP_PROJECT_ROOT')
    os.chdir(project_root)

    # Pull the latest from the base branch.
    pull_latest_from_base_branch()

    # Generate the git branch name.
    git_branch = get_branch_name(task)

    # Create and push the new branch.
    create_and_push_branch(git_branch)

    # Now return to the original path.
    os.chdir(ROOT_PATH)

    print('Task is in progress. Please proceed to committing subtask content...')

    back()
    
def remove_dev_branch(task: ItemDetail):
    '''
    Delete a local development branch and switch back to the main branch if the task is done.
    '''

    # Update the status to done.
    task_status = get_task_status(task)
    if task_status.text != 'Done':
        update_subtask_status_to_done(task, task_status)

    # Get the task status.
    git_branch = get_branch_name(task)

    print(f'Deleting local branch {git_branch} and switching back to {GITHUB_BASE_BRANCH}...')
    project_root = os.getenv('TIFERET_APP_PROJECT_ROOT')
    os.chdir(project_root)

    # Pull the latest from the base branch.
    pull_latest_from_base_branch()

    # Checkout the base branch and delete the specified local branch.
    delete_local_branch(git_branch)

    # Return to the original path.
    os.chdir(ROOT_PATH)

    print('Local branch deleted and switched back to main branch.')

def select_subtasks(task: ItemDetail, back: Callable = lambda d: d):
    '''
    List all subtasks of a given task.
    '''
    subtasks = app.run('item.query_subitems', data=dict(
        parent_item_id=task.id
    ))
    
    print('Select a subtask to work on:')
    for index, subtask in enumerate(subtasks, start=1):
        print(f"{index}. {subtask['name']} (ID: {subtask['id']})")
    print('Enter the number of the subtask (or press Enter to exit): ')
    
    return subtasks

def sprint_task_management_menu(task: ItemDetail, back: Callable = lambda d: d):
    '''
    Display a menu for managing sprint tasks.
    '''

    def create_menu_option():
        if task_status.text == 'Ready to start':
            return 'Start working on this task (create and push a new dev branch)'
        elif task_status.text == 'In Progress':
            return 'Continue working on this task (checkout existing dev branch)'
        elif task_status.text == 'Pending Deployment':
            return 'Finish working on this task (delete local dev branch and switch back to main)'
        else:
            return None
        
    def execute_task_option():
        if task_status.text == 'Ready to start':
            create_dev_branch(task, back=sprint_task_management_menu)
        elif task_status.text == 'Pending Deployment':
            remove_dev_branch(task, back=sprint_task_management_menu)
        
    task_status = get_task_status(task)
    print(f'Current task: {task.name} (Status: {task_status.text})')
    
    print(f'1. {create_menu_option()}')
    print('2. Back to main menu')
    option = input('Enter 1 or 2 (or press Enter to exit): ')
    if option == '':
        print('Exiting...')
        exit(0)
    elif option == '2':
        back()
    elif option == '1' and create_menu_option() is not None:
        execute_task_option()
    else:
        print('Invalid option. Exiting...')
        exit(0)


def main():

    task_id = task_id_input()

    task = retrieve_task_details(task_id)

    sprint_task_management_menu(task, back=main)
    
if __name__ == '__main__':
    main()