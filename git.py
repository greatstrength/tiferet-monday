import subprocess


def pull_latest_from_base_branch(base_branch: str):
    '''
    Pull the latest code from the base branch.
    '''

    # Navigate to the project root and pull the latest code.
    print(f'Checking out and pulling latest from {base_branch}...')
    subprocess.run(['git', 'checkout', base_branch])
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

def checkout_branch(github_branch: str):
    '''
    Checkout a specified git branch.
    :param github_branch: The name of the git branch to checkout.
    '''

    print(f'Checking out branch {github_branch}...')
    subprocess.run(['git', 'checkout', github_branch])

def stage_file(file_path: str):
    '''
    Stage a file for commit.
    :param file_path: The path to the file to stage.
    '''

    print(f'Staging file {file_path}...')
    subprocess.run(['git', 'add', file_path])

def commit_changes(commit_message: str):
    '''
    Commit staged changes with a commit message.
    :param commit_message: The commit message to use.
    '''

    print(f'Committing changes with message: {commit_message}')
    subprocess.run(['git', 'commit', '-m', commit_message])
    # Push the committed changes to the remote repository.
    subprocess.run(['git', 'push'])


def delete_local_branch(git_branch: str):
    '''
    Delete a local git branch.
    :param git_branch: The name of the git branch to delete.
    '''

    # Delete the specified local branch.
    print(f'Deleting local branch {git_branch}...')
    subprocess.run(['git', 'branch', '-D', git_branch])