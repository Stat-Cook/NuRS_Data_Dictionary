from importlib.resources import read_text

TEMPLATE = read_text("nurs_data_reference", "template.txt")

def reference_to_markdown(**kwargs):
    kwargs["Common_1"] = "|".join(map(str, kwargs.get("Common 1")))
    kwargs["Common_2"] = "|".join(map(str, kwargs.get("Common 2")))
    kwargs["Common_3"] = "|".join(map(str, kwargs.get("Common 3")))
    return TEMPLATE.format(
        **kwargs
    )
