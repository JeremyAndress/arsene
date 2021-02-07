from json import dumps


def set_data(data):
    data_convert = {
        'type': type(data).__name__,
        'data': None
    }
    if (
        isinstance(data, list) or isinstance(data, dict) or
        isinstance(data, tuple)
    ):
        data_convert['data'] = dumps(data, default=str)
    elif (
        isinstance(data, str) or isinstance(data, int) or
        isinstance(data, float) or isinstance(data, bytes)
    ):
        data_convert['data'] = data
    return dumps(data_convert)
