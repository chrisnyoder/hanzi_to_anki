# hanzi_to_anki

This is a simple script that I developed in order to help myself creating flashcards.
Flashcards is a nice technique to memorize whatever you'd like.

I am learning chinese and I needed to create my owns as the one covered on the apps are sometimes too general and i'd like to focus on vocabulary i have been learning recently.

The goal is to be able to create, from a list of hanzi (chinese character), like "你好", get its pinyin (phonetic transcription) and its translations, to later create  a card from it. List of hanzi is easy to get, just type them on a file and then generate all the pinyin and translation automatically, which is the most annoying and time consuming part.

# How to use

Don't forget to install requirements

```bash
pip install -r requirements.txt
```


## Generate flashcards for one input file

See _script.py_ for example.

Given a file containing a list of hanzi:

> **Lesson1.txt**  
> 学校  
> 兴趣  
> 从来  
> 共同  
> 幸福

```python
from tools import generate_anki_cards_from_file

generate_anki_cards_from_file(
    input_file_path='Lesson1.txt',
    output_file_path='FlashCardsLesson1.tsv'
)

```

> **FlashCardsLesson1.tsv**  
> 学校	xuéxiào - school CL:所[suo3]  
> 兴趣	xīngqù - interest (desire to know about sth) interest (thing in which one is interested) hobby CL:個|个[ge4]  
> 从来	cónglái - always at all times never (if used in negative sentence)  
> 共同	gòngtóng - common joint jointly together collaborative  
> 幸福	xìngfú - happiness happy blessed  

This file can then directly be imported to any Anki like app as a tsv.

## Generate all flashcards from a folder containing input files

See _script.py_ for example.

# Libraries used

- pinyin: http://pinyin.lxyu.net
