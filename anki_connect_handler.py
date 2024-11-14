import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def format_notes(deck_name, example_sentence_dict):
    notes = []
    for card in example_sentence_dict:
        note = {
            "deckName": deck_name,
            "modelName": "Basic (and reversed card)",
            "fields": {
                "Front": card['example_sentence'] + '<br>' + card['pinyin'],
                "Back": card['translations'][0]
            },
            "options": {
                "allowDuplicate": False
            },
            "tags": []
        }
        notes.append(note)
    return notes

def add_cards_to_new_deck(deck_name, example_sentence_dict):
    invoke('createDeck', deck=deck_name)
    notes = format_notes(deck_name, example_sentence_dict)
    result = invoke('addNotes', notes=notes)
    sync_anki()
    print(f"Added {len([r for r in result if r is not None])} cards to new deck {deck_name}")

def add_cards_to_existing_deck(deck_name, example_sentence_dict):
    notes = format_notes(deck_name, example_sentence_dict)
    result = invoke('addNotes', notes=notes)
    sync_anki()
    print(f"Added {len([r for r in result if r is not None])} cards to existing deck {deck_name}")

def sync_anki():
    invoke('sync')
