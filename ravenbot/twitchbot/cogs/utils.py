def contains(data, d, name):
    if name in data[d]:
        return True


def delete(data, d, name, file):
    if contains(data, d, name):
        data[d].pop(name)
        data.write(file, data)


def add_item(data, d, name, response, file):
    if str(response).isnumeric():
        data[d][name] = response
    else:
        data[d][name] = str(response)
    data.write(file, data)
