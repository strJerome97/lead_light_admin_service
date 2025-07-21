from django.db import models

# Create your models here.
class AdministratorUserDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrator User Details"
        verbose_name_plural = "Administrator User Details"
        ordering = ['name']
        db_table = 'admin_portal_administrator_user_details'

    # def __str__(self):
    #     return self.user.username

class AdministratorLoginCredential(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_password_change = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Administrator Login Credential"
        verbose_name_plural = "Administrator Login Credentials"
        ordering = ['-created_at']
        db_table = 'admin_portal_administrator_login_credential'

    # def __str__(self):
    #     return f"{self.username} - {self.user.user.username}"
    
class AdministratorLoginHistory(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrator Login History"
        verbose_name_plural = "Administrator Login Histories"
        ordering = ['-login_time']
        db_table = 'admin_portal_administrator_login_history'

    # def __str__(self):
    #     return f"{self.user.user.username} - {self.login_time}"

class AdministratorRecoveryEmail(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Administrator Recovery Email"
        verbose_name_plural = "Administrator Recovery Emails"
        ordering = ['-is_primary']
        db_table = 'admin_portal_administrator_recovery_email'

    # def __str__(self):
    #     return f"{self.user.user.username} - {self.email}"

class AdministratorRecoveryPhone(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Administrator Recovery Phone"
        verbose_name_plural = "Administrator Recovery Phones"
        ordering = ['-is_primary']
        db_table = 'admin_portal_administrator_recovery_phone'

    # def __str__(self):
    #     return f"{self.user.user.username} - {self.phone_number}"
