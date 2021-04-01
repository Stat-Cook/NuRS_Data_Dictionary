
with open("nurs_data_reference/template.txt", "r") as f:
    TEMPLATE = f.read()

def reference_to_markdown(**kwargs):
    kwargs["Common_1"] = "|".join(kwargs.get("Common 1"))
    kwargs["Common_2"] = "|".join(kwargs.get("Common 2"))
    kwargs["Common_3"] = "|".join(kwargs.get("Common 3"))
    return TEMPLATE.format(
        **kwargs
    )


