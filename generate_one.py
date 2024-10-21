from tools import write_anki_cards_from_file
import sys


# IO
def get_input_file_arg(args):
    try:
        input_file_arg = args[1]
        return input_file_arg

    except IndexError:
        print('Missing first argument, should be input file name.')
        exit()


def get_output_file_arg(args):
    try:
        output_file_arg = args[2]
        return output_file_arg
    except IndexError:
        print('Missing second argument, should be output file name.')
        exit()

def get_use_ai_arg(args):
    return '--use-ai' in args

if __name__ == '__main__':
    input_file = get_input_file_arg(sys.argv)
    output_file = get_output_file_arg(sys.argv)

    # Get the use_ai flag from the command line arguments
    use_ai = get_use_ai_arg(sys.argv)

    # Generate a single flashcard set from a single file
    write_anki_cards_from_file(
        input_file_path=input_file,
        output_file_path=output_file,
        add_audio=True,
        use_ai=use_ai
    )
