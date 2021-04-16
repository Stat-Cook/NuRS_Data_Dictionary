"""

"""

def iterable_to_string(iterable):
    str_iter = map(str, iterable)
    return "\n".join(str_iter)


def string_to_iterable(string, iterable_type=list):
    iterable = "\n".split(string)
    return iterable_type(iterable)
