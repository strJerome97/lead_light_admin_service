from django.db import models

# Create your models here.
class CompanyDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    affiliated_partner = models.ForeignKey('partner.PartnerDetails', on_delete=models.SET_NULL, blank=True, null=True, related_name='companies')
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Detail"
        verbose_name_plural = "Company Details"
        ordering = ['name']
        db_table = 'company_details'

    def __str__(self):
        return self.name

class CompanyAddress(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Company Address"
        verbose_name_plural = "Company Addresses"
        ordering = ['company', 'city']
        db_table = 'company_address'

    def __str__(self):
        return f"{self.company.name} - {self.city}"

class CompanyBankAccount(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Company Bank Account"
        verbose_name_plural = "Company Bank Accounts"
        ordering = ['company', 'bank_name']
        db_table = 'company_bank_account'

    def __str__(self):
        return f"{self.company.name} - {self.bank_name}"

class CompanyAPIKeys(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='api_keys')
    access_key = models.CharField(max_length=255, unique=True)
    secret_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    is_revoked = models.BooleanField(default=False)
    revoked_at = models.DateTimeField(blank=True, null=True)
    revoked_by = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Company API Key"
        verbose_name_plural = "Company API Keys"
        ordering = ['-created_at']
        db_table = 'company_api_keys'
    
    def __str__(self):
        return f"{self.company.name} - {self.access_key}"