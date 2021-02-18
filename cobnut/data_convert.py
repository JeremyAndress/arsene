from json import dumps
from datetime import date, datetime


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def object_hook(obj):
    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return datetime.fromisoformat(_isoformat)
    return obj


def set_data(data, *, serializable=json_serial):
    data_convert = {
        'type': type(data).__name__,
        'data': None
    }
    if (
        isinstance(data, list) or isinstance(data, dict) or
        isinstance(data, tuple)
    ):
        data_convert['data'] = dumps(data, default=serializable)
    elif (
        isinstance(data, str) or isinstance(data, int) or
        isinstance(data, float) or isinstance(data, bytes)
    ):
        data_convert['data'] = data
    return dumps(data_convert, default=serializable)
