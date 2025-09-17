from monday_app import app
import os, subprocess
from functools import wraps

from tiferet_monday.models.item import ItemDetail, StatusValue

ROOT_PATH = os.getcwd()

GITHUB_BASE_BRANCH = 'main'

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

def get_task_status(task: ItemDetail) -> str:
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

def pull_latest_from_base_branch():
    '''
    Pull the latest code from the base branch.
    '''

    # Navigate to the project root and pull the latest code.
    print(f'Checking out and pulling latest from {GITHUB_BASE_BRANCH}...')
    subprocess.run(['git', 'checkout', GITHUB_BASE_BRANCH])
    subprocess.run(['git', 'pull'])

def create_and_push_branch(git_branch: str):
    '''
    Create a new git branch and push it to the remote repository.
    :param git_branch: The name of the git branch to create.
    '''

    # Create, checkout, and push the new branch to set status to work in progress
    print(f'Creating and pushing new branch {git_branch}...')
    subprocess.run(['git', 'checkout', '-b', git_branch])
    subprocess.run(['git', 'push', '--set-upstream', 'origin', git_branch])

def delete_local_branch(git_branch: str):
    '''
    Delete a local git branch.
    :param git_branch: The name of the git branch to delete.
    '''

    # Delete the specified local branch.
    print(f'Deleting local branch {git_branch}...')
    subprocess.run(['git', 'branch', '-D', git_branch])

def update_subtask_status_to_done(subtask: ItemDetail, subtask_status: StatusValue):
    
    # Update the status to Done.
    print('Updating subtask status to Done...')
    app.run('item.update_simple_column_value', data=dict(
        item_id=subtask.id,
        column_id=subtask_status.id,
        value='Done')
    )

def create_dev_branch():
    '''
    Create and push a new development branch for a subtask if the task is ready to start.
    '''
    
    task_id = input('Enter the sprint task ID to start working on (or press Enter to exit): ')
    if task_id == '':
        print('Exiting...')
        exit(0)

    print('Starting sprint task...')

    # Retrieve the task details.
    task = retrieve_task_details(task_id)

    # Get the task status.
    task_status = get_task_status(task)

    if task_status.text == 'Ready to start':

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
    
def remove_dev_branch():
    '''
    Delete a local development branch and switch back to the main branch if the task is done.
    '''

    task_id = input('Enter the sprint task ID to finish working on (or press Enter to exit): ')
    if task_id == '':
        print('Exiting...')
        exit(0)

    # Retrieve the task details.
    task = retrieve_task_details(task_id)

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

def dev_branch_management_menu(root_project_path: str = None):
    '''
    Display a menu for managing development branches.
    '''

    print('Select an option:')
    print('1. Create and push a new dev branch for a subtask (if the task is ready to start)')
    print('2. Delete a local dev branch and switch back to the main branch (if the task is done)')
    option = input('Enter 1 or 2 (or press Enter to exit): ')
    if option == '':
        print('Exiting...')
        exit(0)
    elif option == '1':
        create_dev_branch()
    elif option == '2':
        remove_dev_branch()

        
    else:
        print('Invalid option. Exiting...')
        exit(0)
def main():

    dev_branch_management_menu()
    

if __name__ == '__main__':
    main()