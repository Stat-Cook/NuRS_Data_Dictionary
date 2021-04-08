"""
Write markdown documents from a template and dictionary.
"""
from importlib.resources import read_text

TEMPLATE = read_text("nurs_data_reference", "template.txt")

def reference_to_markdown(template=TEMPLATE, **kwargs):
    """
    Combine a template string with key word arguments.
    Parameters
    ----------
    template: str
        A template for the markdown structure.
    kwargs: key word arguments

    Returns
    -------

    """
    kwargs["Common_1"] = "|".join(map(str, kwargs.get("Common 1")))
    kwargs["Common_2"] = "|".join(map(str, kwargs.get("Common 2")))
    kwargs["Common_3"] = "|".join(map(str, kwargs.get("Common 3")))
    return template.format(
        **kwargs
    )
