from tools import generate_one_from_folder
import sys


# IO
def get_input_directory_arg(args):
    try:
        input_directory_arg = args[1]
        return input_directory_arg

    except IndexError:
        print('Missing first argument, should be input directory name.')
        exit()


def get_output_file_arg(args):
    try:
        output_file_arg = args[2]
        return output_file_arg
    except IndexError:
        print('Missing second argument, should be output file name.')
        exit()


if __name__ == '__main__':
    input_directory = get_input_directory_arg(sys.argv)
    output_file = get_output_file_arg(sys.argv)

    # Generate a single flashcard set from a given folder
    generate_one_from_folder(
        input_folder_path=input_directory,
        output_file_path=output_file

    )
