from django.db import models

# Create your models here.
class Authentication(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Authentication Token"
        verbose_name_plural = "Authentication Tokens"
        ordering = ['-created_at']
        db_table = 'authentication_token'

    def __str__(self):
        return f"Token for {self.user.username} - Expires at {self.expires_at}"

class UserSession(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        ordering = ['-last_activity']
        db_table = 'authentication_user_session'

    def __str__(self):
        return f"Session for {self.user.username} - Last activity at {self.last_activity}"

class PasswordResetRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=255, unique=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Password Reset Request"
        verbose_name_plural = "Password Reset Requests"
        ordering = ['-requested_at']
        db_table = 'authentication_password_reset_request'

    def __str__(self):
        return f"Reset request for {self.user.username} - Expires at {self.expires_at}"

class TwoFactorAuth(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    backup_codes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Two-Factor Authentication"
        verbose_name_plural = "Two-Factor Authentications"
        ordering = ['user__username']
        db_table = 'authentication_two_factor_auth'

    def __str__(self):
        return f"2FA for {self.user.username} - Enabled: {self.is_enabled}"

class LoginHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Login History"
        verbose_name_plural = "Login Histories"
        ordering = ['-login_time']
        db_table = 'authentication_login_history'

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class LoginAttempt(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"
        ordering = ['-attempt_time']
        db_table = 'authentication_login_attempt'

    def __str__(self):
        return f"{self.user.username} - {'Success' if self.success else 'Failed'} at {self.attempt_time}"

class FlaggedIP(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Flagged IP"
        verbose_name_plural = "Flagged IPs"
        ordering = ['-flagged_at']
        db_table = 'authentication_flagged_ip'

    def __str__(self):
        return f"Flagged IP for {self.user.username} - {self.ip_address}"

class FlaggedUser(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    reason = models.TextField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Flagged User"
        verbose_name_plural = "Flagged Users"
        ordering = ['-flagged_at']
        db_table = 'authentication_flagged_user'

    def __str__(self):
        return f"Flagged User: {self.user.username} - Reason: {self.reason}"