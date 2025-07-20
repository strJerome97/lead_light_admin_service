from django.db import models

# Create your models here.
class PartnerDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Partner Detail"
        verbose_name_plural = "Partner Details"
        ordering = ['name']
        db_table = 'partner_details'

    def __str__(self):
        return self.name


class PartnerAdminCredential(models.Model):
    partner = models.ForeignKey(PartnerDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Partner Admin Credential"
        verbose_name_plural = "Partner Admin Credentials"
        ordering = ['-created_at']
        db_table = 'partner_admin_credential'

    def __str__(self):
        return f"{self.username} - {self.partner.name}"


class PartnerLoginHistory(models.Model):
    partner = models.ForeignKey(PartnerDetails, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Partner Login History"
        verbose_name_plural = "Partner Login Histories"
        ordering = ['-login_time']
        db_table = 'partner_login_history'

    def __str__(self):
        return f"{self.partner.name} - {self.login_time}"


class PartnerRecoveryEmail(models.Model):
    partner = models.ForeignKey(PartnerDetails, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Partner Recovery Email"
        verbose_name_plural = "Partner Recovery Emails"
        ordering = ['-is_primary']
        db_table = 'partner_recovery_email'

    def __str__(self):
        return f"{self.partner.name} - {self.email}"


class PartnerRecoveryPhone(models.Model):
    partner = models.ForeignKey(PartnerDetails, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Partner Recovery Phone"
        verbose_name_plural = "Partner Recovery Phones"
        ordering = ['-is_primary']
        db_table = 'partner_recovery_phone'

    def __str__(self):
        return f"{self.partner.name} - {self.phone_number}"