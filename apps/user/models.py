from django.db import models

# Create your models here.
class UserDetails(models.Model):
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"
        # ordering = ['username']
        db_table = 'user_details'

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        db_table = 'user_profile'

    def __str__(self):
        return self.user.email

class UserCredential(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='credentials')
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
        verbose_name = "User Credential"
        verbose_name_plural = "User Credentials"
        ordering = ['-created_at']
        db_table = 'user_credential'

    def __str__(self):
        return f"{self.username} - {self.user.email}"

class UserLoginHistory(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='login_histories')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "User Login History"
        verbose_name_plural = "User Login Histories"
        ordering = ['-login_time']
        db_table = 'user_login_history'

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"

class UserRecoveryEmail(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='recovery_emails')
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Recovery Email"
        verbose_name_plural = "User Recovery Emails"
        ordering = ['-is_primary']
        db_table = 'user_recovery_email'

    def __str__(self):
        return f"{self.user.email} - {self.email}"


class UserRecoveryPhone(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='recovery_phones')
    phone_number = models.CharField(max_length=15, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Recovery Phone"
        verbose_name_plural = "User Recovery Phones"
        ordering = ['-is_primary']
        db_table = 'user_recovery_phone'

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"

class UserFlaggedIP(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='flagged_ips')
    ip_address = models.GenericIPAddressField()
    reason = models.TextField(blank=True, null=True)
    is_flagged = models.BooleanField(default=True)
    flagged_at = models.DateTimeField(auto_now_add=True)
    flagged_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "User Flagged IP"
        verbose_name_plural = "User Flagged IPs"
        db_table = 'user_flagged_ip'

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"

class UserFlaggedEmail(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='flagged_emails')
    email = models.EmailField()
    reason = models.TextField(blank=True, null=True)
    is_flagged = models.BooleanField(default=True)
    flagged_at = models.DateTimeField(auto_now_add=True)
    flagged_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "User Flagged Email"
        verbose_name_plural = "User Flagged Emails"
        db_table = 'user_flagged_email'

    def __str__(self):
        return f"{self.user.email} - {self.email}"
    
class UserFlaggedPhone(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='flagged_phones')
    phone_number = models.CharField(max_length=15)
    reason = models.TextField(blank=True, null=True)
    is_flagged = models.BooleanField(default=True)
    flagged_at = models.DateTimeField(auto_now_add=True)
    flagged_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "User Flagged Phone"
        verbose_name_plural = "User Flagged Phones"
        db_table = 'user_flagged_phone'

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"

class UserOneTimePassword(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "User One Time Password"
        verbose_name_plural = "User One Time Passwords"
        db_table = 'user_one_time_password'

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

class UserLoginHistory(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='login_histories')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "User Login History"
        verbose_name_plural = "User Login Histories"
        db_table = 'user_login_history'

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"

class UserLoginAttempt(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='login_attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Login Attempt"
        verbose_name_plural = "User Login Attempts"
        db_table = 'user_login_attempt'

    def __str__(self):
        return f"{self.user.email} - {'Success' if self.success else 'Failed'} - {self.attempt_time}"