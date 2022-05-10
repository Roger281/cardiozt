import os
import json


def get_basename(path_file) -> dict:
    base_name = os.path.basename(path_file)
    return {"file_name": os.path.splitext(base_name)[0], "file_extension": os.path.splitext(base_name)[1]}


def dirname(file) -> str:
    return os.path.dirname(file)


def convert_obj_to_dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(convert_obj_to_dict(item))
        else:
            element = convert_obj_to_dict(val)
        result[key] = element
    #return json.loads(json.dumps(object_value, default=lambda o: o.__dict__))
    return result


def get_files_directory(path, limit=50):
    file_list = []
    if os.path.exists(path):
        for file in os.listdir(path)[:limit]:
            if file.endswith(".csv"):
                file_list.append(file)

    return file_list
