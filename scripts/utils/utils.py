import json


def print_json(value):
     print(json.dumps(value, indent=4, ensure_ascii=False))