import os, subprocess, json

from monday_app import app
from tiferet_monday.models.item import ItemDetail

GITHUB_BRANCH = 'v1.0.0-proto'
GITHUB_BEFORE_BRANCH = 'main'
# TASK_ID = 10040173963
SUBTASK_ID = 10015386326
MODULE_ITEM_ID = 10015367194
# SUBTASK_NAME = 'Contexts - Tests (Request) - Add Tests for Flask Request Context'
INCLUDE_BEFORE = False

def read_and_copy_code(doc_id: str, github_branch: str, module_path: str):

    # Current path
    current_path = os.getcwd()

    # Now, read the root project path from the environment variable, or use the default
    root_project_path = os.getenv('TIFERET_APP_PROJECT_ROOT', '/Users/ashatz/Code/aikicore')

    # First, navigate to the root project path
    os.chdir(root_project_path)

    # Then, using git via the subprocess module, checkout the specified GitHub repo
    subprocess.run(['git', 'checkout', github_branch])

    # No read the file content from the specified module path
    with open(os.path.join(root_project_path, module_path), 'r') as f:
        code = f.read().split('\n')

    # Return to the original path
    os.chdir(current_path)

    delta_format = []
    has_new_line = False
    for line in code:
        # This means there is an empty line for a code block
        if line.strip() == '' and has_new_line:
            delta_format.append({'insert': '\n\n', 'attributes': {'code-block': True}})
            has_new_line = False
        else:
            if has_new_line:
                delta_format.append({'insert': '\n', 'attributes': {'code-block': True}})
            delta_format.append({'insert': line})
            has_new_line = True

    doc_content = dict(
        alignment='left',
        direction='ltr',
        deltaFormat=delta_format
    )

    app.run(
        'doc.create_doc_block', 
        data=dict(
            doc_id=doc_id,
            type='code',
            content=json.dumps(doc_content)
        )
    )

# # Check to see if the subtask already exists
# print('Checking for existing subtask...')
# subtasks = app.run('item.query_subitems', data=dict(
#     parent_item_id=TASK_ID
# ))
# subtask_data = next((s for s in subtasks if s.name == SUBTASK_NAME), None)
# create_new = not subtask_data

# if create_new:
#     print('Creating new subtask...')
#     subtask_data = app.run('item.create_subitem', data=dict(
#         parent_item_id=TASK_ID,
#         item_name=SUBTASK_NAME,
#         column_values={
#             'board_relation_mkv3pq0v': {'item_ids': [MODULE_ITEM_ID]},
#         })
#     )

print('Retrieving subtask details...')
subtask = app.run('item.query_detail_by_id', data=dict(
    item_id=SUBTASK_ID
))

# if create_new:
#     print('Adding column values to subtask...')
#     status_column = subtask.get_column_value('Status')
#     app.run('item.update_simple_column_value', data=dict(
#         item_id=subtask.id,
#         column_id=status_column.id,
#         value='Ready to start')
#     )

#     estimated_sp = subtask.get_column_value('Estimated SP')
#     app.run('item.update_simple_column_value', data=dict(
#         item_id=subtask.id,
#         column_id=estimated_sp.id,
#         value='1')
#     )

#     type_column = subtask.get_column_value('Type')
#     app.run('item.update_simple_column_value', data=dict(
#         item_id=subtask.id,
#         column_id=type_column.id,
#         value=SUBTASK_TYPE)
#     )

print('Retrieving code module...')
module = app.run('item.query_detail_by_id', data=dict(
    item_id=MODULE_ITEM_ID
))

print('Creating new/after code doc...')
new_after_code = subtask.get_column_value('Code (New/After)')
doc = app.run('doc.create_doc_in_column', data=dict(
    item_id=subtask.id,
    column_id=new_after_code.id,
))

print('Reading and copying code (new/after)...')
read_and_copy_code(
    doc_id=doc.get('id'),
    github_branch=GITHUB_BRANCH,
    module_path=module.name
)

if INCLUDE_BEFORE:
    print('Creating before code doc...')
    before_code = subtask.get_column_value('Code (Before)')
    doc = app.run('doc.create_doc_in_column', data=dict(
        item_id=subtask.id,
        column_id=before_code.id,
    ))

    print('Reading and copying code (before)...')
    read_and_copy_code(
        doc_id=doc.get('id'),
        github_branch=GITHUB_BEFORE_BRANCH,
        module_path=module.name
    )