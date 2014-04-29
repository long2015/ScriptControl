
def on_help(list_data):
    result = ''

    for i in range(len(list_data)):
        result += '%s  ' % list_data[i]
        if i == 6 or i == 13 or i == 20:
            result += '\n'

    result += '\n'
    return result
