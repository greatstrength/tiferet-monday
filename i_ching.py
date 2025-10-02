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
    lines = []
    while True:
        line = input()

        if line == '':
            break
        lines.append(line)
    return '\n'.join(lines)

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
    print('Select what you wish to do next:')
    print('1. Add another citation for the same hexagram.')
    print('2. Enter citations for a new hexagram number.')
    print('3. Add citations for a different work.')
    print('4. Quit the program.')

    # Set the citation type to none regardless.
    state.citation_type = None

    while True:
      
        try:
            choice = int(input('> ').strip())

            # If another citation is requested, keep hex_no and selected_work the same.
            if choice == 1:
                break

            # If a new hexagram is requested, set the hex_no to None.
            elif choice == 2:
                state.hex_no
                break

            # If a new work is requested, set the selected_work to None.
            elif choice == 3:
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