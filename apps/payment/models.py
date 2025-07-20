from django.db import models

# Create your models here.
class PaymentCompany(models.Model):
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='payment_details')
    billing = models.ForeignKey('billing.CompanyBilling', on_delete=models.CASCADE, related_name='payment_details')
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('other', 'Other')
    ], default='credit_card')
    billing_address = models.TextField(blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Company"
        verbose_name_plural = "Payment Companies"
        ordering = ['company__name']
        db_table = 'payment_company'

    def __str__(self):
        return f"{self.company.name} - Payment Details"


class PaymentTransaction(models.Model):
    payment = models.ForeignKey(PaymentCompany, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen')
    ], default='USD')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"
        ordering = ['-created_at']
        db_table = 'payment_transaction'

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} {self.currency}"