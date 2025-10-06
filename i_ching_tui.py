import os
import threading
 
from monday import (
    create_item,
    query_items_page,
    create_doc_in_column,
    add_content_to_doc,
    update_simple_column_value
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

def create_citation_record(state, source: str = None):

    topic_label = f'Hexagram {state.hex_no:02d}'

    column_values = {
        'dropdown_mktx9w5w': 'Hexagrams',
        'dropdown_mktz2dg8': topic_label,
        'long_text_mktx8kf0': source,
        'board_relation_mktxwz8c': {
            'item_ids': [state.selected_work.id]
        },
    }

    state.citation_record = create_item(
        board_id=BOARD_ID,
        item_name=state.citation_type,
        group_id=GROUP_ID,
        column_values=column_values,
        create_labels_if_missing=True
    )

def format_cache_filename(state):
    citation_type_name = state.citation_type.lower().replace(' ', '_').replace('/', '_')
    return f'citation_{state.hex_no}_{citation_type_name}.txt'

def cache_citation_content(state, content: str, source: str = None):
    cache_dir = 'citation_cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, format_cache_filename(state))
    with open(cache_file, 'w') as f:
        for page in content:
            f.write(page+' |\n')
        if source:
            f.write(f'\n\n{source}')

def add_citation_content(state, content: str):

    doc = create_doc_in_column(state)

    add_content_to_doc(doc.id, content)

    update_simple_column_value(
        item_id=state.citation_record.id,
        column_id='status',
        value='Entered'
    )

def clear_citation_from_cache(state):
    cache_file = os.path.join('citation_cache', format_cache_filename(state))
    if os.path.exists(cache_file):
        os.remove(cache_file)

def execute_add_citation(state, content, source: str = None):
    
    cache_citation_content(state, content, source if source else None)

    create_citation_record(state, source if source else None)

    add_citation_content(state, content)

    clear_citation_from_cache(state)
    print(f'Citation for "{state.citation_type}" added successfully under Hexagram {state.hex_no:02d}.\n')

    state.is_processing = False

class State():

    hex_no = None
    selected_work = None
    citation_type = None
    citation_record = None
    is_processing = False

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
        
        content, source = enter_citation_content()
        if not content:
            print('No content entered. Press Ctrl+C to exit or start over.\n')
            continue

        # Set state to processing synchronously before starting thread
        state.is_processing = True

        threading.Thread(
            target=execute_add_citation, 
            args=(state, content, source if source else None)
        ).start()

        select_follow_up_menu(state)


if __name__ == '__main__':
    main()