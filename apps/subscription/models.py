from django.db import models

# Create your models here.
class SubscriptionModulesList(models.Model):
    module_name = models.CharField(max_length=100, unique=True)
    per_user_price = models.DecimalField(max_digits=10, decimal_places=2)
    per_instance_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription Module"
        verbose_name_plural = "Subscription Modules"
        ordering = ['module_name']
        db_table = 'subscription_modules_list'

    def __str__(self):
        return self.module_name

class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    modules = models.ManyToManyField(SubscriptionModulesList, blank=True, related_name='plans')
    max_users = models.PositiveIntegerField(default=0)
    duration_months = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
        ordering = ['plan_name']
        db_table = 'subscription_plan'

    def __str__(self):
        return self.plan_name

class SubscriptionCompany(models.Model):
    company = models.ForeignKey('company.CompanyDetails', on_delete=models.CASCADE, related_name='subscriptions')
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='companies')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription Company"
        verbose_name_plural = "Subscription Companies"
        ordering = ['company_name']
        db_table = 'subscription_company'

    def __str__(self):
        return self.company_name
