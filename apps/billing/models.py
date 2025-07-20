from django.db import models

# Create your models here.
class CompanyBilling(models.Model):
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='billing_details')
    billing_address = models.TextField(blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('other', 'Other')
    ], default='credit_card')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Billing"
        verbose_name_plural = "Company Billings"
        ordering = ['company__name']
        db_table = 'billing_company'

    def __str__(self):
        return f"{self.company.name} - Billing Details"
