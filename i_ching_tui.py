import os

from monday_app import app
from monday import create_item

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
                print(f'You selected: {selected_work.name} (ID: {selected_work.id})')
                return selected_work
            else:
                print(f'Please enter a number between 0 and {len(works)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

def to_hexagram_topic_label(hexagram_no: int) -> str:
    return f'Hexagram {hexagram_no:02d}'


def main():
    
    print('Welcome to the I Ching Citation Adder powered by Tiferet!')
    print('This tool will help you add citation items to your Monday.com board.')
    print('-----------------------------------------------')

    hex_no = get_hexagram_no()

    works = list_works_cited()
    selected_work = works_cited_selection_menu(works)
    if not selected_work:
        return

if __name__ == '__main__':
    main()