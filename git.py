import subprocess

GITHUB_BASE_BRANCH = 'main'

def pull_latest_from_base_branch(base_branch: str = GITHUB_BASE_BRANCH):
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

def delete_local_branch(git_branch: str):
    '''
    Delete a local git branch.
    :param git_branch: The name of the git branch to delete.
    '''

    # Delete the specified local branch.
    print(f'Deleting local branch {git_branch}...')
    subprocess.run(['git', 'branch', '-D', git_branch])