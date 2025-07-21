
import json
import glob
import os
from django.apps import apps

class DataLoader:
    """
    A class to get JSON data from data directories of every app in the project and then save it to the database.
    The data directory is expected to be structured as follows:
    apps/
        <app_name>/
            data/
                <data_file>.json
    The class will look for the first JSON file in the data directory of the specified app.
    If no app is specified, it will look for the first JSON file in the data directory of any app.
    If no data files are found, it will raise a FileNotFoundError.
    Usage:
        data_loader = DataLoader(file_path='apps/utils/services/data', app_name='your_app_name')
        result = data_loader.execute()
    """
    def __init__(self, file_path, app_name):
        """
        Initialize the DataLoader with the file path and app name.
        :param file_path: The path to the directory containing the data files.
        :param app_name: The name of the app to load data for.
        If no app is specified, it will look for data files in any app's data directory.
        :raises FileNotFoundError: If no JSON data files are found in the specified path.
        """
        self.file_path = file_path
        self.app = app_name

    def execute(self):
        """
        Execute the data loading process.
        """
        data = self._get_data_file()
        result = self._save_data_to_db(data)
        return result
    
    def _save_data_to_db(self, data):
        """
        Save data to the database using Django ORM, resolving the model from the 'object' key.
        The 'object' key should be in the format 'app_label.model_name'.
        The 'action' key should specify the action to perform (e.g., 'create').
        The 'data' key should contain the data to be saved.
        The method will return a list of saved objects.
        If an error occurs while saving, it will print the error message and continue with the next
        entry.
        :param data: List of JSON file paths containing the data to be saved.
        :return: List of saved objects.
        """
        results = []
        for file_path in data:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                for entry in json_data:
                    object_path = entry.get("object")
                    action = entry.get("action")
                    obj_data = entry.get("data")
                    if not (object_path and action and obj_data):
                        continue
                    try:
                        app_label, model_name = object_path.split(".")
                        Model = apps.get_model(app_label, model_name)
                        if not Model:
                            print(f"Model not found for {object_path}")
                            continue
                        if action == "create":
                            obj = Model.objects.create(**obj_data)
                            results.append(obj)
                        # Add more actions as needed
                    except Exception as e:
                        print(f"Error saving {object_path}: {e}")
        return results
    
    def _get_data_file(self):
        """
        Get the first JSON data file from the specified app's data directory.
        If no app is specified, it will look for the first JSON file in any app's data directory.
        :return: List of JSON file paths.
        :raises FileNotFoundError: If no JSON data files are found in the specified path
        """
        if self.app:
            data_dir = os.path.join(self.file_path, self.app, 'data')
            pattern = os.path.join(data_dir, '*.json')
        else:
            pattern = os.path.join(self.file_path, '*', 'data', '*.json')

        files = glob.glob(pattern)

        if not files:
            raise FileNotFoundError("No JSON data files found in the specified path.")

        return files  # Return the list of JSON file paths
