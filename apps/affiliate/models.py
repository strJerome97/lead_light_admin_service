from django.db import models

# Create your models here.
class AffiliateLink(models.Model):
    partner = models.ForeignKey('partner.PartnerDetails', on_delete=models.CASCADE, related_name='affiliate_links')
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Affiliate Link"
        verbose_name_plural = "Affiliate Links"
        ordering = ['created_at']
        db_table = 'affiliate_links'

    def __str__(self):
        return f"{self.partner.name} - {self.link}"

class AffiliateCommission(models.Model):
    affiliate_link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Affiliate Commission"
        verbose_name_plural = "Affiliate Commissions"
        ordering = ['-date_earned']
        db_table = 'affiliate_commissions'

    def __str__(self):
        return f"{self.affiliate_link.partner.name} - {self.amount} on {self.date_earned}"

class AffiliatePayment(models.Model):
    commission = models.ForeignKey(AffiliateCommission, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Affiliate Payment"
        verbose_name_plural = "Affiliate Payments"
        ordering = ['-payment_date']
        db_table = 'affiliate_payments'

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.commission.affiliate_link.partner.name} on {self.payment_date}"

