from django.db import models

# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['user__username']
        db_table = 'admin_portal_user_profile'

    def __str__(self):
        return self.user.username

class Credential(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Credential"
        verbose_name_plural = "Credentials"
        ordering = ['-created_at']
        db_table = 'admin_portal_credential'
    
    def __str__(self):
        return f"{self.username} - {self.user.user.username}"

class LoginHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Login History"
        verbose_name_plural = "Login Histories"
        ordering = ['-login_time']
        db_table = 'admin_portal_login_history'

    def __str__(self):
        return f"{self.user.user.username} - {self.login_time}"

class RecoveryEmail(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Recovery Email"
        verbose_name_plural = "Recovery Emails"
        ordering = ['-is_primary']
        db_table = 'admin_portal_recovery_email'

    def __str__(self):
        return f"{self.user.user.username} - {self.email}"

class RecoveryPhone(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Recovery Phone"
        verbose_name_plural = "Recovery Phones"
        ordering = ['-is_primary']
        db_table = 'admin_portal_recovery_phone'

    def __str__(self):
        return f"{self.user.user.username} - {self.phone_number}"

class MultiFactorAuth(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    method = models.CharField(max_length=50, choices=[('SMS', 'SMS'), ('Email', 'Email'), ('Authenticator App', 'Authenticator App')], default='SMS')

    class Meta:
        verbose_name = "Multi-Factor Authentication"
        verbose_name_plural = "Multi-Factor Authentications"
        db_table = 'admin_portal_multi_factor_auth'

    def __str__(self):
        return f"{self.user.user.username} - {self.method} MFA"

class AdminActivityLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admin Activity Log"
        verbose_name_plural = "Admin Activity Logs"
        ordering = ['-timestamp']
        db_table = 'admin_portal_admin_activity_log'

    def __str__(self):
        return f"{self.user.user.username} - {self.action} at {self.timestamp}"

class AdminLoginHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Admin Login History"
        verbose_name_plural = "Admin Login Histories"
        ordering = ['-login_time']
        db_table = 'admin_portal_admin_login_history'

    def __str__(self):
        return f"{self.user.user.username} - {self.login_time}"

class AdminFlaggedIP(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admin Flagged IP"
        verbose_name_plural = "Admin Flagged IPs"
        ordering = ['-flagged_at']
        db_table = 'admin_portal_admin_flagged_ip'

    def __str__(self):
        return f"Flagged IP for {self.user.user.username} - {self.ip_address}"