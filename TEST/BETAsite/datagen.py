import json

data = {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          'y': [0, 2, 3, 5, 8, 12, 10, 13, 15, 17.9, 21, 25, 35]}

with open('data.star', 'w') as _file:
    json.dump(data, _file)
