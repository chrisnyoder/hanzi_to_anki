from tools import generate_all
import sys


# IO
def get_input_directory_arg(args):
    try:
        input_directory_arg = args[1]
        return input_directory_arg

    except IndexError:
        print('Missing first argument, should be input directory name.')
        exit()


def get_output_directory_arg(args):
    try:
        output_directory_arg = args[2]
        return output_directory_arg
    except IndexError:
        print('Missing second argument, should be output directory name.')
        exit()


if __name__ == '__main__':
    input_directory = get_input_directory_arg(sys.argv)
    output_directory = get_output_directory_arg(sys.argv)

    # Generate separate flashcards sets for input files from a given folder
    generate_all(
        input_folder_path=input_directory,
        output_folder_path=output_directory
    )
