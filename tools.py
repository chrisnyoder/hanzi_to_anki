import pinyin
import pinyin.cedict as cedict


def format_anki_card(front, back, tags=None, separator='\t'):
    """
    Generic function to generate a string recognized by anki apps import modules
    :param front: string, front of the card.
    :param back: string, back of the card.
    :param tags: list of strings, tags of the card, no tags by defualt.
    :param separator: string, separator between front back and tags, tab by default, for tsv format.
    :return:
    """
    tags_separator = ','
    anki_elements = [
        front,
        back
    ]

    if tags:
        anki_elements.append(tags_separator.join(tags))

    return separator.join(anki_elements)


def read_hanzi_from_file(file_path, get_tags=True):
    """
    Given a file's path, read and extract the hanzi, one hanzi by line. Multiple tags can be added after the hanzi,
    separated by space
    :param file_path: string, path of the file
    :param get_tags: boolean, whether or not to extract tags
    :return:
    """
    hanzi_dicts = []

    incorrect_lines = ['\n', '', None]

    with open(file=file_path, mode='r') as f:
        lines = f.readlines()

    # Process lines
    for line in lines:
        # Skipping if line is incorrect
        if line in incorrect_lines:
            continue

        words = line.split()

        # Extracting hanzi
        hanzi = words[0]
        hanzi_dict = {
            'hanzi': hanzi
        }

        if not get_tags:
            continue

        if len(words) > 1:
            tags = words[1:]
            tags = list(tags)
        else:
            tags = []

        hanzi_dict['tags'] = tags

        hanzi_dicts.append(hanzi_dict)

    return hanzi_dicts


def get_hanzi_details(hanzi):
    """
    Given an hanzi, get its translations and pinyin, return a dictionary containing all three infos
    :param hanzi: string, hanzi to get details from
    :return: dict, containing hanzi's details
    """
    # Create output structure, dict
    hanzi_details = {'hanzi': hanzi}

    # Add pinyin info to the given hanzi dict
    try:
        hanzi_details['pinyin'] = pinyin.get(hanzi)
    except:
        hanzi_details['pinyin'] = 'Not found'

    # Add translation info to the given hanzi dict, as a list of translations.
    translations_list = cedict.translate_word(hanzi)
    if type(translations_list) != list:
        translations_list = ['Not Found']

    hanzi_details['translations'] = translations_list

    return hanzi_details


def format_hanzi_details_to_ankiapp_flashcard(hanzi_details):
    """
    Given a dictionary with hanzi details: hanzi pinyin translations and tags, format it as a anki card string.
    :param hanzi_details: dict, containing one hanzi's details
    :return: string, formatted anki card string
    """
    new_line_separator = '<br>'

    return format_anki_card(
        front=hanzi_details['hanzi'],
        back='%s - %s' % (
            hanzi_details['pinyin'],
            new_line_separator.join(hanzi_details['translations'])
        ),
        tags=hanzi_details.get('tags', None)
    )


def generate_anki_cards_from_file(input_file_path, output_file_path):
    """

    :param input_file_path:
    :param output_file_path:
    :return:
    """
    # Extract list of hanzi from the given input file path
    hanzi_list = read_hanzi_from_file(
        file_path=input_file_path
    )

    # Get the additional details, pinyin and translations
    hanzi_details = [
        get_hanzi_details(hanzi['hanzi'])
        for hanzi in hanzi_list
    ]

    # Format to anki card format
    formatted_details = [
        format_hanzi_details_to_ankiapp_flashcard(details)
        for details in hanzi_details
    ]

    # Write them to the given output file path
    with open(file=output_file_path, mode='w+') as f:
        f.write('\n'.join(formatted_details))