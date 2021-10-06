import json
# Open the test JSON files and load them as JSON objects
def load_json_file(file_path):
    with open(file_path) as f:
        json_item = json.loads(f.read())
    f.close()
    return json_item
