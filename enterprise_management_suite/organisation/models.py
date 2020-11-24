from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='media/organisation/logos', null=True, blank=True)

    def __str__(self):
        return self.name


class FinancialYear(models.Model):
    org = models.ForeignKey(Organisation, null=True, blank=True, on_delete=models.CASCADE)
    financial_period_start = models.DateField()
    financial_period_end = models.DateField()
    year = models.CharField(max_length=4, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.financial_period_start, self.financial_period_end)


class Component(models.Model):

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    """
    Cluster /Department/ Division/branch/dept/cluster,
    """
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'


class Programme(models.Model):

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    index_no = models.CharField(max_length=5, blank=True, null=True)
    overview = models.TextField(null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubProgramme(models.Model):

    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    index_no = models.CharField(max_length=5, blank=True, null=True)
    purpose = models.TextField(null=True, blank=True)

