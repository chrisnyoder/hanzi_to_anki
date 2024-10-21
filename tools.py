import pinyin
import pinyin.cedict as cedict
import os
import logging
import shutil
import time
from zipfile import ZipFile
from os.path import basename
from natsort import natsorted
from openai_handler import OpenAIHandler
logger = logging.getLogger(__name__)


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

    with open(file=file_path, mode='r', encoding='utf8') as f:
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
    :param hanzi: dict, containing hanzi and tags
    :return: dict, containing hanzi's details
    """
    # Add pinyin info to the given hanzi dict
    try:
        hanzi['pinyin'] = pinyin.get(hanzi['hanzi'])
    except:
        logger.warning('Pinyin not found for: %s' % hanzi['hanzi'])
        hanzi['pinyin'] = 'Not found'

    # Add translation info to the given hanzi dict, as a list of translations.
    translations_list = cedict.translate_word(hanzi['hanzi'])
    if type(translations_list) != list:
        logger.warning('Translation not found for: %s' % hanzi['hanzi'])
        translations_list = ['Not Found']

    hanzi['translations'] = translations_list

    hanzi['audio'] = '%s.mp3' % hanzi['hanzi']

    return hanzi


def write_card(formatted_details, output_file_path):
    """

    :param formatted_details:
    :param output_file_path:
    :return:
    """
    with open(file=output_file_path, mode='w+', encoding='utf8') as f:
        f.write('\n'.join(formatted_details))

def get_formatted_details_using_dict(hanzi_details, default_tag=None, card_type=None):
    # Add a default tag if given
    if default_tag:
        for hanzi in hanzi_details:
            hanzi['tags'].append(default_tag)
   
    from card_types import HanziFront, SpeechFront, TranslationFront

    # All by default
    card_types = [card_type] if card_type else [
        HanziFront,
        SpeechFront,
        TranslationFront
    ]

    formatted_details = []
    for card_type in card_types:
        formatted_details += [
            card_type.format(hanzi_details=details).formatted_line
            for details in hanzi_details
        ]

    # Write them to the given output file path
    return formatted_details

def generate_anki_cards_using_dict(hanzi_list, default_tag=None, card_type=None):
    """

    :param hanzi_list:
    :param default_tag:
    :param card_type
    :return:
    """
    # Get the additional details, pinyin and translations
    hanzi_details = [
        get_hanzi_details(hanzi)
        for hanzi in hanzi_list
    ]

    return get_formatted_details_using_dict(hanzi_details, default_tag, card_type)


def generate_anki_cards_using_ai(hanzi_list, default_tag=None, card_type=None):
    openai_handler = OpenAIHandler()
    
    example_sentence_dicts = []
    for hanzi in hanzi_list:
        example_sentence_dict = openai_handler.get_openai_response(hanzi['hanzi'])
        example_sentence_dicts.append(example_sentence_dict)
        time.sleep(1)

    return get_formatted_details_using_dict(example_sentence_dicts, default_tag, card_type)

def zip_directory(output_file_path):
    # create a ZipFile object
    with ZipFile(output_file_path + '.zip', 'w') as zip_obj:
        # Iterate over all the files in directory
        for folder_name, sub_folders, filenames in os.walk(output_file_path):
            for filename in filenames:
                # create complete filepath of file in directory
                file_path = os.path.join(folder_name, filename)

                # Add file to zip
                zip_obj.write(file_path, basename(file_path))


def generate_audios(hanzi_list, output_file_path):
    from tts_tools import create_audio

    for hanzi in hanzi_list:
        hanzi = hanzi['hanzi']

        create_audio(hanzi, output_path=output_file_path)


def write_anki_cards_from_file(input_file_path, output_file_path, add_audio=False, use_ai=False):
    """
    :param input_file_path:
    :param output_file_path:
    :param add_audio:
    :param mode
    :return:
    """
    # Preparing the folder
    try:
        shutil.rmtree(output_file_path)
    except:
        pass
    os.mkdir(output_file_path)

    card_file = output_file_path + '/cards.csv'

    # Extract list of hanzi from the given input file path
    hanzi_list = read_hanzi_from_file(
        file_path=input_file_path
    )

    # Generate the cards content
    if use_ai:
        formatted_details = generate_anki_cards_using_ai(hanzi_list)
    else:
        formatted_details = generate_anki_cards_using_dict(hanzi_list)
   
    input('Continue ? Press any key')

    # Export the content
    write_card(formatted_details, card_file)

    # Generate the audios
    if add_audio:
        generate_audios(hanzi_list, output_file_path)

    # Zip directory. directory => directory.zip
    zip_directory(output_file_path)

    # Remove directory
    shutil.rmtree(output_file_path)


def generate_all(input_folder_path, output_folder_path):
    """

    :param input_folder_path:
    :param output_folder_path:
    :return:
    """
    input_files = os.listdir(input_folder_path)

    for file in input_files:
        file_name = file.split('.')[0]

        write_anki_cards_from_file(
            input_file_path=input_folder_path + file,
            output_file_path=output_folder_path + file_name + '.tsv'
        )


def generate_one_from_folder(input_folder_path, output_file_path):
    """

    :param input_folder_path:
    :param output_file_path:
    :return:
    """
    input_files = natsorted(os.listdir(input_folder_path))

    all_formatted_details = []

    for file in input_files:
        file_name = file.split('.')[0]

        hanzi_list = read_hanzi_from_file(
            file_path=input_folder_path + file,
        )

        # Generate the cards content
        formatted_details = generate_anki_cards_using_dict(
            hanzi_list=hanzi_list,
            default_tag=file_name
        )

        # Append to global list
        all_formatted_details += formatted_details

    # Export the content
    write_card(all_formatted_details, output_file_path)
