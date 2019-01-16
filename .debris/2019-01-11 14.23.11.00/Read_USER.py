from pyqum.instrument.logger import get_data, search_param

# USR = get_data("LTH")
USR = {'A': {'B': {'C': {'D': {'E': 100}}}},
'A1': {'B': {'C': {'D': {'E': 100}}}},
'A2': {'B': {'C': {'D': {'E': 100}}}},
'A3': {'B1': 100, 'C1': 200, 'D1': 300, 'E1': {'F1: 100'}},
'A4': 100, 'AA': {'B2': {'C2': 100, 'D2': 300}},
'A5': {'B3': {'C3': 100, 'D3': {'E3': 100, 'F3': 200, 'G3': 300}}},
'A6': {'B5': {'C5': {'D5': {'E5': {'F5': {'G5': 100, 'H24': 'David'}}}}}}, 'alien': 'is good',
'A7': 100, 'B7': 100, 'C7': {'D7': {'E7': 200, 'F7': 100, 'G7': 300}}}

def deletelement_from_dict(dictionary, keys):
    from contextlib import suppress
    for key in keys:
        with suppress(KeyError):
            del dictionary[key]
    for value in dictionary.values():
        if hasattr(value, 'items'):
            deletelement_from_dict(value, keys)

result = search_param(USR, 100)
print("\nSearch result: %s" %list(result))
