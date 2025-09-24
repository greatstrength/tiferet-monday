from monday_app import app
import os, json
from typing import List, Callable

from tiferet_monday.models.item import ItemDetail, Item

from git import (
    pull_latest_from_base_branch,
    create_and_push_branch,
    checkout_branch,
    stage_file,
    commit_changes,
    delete_local_branch
)
from task import (
    task_id_input,
    get_status_text,
    retrieve_task_details,
    get_branch_name,
    list_subtasks,
    begin_subtask,
    update_subtask_status_to_done
)

ROOT_PATH = os.getcwd()
PROJECT_ROOT = os.getenv('TIFERET_APP_PROJECT_ROOT')
GITHUB_BASE_BRANCH = 'main'
TASK_OWNER_ID = '39073543'


# * function: create_dev_branch
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

# * function: remove_dev_branch    
def remove_dev_branch(task: ItemDetail, back: Callable = lambda d: d):
    '''
    Delete a local development branch and switch back to the main branch if the task is done.
    '''

    # Update the status to done.
    task_status = task.get_column_value('Status')
    if task_status.text != 'Done':
        update_subtask_status_to_done(task, task_status)

    # Get the task status.
    git_branch = get_branch_name(task)

    print(f'Deleting local branch {git_branch} and switching back to {GITHUB_BASE_BRANCH}...')
    PROJECT_ROOT = os.getenv('TIFERET_APP_PROJECT_ROOT')
    os.chdir(PROJECT_ROOT)

    # Pull the latest from the base branch.
    pull_latest_from_base_branch()

    # Checkout the base branch and delete the specified local branch.
    delete_local_branch(git_branch)

    # Return to the original path.
    os.chdir(ROOT_PATH)

    print('Local branch deleted and switched back to main branch.')

    back(task)

# * function: select_subtask_from_list
def select_subtask_from_list(subtasks: List[Item], back: Callable = lambda d: d):
    '''
    Display a list of subtasks and allow the user to select one.
    '''
    
    print('Select a subtask to work on:')
    for index, subtask in enumerate(subtasks, start=1):
        print(f"{index}. {subtask.name} (ID: {subtask.id})")

    # Get user input for subtask selection.
    print('Enter the number of the subtask (or press Enter to exit): ')
    option = input('> ')
    if option == '':
        print('Exiting...')
        back()
    option = int(option)
    
    # Retieve the selected subtask.
    subtask = subtasks[option - 1]

    # Retrieve the latest details of the selected subtask.
    subtask_details = retrieve_task_details(subtask.id, is_subtask=True)

    # Ensure the selected subtask is not already committed.
    if subtask_details.get_column_value('Status').text == 'Committed':
        print('Selected subtask has already been committed. Please select another subtask.')
        return select_subtask_from_list(subtasks, back=back)
    
    print(f'You selected subtask: {subtask.name} (ID: {subtask.id})')

    return subtask_details

# * function: retrieve_subtask_code
def retrieve_subtask_code(subtask: ItemDetail):
    '''
    Retrieve the code document associated with the subtask.
    '''

    print('Retrieving code document from item...')
    code_new_after = subtask.get_column_value('Code (New/After)')
    code_new_after = app.run('item.query_column_values', data=dict(
        item_id=subtask.id,
        column_ids=[code_new_after.id]
    ))[0]

    # Query the doc content using the object ID from the code column value
    print('Read code from document...')
    object_ids = [code_new_after.get_object_id()]
    doc = app.run('doc.query_by_object_ids', data=dict(
        object_ids=object_ids
    ))[0]

    # Extract the code from the doc content.
    print('Extracting code from doc...')
    blocks = doc.get('blocks', [])
    content = blocks[0]['content'] if blocks else None
    code_blocks = json.loads(content) if content else None
    code = []
    for block in code_blocks['deltaFormat']:
        code.append(block['insert'])
    return ''.join(code).replace('\n\n\n', '\n\n').replace('\xa0', ' ')


# * function: write_code_to_file
def write_code_to_file(subtask: ItemDetail, branch: str, code):
    '''
    Write the retrieved code to the appropriate file.
    '''

    print('Retrieving linked code module...')

    # Retrieve the module column from the subtask.
    module = subtask.get_column_value('Module')

    # Retrieve the column value to get the linked item ID.
    module = app.run(
        'item.query_column_values',
        data=dict(
            item_id=subtask.id,
            column_ids=[module.id]
        )
    )[0]

    # Retrieve the linked item to get the file path.
    linked_item_id = module.linked_item_ids[0]
    linked_item: ItemDetail = app.run(
        'item.query_detail_by_id', 
        data=dict(
            item_id=linked_item_id
        )
    )

    # Change to the project root and write the code to the file.
    os.chdir(PROJECT_ROOT)
    checkout_branch(branch)
    file_path = os.path.join(PROJECT_ROOT, linked_item.name)
    print(f'Writing code to file: {file_path}...')
    with open(file_path, 'w') as f:
        f.write(code)
    stage_file(file_path)
    

