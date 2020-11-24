from django.db import models
from django.core.files.storage import FileSystemStorage

from accounts.models import Employee
from organisation.models import Branch, Component, Organisation, Programme

TEMPLATES = FileSystemStorage(location='media/ppm/projects/templates')
PLANS = FileSystemStorage(location='media/ppm/projects/plan')
SUPPORT_DOCS = FileSystemStorage(location='media/ppm/projects/support_docs')


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProjectType(TimeStampedModel):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Status(models.Model):

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Project Progress Status'


class Project(TimeStampedModel):

    ANNUALLY = 'Annually'
    QUARTERLY = 'Quarterly'
    REPORTING_CYCLE = (
        (ANNUALLY, 'Annually'),
        (QUARTERLY, 'Quarterly')
    )

    ON_TRACK = 'On-Track'
    DELAYED = 'Delayed'
    CHALLENGED = 'Challenged'
    CANCELLED = 'Cancelled'

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    project_manager = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    budget = models.DecimalField(decimal_places=2, default=0.0, max_digits=12)
    report_cycle = models.CharField(choices=REPORTING_CYCLE, max_length=15)
    templates = models.FileField(upload_to=TEMPLATES, null=True)
    plan = models.FileField(upload_to=PLANS, null=True)
    supporting_docs = models.FileField(null=True)
    risk = models.TextField(null=True)
    number = models.UUIDField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    details = models.TextField(null=True)
    # Designates whether this project should be treated as active.
    # Unselect / flag as False this instead of deleting projects
    is_active = models.BooleanField(default=True)
    comments = models.TextField(null=True)
    sponsor = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

