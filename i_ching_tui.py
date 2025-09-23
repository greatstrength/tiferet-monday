import os
import json

from monday_app import app
from monday import (
    create_item
)

BOARD_ID = os.getenv('I_CHING_CITATIONS_BOARD_ID', '9835217647')
GROUP_ID = os.getenv('I_CHING_CITATIONS_GROUP_ID', 'topics')
WORKS_CITED_BOARD_ID = os.getenv('I_CHING_WORKS_CITED_BOARD_ID', '8437366843')
CITATION_TYPES = [
    'Summary Terms',
    'Name',
    'Judgement - Translation',
    'Judgement - Interpretation',
    'Outer and Inner Worlds',
    'Hidden Possibility',
    'Sequence',
    'Definition',
    'Image - Translation',
    'Changing Line 1 - Translation',
    'Changing Line 1 - Interpretation',
    'Changing Line 2 - Translation',
    'Changing Line 2 - Interpretation',
    'Changing Line 3 - Translation',
    'Changing Line 3 - Interpretation',
    'Changing Line 4 - Translation',
    'Changing Line 4 - Interpretation',
    'Changing Line 5 - Translation',
    'Changing Line 5 - Interpretation',
    'Changing Line 6 - Translation',
    'Changing Line 6 - Interpretation',  
]

def get_hexagram_no():
    while True:
        try:
            print('Enter the hexagram number you want to add citations for (1-64): ')
            hexagram_no = int(input('> ').strip())
            if 1 <= hexagram_no <= 64:
                print('You entered hexagram number:', hexagram_no)
                print('')
                return hexagram_no
            else:
                print('Please enter a number between 1 and 64.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

def to_hexagram_topic_label(hexagram_no: int) -> str:
    return f'Hexagram {hexagram_no:02d}'

def list_works_cited():
    works = app.run('board.query_items_page', data=dict(
        board_id=WORKS_CITED_BOARD_ID,
        limit=100
    ))
    return works

def works_cited_selection_menu(works):
    print('Select a work from the list below by entering its number:')
    for idx, work in enumerate(works, start=1):
        print(f"{idx}. {work.name} (ID: {work.id})")
    print("Press Esc to cancel.")
    
    while True:
        try:
            choice = int(input('> ').strip())
            if choice == 'Esc':
                print('Operation cancelled.')
                return None
            elif 1 <= choice <= len(works):
                selected_work = works[choice - 1]
                print(f'You selected: {selected_work.name} (ID: {selected_work.id})\n')
                return selected_work
            else:
                print(f'Please enter a number between 0 and {len(works)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')


def select_citation_type_menu():
    print('Select a citation type from the list below by entering its number:')
    for idx, ctype in enumerate(CITATION_TYPES, start=1):
        print(f"{idx}. {ctype}")
    print("Press Esc to cancel.")
    
    while True:
        try:
            choice = input('> ').strip()
            if choice.lower() == 'esc':
                print('Operation cancelled.')
                return None
            choice_int = int(choice)
            if 1 <= choice_int <= len(CITATION_TYPES):
                selected_type = CITATION_TYPES[choice_int - 1]
                print(f'You selected: {selected_type}\n')
                return selected_type
            else:
                print(f'Please enter a number between 1 and {len(CITATION_TYPES)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

def create_citation_record(selected_work, topic_label, citation_type):

    column_values = {
        'dropdown_mktx9w5w': 'Hexagrams',
        'dropdown_mktz2dg8': topic_label,
        'board_relation_mktxwz8c': {
            'item_ids': [selected_work.id]
        },
    }

    print('Creating citation record...')
    return create_item(
        board_id=BOARD_ID,
        item_name=citation_type,
        group_id=GROUP_ID,
        column_values=column_values,
        create_labels_if_missing=True
    )

def add_citation_content(item_id: str, citation_type: str):

    print('Creating document for citation content...')
    doc = app.run(
        'doc.create_doc_in_column',
        data=dict(
            column_id='doc_mktxy71m',
            item_id=item_id, 
        )
    )

    app.run(
        'doc.update_doc_name',
        data=dict(
            doc_id=doc.id,
            name=citation_type
        )
    )

    print('Enter in the citation content (end with a blank line):\n')
    lines = []
    while True:
        line = input()

        if line == '':
            break
        lines.append(line)
    content = '\n'.join(lines)

    print('Updating document with citation content...')
    doc_content = dict(
        alignment='left',
        direction='ltr',
        deltaFormat= [
            {'insert': content}
        ]
    )
    app.run(
        'doc.create_doc_block', 
        data=dict(
            doc_id=doc.id,
            type='normal_text',
            content=json.dumps(doc_content)
        )
    )

    print('Please enter in citation source (or press Enter to skip):')
    source = input('> ').strip()
    if source:
        app.run('item.update_simple_column_value', data=dict(
            item_id=item_id,
            column_id='long_text_mktx8kf0',
            value=source
        ))

    print('Citation content added to document\n')
    app.run(
        'item.update_simple_column_value',
        data=dict(
            item_id=item_id,
            column_id='status',
            value='Entered'
        )
    )

def main():
    
    print('Welcome to the I Ching Citation Adder powered by Tiferet!')
    print('This tool will help you add citation items to your Monday.com board.')
    print('-----------------------------------------------\n')

    hex_no = None
    selected_work = None

    while True:

        # Get hexagram number if it does not exist.
        if not hex_no:
            hex_no = get_hexagram_no()

        # Otherwise ask if they want to add another citation to it.
        else:
            print(f'You are currently working on citations for Hexagram {hex_no:02d}.')
            print('Would you like to add another citation for this hexagram? (y/n)')
            choice = input('> ').strip().lower()
            if choice == 'y':
                pass
            elif choice == 'n':
                hex_no = get_hexagram_no()
            else:
                print('Invalid input. Please enter y or n.')
                continue
            print('')

        # Get topic label.
        topic_label = to_hexagram_topic_label(hex_no)

        if selected_work:
            print(f'You have previously selected the work: {selected_work.name} (ID: {selected_work.id})')
            print('Would you like to use this work again? (y/n)')
            choice = input('> ').strip().lower()
            if choice == 'y':
                pass
            else:
                works = list_works_cited()
                selected_work = works_cited_selection_menu(works)
        print('')

        if not selected_work:
            return
        
        citation_type = select_citation_type_menu()
        if not citation_type:
            return
        
        item = create_citation_record(selected_work, topic_label, citation_type)

        add_citation_content(item.id, citation_type)


if __name__ == '__main__':
    main()