# * function: commit_changes_and_close_subtask
def commit_changes_and_close_subtask(subtask: ItemDetail):
    '''
    Commit the changes to git and update the subtask status to Committed.
    '''

    commit = input("Wrote code to file. Press y to commit, any other key to exit: ")
    if commit.lower() == 'y':
        
        # Commit and push the changes and return to the original path.
        commit_changes(subtask.name)
        os.chdir(ROOT_PATH)

        subtask_status, actual_sp = subtask.get_column_values(['Status', 'Actual SP'])

        # Update the status to Committed.
        print('Updating subtask status to Committed...')
        app.run('item.update_simple_column_value', data=dict(
            item_id=subtask.id,
            column_id=subtask_status.id,
            value='Committed')
        )

        # Set the Actual SP column to 1.
        print('Setting Actual SP...')
        app.run('item.update_simple_column_value', data=dict(
            item_id=subtask.id,
            column_id=actual_sp.id,
            value='1')
        )

# * function: work_dev_branch
def work_dev_branch(task: ItemDetail, back: Callable = lambda d: d):
    '''
    Checkout and work an existing development branch for a subtask if the task is in progress.
    '''

    # List all subtasks of the task.
    subtasks = list_subtasks(task.id)
    if not subtasks:
        print('No subtasks found for this task. Please create a subtask first.')
        back()

    while True:

        # Let the user select a subtask to work on.
        subtask = select_subtask_from_list(subtasks, back=lambda: sprint_task_management_menu(task, back=back))

        # Retrieve the latest details of the selected subtask.
        subtask = retrieve_task_details(subtask.id)
        
        # Retrieve the owner and status columns of the selected subtask.
        owner, status = subtask.get_column_values(['Owner', 'Status'])

        # Begin working on the selected subtask.
        begin_subtask(
            subtask, 
            owner_column_id=owner.id, 
            owner_id=TASK_OWNER_ID, 
            status_column_id=status.id
        )

        # Retrieve the code associated with the subtask.
        code = retrieve_subtask_code(subtask)

        # Retrieve the git branch and write the code to the appropriate file.
        git_branch = get_branch_name(task)
        write_code_to_file(subtask, git_branch, code)

        # Commit the changes and close the subtask.
        commit_changes_and_close_subtask(subtask)

        print('\nSubtask work completed.')
        print('Do you want to work on another subtask? (y/n): ')
        option = input('> ')
        print('')
        if option.lower() != 'y':
            break

# * function: sprint_task_management_menu
def sprint_task_management_menu(task: ItemDetail, back: Callable = lambda d: d):
    '''
    Display a menu for managing sprint tasks.
    '''

    def create_menu_option():
        if task_status_text == 'Ready to start':
            return 'Start working on this task (create and push a new dev branch)'
        elif task_status_text == 'In Progress':
            return 'Continue working on this task (checkout existing dev branch)'
        elif task_status_text == 'Pending Deploy':
            return 'Finish working on this task (delete local dev branch and switch back to main)'
        else:
            return None
        
    def execute_task_option():
        if task_status_text == 'Ready to start':
            create_dev_branch(task, back=lambda: sprint_task_management_menu(task.id))
        elif task_status_text == 'In Progress':
            work_dev_branch(task, back=main)
        elif task_status_text == 'Pending Deploy':
            remove_dev_branch(task, back=sprint_task_management_menu)

    
    task_status_text = get_status_text(task)

    if task_status_text not in ['Ready to start', 'In Progress', 'Awaiting Review', 'Pending Deploy']:
        print(f'Task status is "{task_status_text}". No actions available. Exiting...')
        exit(0)

    
    
    print('Select an option:')
    
    print(f'\t1. {create_menu_option()}')
    print('\t2. Back to main menu')
    print('Enter 1 or 2 (or press Enter to exit): ')
    option = input('> ')
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

# * function: main
def main():

    # Get the task ID from user input and retrieve the task details.
    task_id = task_id_input()
    task = retrieve_task_details(task_id)
    print(f'Current task: {task.name} (Status: {get_status_text(task)})')

    sprint_task_management_menu(task, back=main)
    
if __name__ == '__main__':
    main()