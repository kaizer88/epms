from django.db import models

from strategy.models import Subprogramme, Objective, StrategicOutput, KeyPerformanceIndicator, AnnualTarget


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class QuarterlyTarget(TimeStampedModel):

    uuid = models.UUIDField()
    subprogramme = models.ForeignKey(Subprogramme, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    output = models.ForeignKey(StrategicOutput, on_delete=models.CASCADE)
    kpi = models.ForeignKey(KeyPerformanceIndicator, on_delete=models.CASCADE)
    annual_target = models.ForeignKey(AnnualTarget, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    baseline = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)
    quarter = models.SmallIntegerField(null=True)

    def __str__(self):
        return "{} to {}".format(self.start_date, self.end_date)


class Risk(TimeStampedModel):

    quarterly_target = models.ManyToManyField(QuarterlyTarget)
    description = models.TextField()
