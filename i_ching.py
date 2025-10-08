from time import sleep

CITATION_TYPES = [
    'Summary/Key Terms',
    'Name',
    'Judgement - Translation',
    'Judgement - Interpretation',
    'Outer and Inner Worlds',
    'Hidden Possibility',
    'Sequence',
    'Definition',
    'Image - Translation',
    'Image - Interpretation',
    'Lines - General',
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
    'All Changing Lines - Translation',
    'All Changing Lines - Interpretation'
]

def enter_hexagram_number(state):
    while True:
        try:
            print('Enter the hexagram number you want to add citations for (1-64).')
            print('Press Ctrl+C to exit.')
            hexagram_no = int(input('> ').strip())
            if 1 <= hexagram_no <= 64:
                print('You entered hexagram number:', hexagram_no)
                print('')
                state.hex_no = hexagram_no
                break
            else:
                print('Please enter a number between 1 and 64.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyboardInterrupt:
            print('\nOperation cancelled by user.')
            exit(0)

def select_work_to_cite(state):
    
    works = state.works

    print('Select a work from the list below by entering its number:')
    for idx, work in enumerate(works, start=1):
        print(f"{idx}. {work.name} (ID: {work.id})")
    print("Press q to exit.")
    
    while True:
        try:
            choice = int(input('> ').strip())
            if choice == 'q':
                print('Operation cancelled.')
                return
            elif 1 <= choice <= len(works):
                selected_work = works[choice - 1]
                print(f'You selected: {selected_work.name} (ID: {selected_work.id})\n')
                state.selected_work = selected_work
                break
            else:
                print(f'Please enter a number between 0 and {len(works)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

def enter_citation_content():
    print('Enter in the citation content (end with a blank line):\n')
    pages = []
    lines = []
    source = None
    while True:
        line = input()

        if line == '':
            print('Is this a page break? Choose one of the following options:')
            print('y - Add a page break and continue entering content')
            print('n - Finish entering content')
            print('Or enter a citation source (or press Enter to skip):')
            choice = input('> ').strip().lower()
            if choice == 'y':
                if lines:
                    pages.append('\n'.join(lines))
                    lines = []
                    print('Page break added. Continue entering content or press Enter again to finish.\n')
                else:
                    print('No content to save for this page break.')
            else:
                if lines:
                    pages.append('\n'.join(lines))
                source = choice if choice else None
                break
        else:
            lines.append(line)
    return pages, source

def select_citation_type_menu(state):
    print('Select a citation type from the list below by entering its number:')
    for idx, ctype in enumerate(CITATION_TYPES, start=1):
        print(f"{idx}. {ctype}")
    print("Press q to quit.")
    
    while True:
        try:
            choice = input('> ').strip()
            if choice.lower() == 'q':
                print('Operation cancelled.')
                exit(0)
            choice_int = int(choice)
            if 1 <= choice_int <= len(CITATION_TYPES):
                selected_type = CITATION_TYPES[choice_int - 1]
                print(f'You selected: {selected_type}\n')
                state.citation_type = selected_type
                break
            else:
                print(f'Please enter a number between 1 and {len(CITATION_TYPES)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

def select_follow_up_menu(state):
   
    still_processing = False

    while True:
        if state.is_processing:
            if not still_processing:
                still_processing = True
                print('Currently processing the citation. Please wait...')
            else:
                print('Still processing. Please wait...')
            sleep(5)
            continue

        index = CITATION_TYPES.index(state.citation_type) + 1

        if index < len(CITATION_TYPES):
            print(f'Do you wish to add the next citation for: {CITATION_TYPES[index]}? (y/n or Enter to skip)')
            choice = input('> ').strip().lower()
            print('')
            if choice == 'y':
                state.citation_type = CITATION_TYPES[index]
                return
            else:
                state.citation_type = None
            
        print('Select what you wish to do next:')
        print('1. Add another citation for the same hexagram.')
        print('2. Enter citations for a new hexagram number.')
        print('3. Add citations for a different work.')
        print('4. Quit the program.')

        try:
            choice = int(input('> ').strip())

            # If another citation is requested, keep hex_no and selected_work the same.
            if choice == 1:
                break

            # If a new hexagram is requested, set the hex_no and citation_type to None.
            elif choice == 2:
                state.hex_no = None
                break

            # If a new work is requested, set the selected_work to None.
            elif choice == 3:
                state.hex_no = None
                state.selected_work = None
                break

            # If quitting is requested, exit the program.   
            elif choice == 4:
                print('Exiting the program.')
                exit(0)

            else:
                print('Please enter a number between 1 and 4.')
                
        except ValueError:
            print('Invalid input. Please enter a valid number.')