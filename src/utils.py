import argparse
import requests
import json

# Check command line arguments are valid so they wont cause errors in the program
def validate_arguments(API_id, file_path):
    test_request = requests.get(f"http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/{API_id}/bristol/")
    if test_request.status_code == 404:
        print("Please enter valid API ID..\n")
        exit()
    try:
        test_open = open(file_path, "w")
        test_open.close()
    except IOError:
        print("Please enter a valid file path..\n")
        exit(0)

# Parse arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Answer some weather questions.")
    parser.add_argument("API_id", type=str, help="API ID number.")
    parser.add_argument("file_path", type=str, help="JSON response save location.")
    args = parser.parse_args()
    return args.API_id, args.file_path

# Save answers to the questions to a JSON file
def answers_to_json_file(answers, file_path):
    answers_dict = {"answers": []}
    for answer in answers:
        answers_dict["answers"].append(answer)
    json_obj = json.dumps(answers_dict)
    with open(file_path, "w") as text_file:
        text_file.write(json_obj)
    text_file.close()
