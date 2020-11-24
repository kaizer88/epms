import datetime

from django.db import models
from django.core.files.storage import FileSystemStorage
from organisation.models import Programme, Branch
from accounts.models import Employee

REVISIONS_MANDATES = FileSystemStorage(location='media/strategy/overview/rev_mandates')
RESOURCE_PLANS = FileSystemStorage(location='media/strategy/strat_obj/rsc_plans')


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


"""
Departmental Strategic Overview - PART A -- Start
"""


class Overview(TimeStampedModel):
    # TODO add uuid as ID
    """ Strategic overview of the branch / department """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    priority_programme = models.CharField(max_length=50, null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)
    values = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)
    revisions = models.TextField(null=True, blank=True)
    mtef_budget = models.DecimalField(decimal_places=2, default=00.00, max_digits=10)
    analysis = models.TextField(null=True, blank=True)
    is_signed = models.BooleanField(default=False)
    signed_user = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}{}".format(self.branch.name, self.id)


"""
Departmental Strategic Objectives /StrategicObjective - PART B -- Start
"""


class Framework(TimeStampedModel):
    """StrategicDetail Planning and Development"""

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    obj_id = models.UUIDField(unique=True)

    def __str__(self):
        return "{} {} {}".format(self.year, self.obj_id, self.branch)


class Goal(TimeStampedModel):

    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    goal_id = models.obj_id = models.UUIDField(unique=True)
    goal = models.CharField(max_length=255, null=True, blank=True)
    statement = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.goal


class AnnualTarget(TimeStampedModel):
    framework = models.ForeignKey(Framework, null=True, on_delete=models.CASCADE)
    year_index = models.PositiveSmallIntegerField(default=0)
    baseline = models.TextField(null=True, blank=True)
    evidence = models.TextField(null=True, blank=True)
    timeframe_start_d = models.DateField(default=datetime.date.today)
    timeframe_end_d = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{} > {}".format(self.timeframe_start_d, self.timeframe_end_d)


class KeyPerformanceIndicator(TimeStampedModel):
    """ KPIs"""
    annual_targets = models.ManyToManyField(AnnualTarget)
    kpi = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.kpi


class StrategicOutput(TimeStampedModel):
    """Strategic outputs"""

    kpis = models.ManyToManyField(KeyPerformanceIndicator)
    output = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.output


class Objective(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, null=True, on_delete=models.CASCADE)
    strategic_outputs = models.ManyToManyField(StrategicOutput)
    programme = models.ForeignKey(Programme, null=True, on_delete=models.CASCADE)
    objective = models.TextField(null=True, blank=True)
    baseline = models.TextField(null=True, blank=True)
    justification = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    statement = models.TextField(null=True, blank=True)
    index_no = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.objective


class Subprogramme(TimeStampedModel):
    objective = models.ManyToManyField(Objective)
    linked_programme = models.ForeignKey(Programme, related_name="linked_programme", on_delete=models.CASCADE, null=True)
    subprogramme = models.TextField(null=True, blank=True)
    index_no = models.CharField(max_length=5, blank=True, null=True)
    purpose = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subprogramme


class Imperatives(TimeStampedModel):

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.link, self.objective)


class Risk(TimeStampedModel):
    """ Organisational risks"""
    framework = models.ForeignKey(Framework, null=True, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    likelihood = models.CharField(max_length=100, blank=True, null=True)
    impact = models.TextField(null=True, blank=True)
    mit_plan = models.TextField(null=True, blank=True)


class ResourcePlan(TimeStampedModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    plan = models.TextField(null=True, blank=True)


"""
Departmental Strategic Links to Other Plans - PART C -- Start
"""


class LinksToPlans(TimeStampedModel):
    """ Links to other plans """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    link = models.CharField(max_length=100, null=True, blank=True)


"""
Departmental Strategic Annexture /addendum - PART D -- Start
"""


class Annexture(TimeStampedModel):
    """ link to annexture / addendum """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, null=True, blank=True)

