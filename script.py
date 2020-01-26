from tools import generate_anki_cards_from_file
import os


def generate_all(input_folder, output_folder):
    input_files = os.listdir(input_folder)

    for file in input_files:
        file_name = file.split('.')[0]

        generate_anki_cards_from_file(
            input_file_path=input_folder + file,
            output_file_path=output_folder + file_name + '.tsv'
        )


path = '/Users/rafael/Documents/coding/hsk4_confucius_flashcards/'
input_path = path + 'input_hanzi/'
output_path = path + 'output_flashcards/'

# Generate a single flashcard from a single file
generate_anki_cards_from_file(
    input_file_path=input_path + 'lesson_2.txt',
    output_file_path=output_path + 'lesson_2.tsv'
)

# # Generate all flashcards from a given folder
# generate_all(
#     input_folder=input_path,
#     output_folder=output_path
# )
