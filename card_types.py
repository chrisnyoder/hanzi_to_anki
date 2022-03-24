from abc import abstractmethod
import copy

NEW_LINE_SEPARATOR = '<br>'


class AnkiCardCSVLine:

    def __init__(self, formatted_line):
        self.formatted_line = formatted_line

    @staticmethod
    def format_anki_card(
            front,
            back,
            tags=None,
            front_image='',
            back_image='',
            front_audio='',
            back_audio='',
            separator='\t'
    ):
        """
        Generic function to generate a string recognized by anki apps import modules
        :param front: string, front of the card.
        :param back: string, back of the card.
        :param tags: list of strings, tags of the card, no tags by default.
        :param separator: string, separator between front back and tags, tab by default, for tsv format.
        :param front_image:
        :param back_image:
        :param front_audio:
        :param back_audio:
        :return:
        """
        tags_separator = ','
        anki_elements = [
            '"' + front + '"',
            '"' + back + '"'
        ]

        if tags:
            anki_elements.append(
                '"{tags}"'.format(tags=tags_separator.join(tags))
            )

        anki_elements += [
            front_image,
            back_image,
            front_audio,
            back_audio
        ]

        return separator.join(anki_elements)

    @staticmethod
    def format_hanzi(hanzi_details):
        return '<font size="7">%s</font>' % hanzi_details['hanzi']

    @staticmethod
    def format_translation(hanzi_details):
        return NEW_LINE_SEPARATOR.join(hanzi_details['translations']).replace(',', ';')

    @staticmethod
    def format_pinyin(hanzi_details):
        return '<b><font size="5">%s</font></b>' % hanzi_details['pinyin']

    @classmethod
    @abstractmethod
    def format(cls, hanzi_details):
        raise NotImplementedError


class HanziFront(AnkiCardCSVLine):

    def __init__(self, formatted_line):
        super().__init__(formatted_line)

    @classmethod
    def format(cls, hanzi_details):
        """
        Given a dictionary with hanzi details: hanzi pinyin translations and tags, format it as a anki card string.
        :param hanzi_details: dict, containing one hanzi details
        :return: string, formatted anki card string
        """
        front = cls.format_hanzi(hanzi_details)

        back = NEW_LINE_SEPARATOR.join([
            cls.format_pinyin(hanzi_details),
            cls.format_translation(hanzi_details)
        ])
        back_audio = hanzi_details['hanzi'] + '.mp3'

        tags = copy.deepcopy(hanzi_details.get('tags', []))
        tags += [cls.__name__]

        return cls(
            formatted_line=cls.format_anki_card(
                front=front,
                back=back,
                tags=tags,
                back_audio=back_audio,
                separator=','
            )
        )


class SpeechFront(AnkiCardCSVLine):

    def __init__(self, formatted_line):
        super().__init__(formatted_line)

    @classmethod
    def format(cls, hanzi_details):
        """
        :param hanzi_details: dict, containing one hanzi details
        :return: string, formatted anki card string
        """
        front = ''
        front_audio = hanzi_details['hanzi'] + '.mp3'

        back = NEW_LINE_SEPARATOR.join([
            cls.format_hanzi(hanzi_details),
            cls.format_pinyin(hanzi_details),
            cls.format_translation(hanzi_details)
        ])

        tags = copy.deepcopy(hanzi_details.get('tags', []))
        tags += [cls.__name__]

        return cls(
            formatted_line=cls.format_anki_card(
                front=front,
                back=back,
                tags=tags,
                front_audio=front_audio,
                separator=','
            )
        )


class TranslationFront(AnkiCardCSVLine):

    def __init__(self, formatted_line):
        super().__init__(formatted_line)

    @classmethod
    def format(cls, hanzi_details):
        """
        :param hanzi_details: dict, containing one hanzi details
        :return: string, formatted anki card string
        """
        front = cls.format_translation(hanzi_details)

        back = NEW_LINE_SEPARATOR.join([
            cls.format_hanzi(hanzi_details),
            cls.format_pinyin(hanzi_details),
        ])
        back_audio = hanzi_details['hanzi'] + '.mp3'

        tags = copy.deepcopy(hanzi_details.get('tags', []))
        tags += [cls.__name__]

        return cls(
            formatted_line=cls.format_anki_card(
                front=front,
                back=back,
                tags=tags,
                back_audio=back_audio,
                separator=','
            )
        )
