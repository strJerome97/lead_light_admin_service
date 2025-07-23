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
        db_table = 'administrator_user_details'

    def __str__(self):
        return self.name

class AdministratorLoginCredential(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    required_password_change = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_sso_enabled = models.BooleanField(default=False)
    is_mfa_enabled = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Administrator Login Credential"
        verbose_name_plural = "Administrator Login Credentials"
        ordering = ['-created_at']
        db_table = 'administrator_login_credential'

    def __str__(self):
        return f"{self.username} - {self.admin.name}"

class AdministratorLoginHistory(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrator Login History"
        verbose_name_plural = "Administrator Login Histories"
        ordering = ['-login_time']
        db_table = 'administrator_login_history'

    def __str__(self):
        return f"{self.admin.name} - {self.login_time}"

class AdministratorRecoveryEmail(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Administrator Recovery Email"
        verbose_name_plural = "Administrator Recovery Emails"
        ordering = ['-is_primary']
        db_table = 'administrator_recovery_email'

    def __str__(self):
        return f"{self.admin.name} - {self.email}"

class AdministratorRecoveryPhone(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Administrator Recovery Phone"
        verbose_name_plural = "Administrator Recovery Phones"
        ordering = ['-is_primary']
        db_table = 'administrator_recovery_phone'

    def __str__(self):
        return f"{self.admin.name} - {self.phone_number}"


class AdministratorFlaggedIP(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    reason = models.TextField(blank=True, null=True)
    is_flagged = models.BooleanField(default=True)
    flagged_at = models.DateTimeField(auto_now_add=True)
    flagged_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrator Flagged IP"
        verbose_name_plural = "Administrator Flagged IPs"
        ordering = ['-flagged_at']
        db_table = 'administrator_flagged_ip'


class AdministratorFlaggedEmail(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    email = models.EmailField()
    reason = models.TextField(blank=True, null=True)
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Administrator Flagged Email"
        verbose_name_plural = "Administrator Flagged Emails"
        ordering = ['-flagged_at']
        db_table = 'administrator_flagged_email'

    def __str__(self):
        return f"{self.admin.email} - {self.email}"


class AdministratorFlaggedPhone(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    reason = models.TextField(blank=True, null=True)
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Administrator Flagged Phone"
        verbose_name_plural = "Administrator Flagged Phones"
        ordering = ['-flagged_at']
        db_table = 'administrator_flagged_phone'

    def __str__(self):
        return f"{self.admin.email} - {self.phone_number}"

class AdministratorOneTimePassword(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Administrator One Time Password"
        verbose_name_plural = "Administrator One Time Passwords"
        ordering = ['-created_at']
        db_table = 'administrator_one_time_password'

    def __str__(self):
        return f"OTP for {self.admin.name} - {self.otp}"

class AdministratorLoginAttempt(models.Model):
    admin = models.ForeignKey(AdministratorUserDetails, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrator Login Attempt"
        verbose_name_plural = "Administrator Login Attempts"
        ordering = ['-attempt_time']
        db_table = 'administrator_login_attempt'

    def __str__(self):
        return f"{self.admin.name} - {'Success' if self.success else 'Failed'} at {self.attempt_time}"
    