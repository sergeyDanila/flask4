import json
import os


def jsonsave(filename, part):
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
    else:
        data = []

    data.append(part)

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
