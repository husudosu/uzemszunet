import re
from datetime import datetime, date

DOTNET_JSON_DATE = re.compile(r'/Date\((\d*)\)/')


def order_list(uzemszunetek):
    """
    Rendezi az üzemszünetek listáját dátum és település szerint.
    """
    ret = {}
    for item in uzemszunetek:
        ret.setdefault(item.get("datum_tol").strftime("%Y.%m.%d"), {}).setdefault(
            item.get("telepules"), []).append(item)
    return ret


def convert_dotnet_date(datum):
    """
    Átkonvertál egy .NET json dátumot.
    Jelen pillanatban a timezone offset nem támogatott.
    :param datum: Dátum .NET formában
    """
    try:
        res = DOTNET_JSON_DATE.match(datum)
        return datetime.fromtimestamp(int(res[1]) / 1000.0)
    except Exception:
        return None


def encode_json(o):
    if isinstance(o, (date, datetime)):
        return o.strftime('%Y.%m.%d %H:%M:%S')
