from django.db import models

# Create your models here.
class CompanyDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    affiliated_partner = models.ForeignKey('partner.PartnerDetails', on_delete=models.SET_NULL, blank=True, null=True, related_name='companies')
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
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
    