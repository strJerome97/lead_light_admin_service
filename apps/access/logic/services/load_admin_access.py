from apps.access.models import AccessGroups, AccessPermissions, AccessObjects, UserGroupAccess
from apps.administration.models import AdministratorUserDetails
import json

class LoadAdminAccess:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        """
        Execute the loading of admin access.
        This method creates or retrieves the admin access group, sets up default permissions,
        and creates the admin user group access if it does not already exist.
        Returns a dictionary with the following keys:
        - 'code': HTTP status code (int)
        - 'status': Status of the operation (str)
        - 'message': A message describing the result (str)
        - 'data': The data returned by the command (list or dict)
        If an error occurs, it will return a dictionary with an error message.
        Usage:
            load_admin_access = LoadAdminAccess(request)
            result = load_admin_access.execute()
        """
        # Create or get the admin access group
        admin_access_result = self._create_admin_access_groups_if_not_exists()
        if admin_access_result.get("status") != "success":
            return {"code": 500, "status": "error", "message": admin_access_result.get("message", "Unknown error"), "data": None}

        group_object = admin_access_result.get("data")
        # Create default access permissions if they do not exist
        permissions_result = self._create_access_permissions_if_not_exists(group_object)
        if permissions_result.get("status") != "success":
            return {"code": 500, "status": "error", "message": permissions_result.get("message", "Unknown error"), "data": None}

        # Create admin user group access if it does not exist
        user_group_result = self._create_admin_user_group_access_if_not_exists(group_object)
        if user_group_result.get("status") != "success":
            return {"code": 500, "status": "error", "message": user_group_result.get("message", "Unknown error"), "data": None}

        return {
            "code": 201, 
            "status": "success", 
            "message": user_group_result.get("message", "Admin access setup completed successfully"),
            "data": { "group_id": group_object.id }
        }

    def _create_admin_user_group_access_if_not_exists(self, group_object):
        try:
            # Logic to create admin user group access if it does not exist
            # This is a placeholder for the actual implementation
            admin_id = self.body.get("admin_id")
            if not admin_id:
                return {"code": 400, "status": "error", "message": "Admin ID is required"}
            admin_object_instance = AdministratorUserDetails.objects.filter(id=admin_id).first()
            data = {
                "unique_id": "super_admin_group_access",
                "admin": admin_object_instance,
                "group": group_object,
            }
            if admin_object_instance:
                if not UserGroupAccess.objects.filter(admin=admin_object_instance, group=group_object).exists():
                    result = UserGroupAccess.objects.create(**data)
                    return {"code": 201, "status": "success", "message": "Admin user group access created successfully", "data": {"id": result.id}}
                else:
                    return {"code": 200, "status": "success", "message": "Admin user group access already exists"}
        except Exception as e:
            print(f"Error creating admin user group access: {e}")
            return {"code": 500, "status": "error", "message": str(e)}

    def _create_access_permissions_if_not_exists(self, group_object):
        try:
            # Logic to create default access permissions if they do not exist
            # This is a placeholder for the actual implementation
            default_permissions = {
                "can_view": True,
                "can_create": True,
                "can_update": True,
                "can_delete": True,
                "can_archive": True,
                "can_restore": True
            }
            admin_portal_objects = AccessObjects.objects.filter(module='admin_portal')
            for obj in admin_portal_objects:
                check = AccessPermissions.objects.filter(object=obj)
                if not check.exists():
                    AccessPermissions.objects.create(group=group_object, object=obj, **default_permissions)
            return {"code": 201, "status": "success", "message": "Access permissions created successfully"}
        except Exception as e:
            print(f"Error creating access permissions: {e}")
            return {"code": 500, "status": "error", "message": str(e)}

    def _create_admin_access_groups_if_not_exists(self):
        try:
            data = {
                "name": "Portal Super Admin",
                "description": "Super Admin group with all permissions for the portal",
                "unique_id": "portal_super_admin"
            }
            check = AccessGroups.objects.filter(unique_id=data["unique_id"])
            result = {}
            if not check.exists():
                result = AccessGroups.objects.create(**data)
            else:
                result = check.first()
            return {"code": 200, "status": "success", "data": result}
        except Exception as e:
            print(f"Error creating admin access group: {e}")
            return {"code": 500, "status": "error", "message": str(e)}
