'''
    Basic .json file (structure) handling.
    Reference Document: https://docs.python.org/3/library/json.html
    To Do: implement stamping via https://pypi.org/project/jwt/
'''

import json

# plain english string -> json converter.
def json_load_string(string: str):
    value: dict = json.loads(string)
    return value

def json_dump_string(data):
    return json.dumps(data)