from apps.utils.common.logger import logger
import json
import glob
import os
from django.apps import apps

logger = logger.PortalLogger("DATA_LOADER")

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
        This method will resolve ForeignKey fields by fetching the related model instance using the provided ID.
        The method will return a list of saved objects.
        If an error occurs while saving, it will print the error message and continue with the next entry.
        :param data: List of JSON file paths containing the data to be saved.
        :return: List of saved objects.
        """
        try:
            if len(data) == 0:
                logger.error("No data files found to process.")
                # Construct an empty result list if no data files are found
                return {
                    "code": 404,
                    "status": "error", 
                    "message": "No data files found", 
                    "data": []
                }

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
                            logger.info(f"Creating {object_path} with data: {obj_data}")
                            app_label, model_name = object_path.split(".")
                            Model = apps.get_model(app_label, model_name)
                            if not Model:
                                print(f"Model not found for {object_path}")
                                continue
                            if action == "create":
                                # Handle create or upsert by ID
                                obj_id = obj_data.pop("id", None)
                                # Resolve ForeignKey fields
                                for field, value in list(obj_data.items()):
                                    try:
                                        model_field = Model._meta.get_field(field)
                                        if model_field.is_relation and model_field.many_to_one:
                                            obj_data[field] = model_field.related_model.objects.get(pk=value)
                                    except Exception:
                                        pass  # Not a relation or invalid field, skip

                                if obj_id and Model.objects.filter(pk=obj_id).exists():
                                    obj = Model.objects.get(pk=obj_id)
                                    for field, value in obj_data.items():
                                        setattr(obj, field, value)
                                    obj.save()
                                    logger.info(f"Successfully updated {object_path} with data: {obj_data}")
                                else:
                                    if obj_id:
                                        obj = Model.objects.create(id=obj_id, **obj_data)
                                    else:
                                        obj = Model.objects.create(**obj_data)
                                    logger.info(f"Successfully created {object_path} with data: {obj_data}")
                                results.append({"object": object_path, "id": obj.id})
                            elif action == "update":
                                # Add more actions as needed
                                obj_id = obj_data.pop("id", None)
                                if obj_id:
                                    obj = Model.objects.get(pk=obj_id)
                                    for field, value in obj_data.items():
                                        setattr(obj, field, value)
                                    obj.save()
                                    results.append({"object": object_path, "id": obj.id})
                                    logger.info(f"Successfully updated {object_path} with data: {obj_data}")
                                else:
                                    results.append({"object": object_path, "id": None})
                                    logger.error(f"ID not provided for update action on {object_path}")
                        except Exception as e:
                            print(f"Error saving {object_path}: {e}")
                            logger.error(f"Error saving {object_path}: {e}")
            # Construct the final results
            return {
                "code": 200,
                "status": "success",
                "message": "Data loaded successfully",
                "data": results
            }
        except Exception as e:
            logger.error(f"Error saving data to database: {e}")
            # Construct an empty result list if an error occurs
            return {
                "code": 500,
                "status": "error",
                "message": "Error saving data to database",
                "data": []
            }
    
    def _get_data_file(self):
        """
        Get the first JSON data file from the specified app's data directory.
        If no app is specified, it will look for the first JSON file in any app's data directory.
        :return: List of JSON file paths.
        :raises FileNotFoundError: If no JSON data files are found in the specified path
        """
        try:
            if self.app:
                data_dir = os.path.join('apps', self.app, 'data')
                pattern = os.path.join(data_dir, '*.json')
            else:
                pattern = os.path.join(self.file_path, '*', 'data', '*.json')
            print(f"Searching for JSON files in: {pattern}")
            files = glob.glob(pattern)

            if not files:
                raise FileNotFoundError("No JSON data files found in the specified path.")

            return files  # Return the list of JSON file paths
        except Exception as e:
            logger.error(f"Error getting data files: {e}")
            return []
        