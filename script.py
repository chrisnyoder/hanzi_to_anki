from tools import generate_anki_cards_from_file, generate_all, generate_one_from_folder


path = '/Users/rafael/Documents/coding/hsk4_confucius_flashcards/'
input_path = path + 'input_hanzi/hsk3/'
output_path = path + 'output_flashcards/hsk3/'

# # Generate a single flashcard from a single file
# generate_anki_cards_from_file(
#     input_file_path=input_path + 'lesson_2.txt',
#     output_file_path=output_path + 'lesson_2.tsv'
# )

# # Generate all flashcards from a given folder
# generate_all(
#     input_folder_path=input_path,
#     output_folder_path=output_path
# )


generate_one_from_folder(
    input_folder_path=input_path,
    output_file_path=output_path + 'all_lessons.tsv'

)