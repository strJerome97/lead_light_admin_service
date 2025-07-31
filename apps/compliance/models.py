from django.db import models

# Create your models here.
class ComplianceLocalizations(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    affiliated_partner = models.ForeignKey('partner.PartnerDetails', on_delete=models.SET_NULL, blank=True, null=True, related_name='compliance_localizations')
    website = models.URLField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compliance Localization"
        verbose_name_plural = "Compliance Localizations"
        ordering = ['name']
        db_table = 'compliance_localizations'

    def __str__(self):
        return self.name
    
