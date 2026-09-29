PLUGIN={"id":"json-parser","name":"Basic Input Parser","kind":"parser","description":"Normalizes text input without model calls"}
def parse_input(value):
    if not isinstance(value,str): value=str(value)
    return value.strip()[:12000]
