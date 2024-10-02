import json
import inspect
from wowapi.WoWapi import WoWAPI
from dotenv import load_dotenv
from pylog import get_logger
import logging

load_dotenv()

api_logger = get_logger(
    "wowapi.WoWapi",
    console=False,
    file=False,
    mongo_uri="mongodb://localhost:27018",
    mongo_db_name="logs",
    mongo_collection_name="testing",
    log_level=logging.DEBUG,
    app_name="WowAPI Test Script",
)

script_logger = get_logger(
    "api-test",
    console=True,
    file=False,
    mongo_uri="mongodb://localhost:27018",
    mongo_db_name="logs",
    mongo_collection_name="testing",
    log_level=logging.DEBUG,
    app_name="WowAPI Test Script",
)

def print_json(data):
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))

def test_endpoint(api, method_name, *args):
    """Test a specific endpoint and print the result."""
    method = getattr(api, method_name, None)
    if not method:
        print(f"Error: Method '{method_name}' not found in WoWAPI class.")
        return

    try:
        result = method(*args)
        print(f"\nResult from {method_name}:")
        print_json(result)
    except Exception as e:
        print(f"Error occurred while calling {method_name}: {str(e)}")

def get_api_methods():
    """Get all public methods from the WoWAPI class."""
    return [name for name, func in inspect.getmembers(WoWAPI, predicate=inspect.isfunction)
            if not name.startswith('_')]

def prompt_for_args(method):
    """Prompt the user for arguments based on the method's signature."""
    sig = inspect.signature(method)
    args = []
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
        if param.default == inspect.Parameter.empty:
            value = input(f"Enter {param_name}: ")
            args.append(int(value) if param.annotation == int else value)
        else:
            value = input(f"Enter {param_name} (default {param.default}): ")
            if value:
                args.append(int(value) if param.annotation == int else value)
            else:
                args.append(param.default)
    return args

def main():
    api = WoWAPI()
    methods = get_api_methods()

    while True:
        print("\nAvailable methods:")
        for i, method in enumerate(methods, 1):
            print(f"{i}. {method}")
        print("0. Exit")

        choice = input("Enter the number of the method you want to test (0 to exit): ")

        if choice == '0':
            break

        try:
            method_index = int(choice) - 1
            if 0 <= method_index < len(methods):
                method_name = methods[method_index]
                method = getattr(api, method_name)
                args = prompt_for_args(method)
                test_endpoint(api, method_name, *args)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")



if __name__ == "__main__":
    main()
