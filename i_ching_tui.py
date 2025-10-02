import os
import json

from monday_app import app
from monday import (
    create_item,
    query_items_page
)
from i_ching import (
    enter_hexagram_number,
    select_work_to_cite,
    select_citation_type_menu,
    enter_citation_content,
    select_follow_up_menu
)

BOARD_ID = os.getenv('I_CHING_CITATIONS_BOARD_ID', '9835217647')
GROUP_ID = os.getenv('I_CHING_CITATIONS_GROUP_ID', 'topics')
WORKS_CITED_BOARD_ID = os.getenv('I_CHING_WORKS_CITED_BOARD_ID', '8437366843')

def create_citation_record(state):

    topic_label = f'Hexagram {state.hex_no:02d}'

    column_values = {
        'dropdown_mktx9w5w': 'Hexagrams',
        'dropdown_mktz2dg8': topic_label,
        'board_relation_mktxwz8c': {
            'item_ids': [state.selected_work.id]
        },
    }

    print('Creating citation record...')
    state.citation_record = create_item(
        board_id=BOARD_ID,
        item_name=state.citation_type,
        group_id=GROUP_ID,
        column_values=column_values,
        create_labels_if_missing=True
    )

def add_citation_content(state, content: str):

    print('Creating document for citation content...')
    doc = app.run(
        'doc.create_doc_in_column',
        data=dict(
            column_id='doc_mktxy71m',
            item_id=state.citation_record.id, 
        )
    )

    app.run(
        'doc.update_doc_name',
        data=dict(
            doc_id=doc.id,
            name=state.citation_type
        )
    )

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
            item_id=state.citation_record.id,
            column_id='long_text_mktx8kf0',
            value=source
        ))

    print('Citation content added to document\n')
    app.run(
        'item.update_simple_column_value',
        data=dict(
            item_id=state.citation_record.id,
            column_id='status',
            value='Entered'
        )
    )

class State():

    hex_no = None
    selected_work = None
    citation_type = None
    citation_record = None

    def __init__(self, works):
        self.works = works

def main():
    
    print('Welcome to the I Ching Citation Adder powered by Tiferet!')
    print('This tool will help you add citation items to your Monday.com board.')
    print('-----------------------------------------------\n')

    print('Fetching works from the Works Cited board...')
    works = query_items_page(board_id=WORKS_CITED_BOARD_ID, limit=100)
    state = State(works)

    while True:

        if not state.hex_no:
            enter_hexagram_number(state)

        if not state.selected_work:
            select_work_to_cite(state)

        if not state.citation_type:
            select_citation_type_menu(state)
        
        content = enter_citation_content()
        if not content:
            print('No content entered. Press Ctrl+C to exit or start over.\n')
            continue
        
        create_citation_record(state)

        add_citation_content(state, content)

        select_follow_up_menu(state)


if __name__ == '__main__':
    main()