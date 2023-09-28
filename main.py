import utils
import re
import time

# get access token to use genius api
access_token = utils.get_access_token()


# start song search process
while True:
    song_title = input('Enter song title: ')
    print()
    song_options = utils.song_search(song_title, access_token)

    # Display results, song options
    for index, dict in enumerate(song_options, start=1):
        print(f"{index}: {dict['full_title']}")

    # Song slection
    try:
        song_index = int(input("Select song (enter 0 to restart): ")) - 1
        if not (song_index + 1):
            continue
        if 0 <= song_index < len(song_options):
            selected_song_id = song_options[song_index]['id']
            selected_song_title = re.sub(
                r'[\\/:*?"<>|]', '', song_options[song_index]['full_title'])
            break
        else:
            print("Invalid song selection")
    except ValueError as e:
        print(f'Must be a number between 1 - {len(song_options)}')


# Get lyrics from song title and artist
lyrics = utils.lyrics_search(
    selected_song_id, selected_song_title, access_token)
print()

# allow user to edit
while True:
    with open(f'{selected_song_title}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines into a list

    for i, line in enumerate(lines, start=1):
        print(f"{i}: {line.strip()}")

    print()
    print('Would you like to edit any lines of the lyrics?')
    line_index = input('Line # or 0 to continue: ')

    if line_index == '0':
        break  # Exit the loop if the user enters '0'

    try:
        line_index = int(line_index)  # Convert the input to an integer
        if 1 <= line_index <= len(lines):
            print('Enter the new content for the line:')
            line_replace = input(': ')

            # Update the selected line in the list of lines
            lines[line_index - 1] = line_replace + '\n'

            # Write the updated lines back to the file
            with open(f'{selected_song_title}.txt', 'w', encoding='utf-8') as file:
                file.writelines(lines)

            print('Line updated successfully.')
            time.sleep(2)
        else:
            print('Invalid line number. Please enter a valid line number.')
    except ValueError:
        print('Invalid input. Please enter a valid line number.')


print()
time.sleep(2)
print('Translator uses ISO 639-1 language codes')
time.sleep(2)
print('You will need to know the original language code and desired output language code.')
time.sleep(2)
show_codes = input(
    'Would you like to see a list of language codes? Y/n: ')
try:
    if show_codes.lower() == 'y':
        utils.print_languages()
except Exception as e:
    print(f'Error: {e}')

while True:
    print()
    song_lang = input('What language is the song in?: ')
    translate_lang = input(
        'What language would you like this song translated into?: ')
    print()
    print(f'Song language: {song_lang}')
    print(f'Translate into: {translate_lang}')
    print()
    response = input('Is this correct? Y/n: ')
    try:
        if response.lower() == 'y':
            break
    except Exception as e:
        print(f'Error: {e}')

print()
print('Translating... please wait')
utils.translate(selected_song_title, song_lang, translate_lang)
print(f'Completed - See file - {selected_song_title}.txt')
