from django.db import models

# Create your models here.
class AccessGroups(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    unique_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='access_groups', null=True, blank=True)

    class Meta:
        verbose_name = "Access Group"
        verbose_name_plural = "Access Groups"
        db_table = 'access_groups'

    def __str__(self):
        return self.name

class AccessObjects(models.Model):
    name = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=100, blank=True, null=True)  # Optional field for module name
    application = models.CharField(max_length=100, blank=True, null=True)  # Optional field for application name
    model_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Access Object"
        verbose_name_plural = "Access Objects"
        db_table = 'access_objects'

    def __str__(self):
        return self.name

class AccessPermissions(models.Model):
    group = models.ForeignKey(AccessGroups, on_delete=models.CASCADE, related_name='permissions')
    object = models.ForeignKey(AccessObjects, on_delete=models.CASCADE, related_name='permissions')
    can_view = models.BooleanField(default=False) # can view and export data
    can_create = models.BooleanField(default=False) # can create and import data
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_archive = models.BooleanField(default=False)
    can_restore = models.BooleanField(default=False)
    filter_query = models.TextField(blank=True, null=True)  # Optional field for filter query
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Access Permission"
        verbose_name_plural = "Access Permissions"
        db_table = 'access_permissions'
        unique_together = ('group', 'object')

    def __str__(self):
        return f"{self.group.name} - {self.object.name}"

class UserGroupAccess(models.Model):
    user = models.ForeignKey('user.UserDetails', on_delete=models.CASCADE, related_name='group_access', null=True, blank=True)
    admin = models.ForeignKey('administration.AdministratorUserDetails', on_delete=models.CASCADE, related_name='group_access', null=True, blank=True)
    unique_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    group = models.ForeignKey(AccessGroups, on_delete=models.CASCADE, related_name='user_access')
    group_inherit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='inherited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='user_group_access', null=True, blank=True)

    class Meta:
        verbose_name = "User Group Access"
        verbose_name_plural = "User Group Accesses"
        db_table = 'access_user_group'
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.email} - {self.group.name}"