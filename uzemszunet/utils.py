
def order_list(uzemszunetek):
    """
    Rendezi az üzemszünetek listáját dátum és település szerint.
    """
    ret = {}
    for item in uzemszunetek:
        ret.setdefault(item.get("datum"), {}).setdefault(
            item.get("telepules"), []).append(item)
    return ret
