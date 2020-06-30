import json


def open_file(file):
    with open('json/' + file + '.json') as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


def write_file(data, file):
    with open('json/' + file + '.json', 'w') as outfile:
        json.dump(data, outfile)
