from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: True


class PaymentsCapitalAssets(TimeStampedModel):

    fixed_accounts = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    intangible_assets = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    machinery = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)

    def __str__(self):
        return self.id


class TransfersSubsidies(TimeStampedModel):

    dept_agencies = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    social_benefits = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    non_profit_inst = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)

    def __str__(self):
        return self.id


class CurrentPayments(TimeStampedModel):

    compensation_employees = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
