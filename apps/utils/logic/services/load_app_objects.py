from apps.utils.common.logger import logger
from django.apps import apps
from apps.access.models import AccessObjects
import json

logger = logger.PortalLogger("LOAD_APP_OBJECTS")

class LoadAppObjects:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body) if request.body else {}

    def execute(self):
        """
        This method is used to execute the loading of app objects.
        It retrieves the app objects from the Django apps registry and saves them to the database.
        It can be called from the API endpoint or from other services.
        :return: A dictionary containing the status of the operation.
        If successful, it returns a success message with the number of objects saved.
        If no objects are found, it returns a 404 error with a message.
        If an error occurs while saving, it returns a 500 error with the error message.
        Usage:
        load_app_objects = LoadAppObjects(request)
        result = load_app_objects.execute()
        :raises Exception: If an error occurs while loading or saving app objects.
        """
        module = "admin_portal"  # Default module name
        app_objects = self._get_objects()
        logger.info(f"App objects loaded: {app_objects}")
        if not app_objects:
            return {"code": 404, "status": "error", "message": "No app objects found", "data": []}
        # Save the app objects to the database
        result = self._save_objects_to_db(app_objects, module)
        return result

    def execute_from_external(self):
        """
        This method is used to execute the loading of app objects from an external source.
        It can be called from other services or scripts.
        """
        module = self.body.get("module", "default")
        app_objects = self.body.get("app_objects", [])
        if not app_objects or len(app_objects) == 0:
            return {"code": 404, "status": "error", "message": "No app objects found", "data": []}
        result = self._save_objects_to_db(app_objects, module)
        return result
    
    def _save_objects_to_db(self, objects, module=None):
        """
        Save the app objects to the database.
        :param objects: A dictionary containing the app objects to be saved.
        The keys are the app labels and the values are lists of model names.
        :return: A dictionary containing the status of the operation.
        If successful, it returns a success message with the number of objects saved.
        If no objects are saved, it returns a 404 error with a message.
        If an error occurs while saving, it returns a 500 error with the error message.
        """
        try:
            output = []
            for key, value in objects.items():
                # Assuming 'AccessObjects' is the model to save the app objects
                for obj in value:
                    data = {
                        'name': f"{key}.{obj}",
                        'application': key,
                        'model_name': obj,
                        'module': module if module else 'default'
                    }
                    result = AccessObjects.objects.update_or_create(
                        name=data['name'],
                        defaults=data
                    )
                    output.append(str(result))
            if len(output) == 0:
                logger.error("No objects were saved to the database.")
                return {"status": "error", "code": 404, "message": "No objects were saved.", "data": []}
            else:
                logger.info(f"Successfully saved {len(output)} objects to the database.")
                return {"status": "success", "code": 200, "message": f"Saved {len(output)} objects.", "data": output}
        except Exception as e:
            logger.error(f"Error saving objects to database: {str(e)}")
            return {"status": "error", "code": 500, "message": str(e), "data": []}

    def _get_objects(self):
        """
        Get a list of all app objects in the project.
        :return: A dictionary containing the app objects.
        The keys are the app labels and the values are lists of model names.
        If an error occurs while retrieving the app objects, it returns False.
        model_map structure:
        {
            "app_label": ["Model1", "Model2", ...],
            ...
        }
        """
        try:
            model_map = {}
            for app_config in apps.get_app_configs():
                app_label = app_config.label
                models = app_config.get_models()
                model_map[app_label] = [model.__name__ for model in models]

            logger.info(f"Loaded app objects: {model_map}")
            return model_map
        except Exception as e:
            logger.error(f"Error loading app objects: {str(e)}")
            return False