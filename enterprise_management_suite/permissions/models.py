from django.db import models
from accounts.models import Employee
from programme_project.models import Project, TimeStampedModel

import uuid


class AccessLevel(models.Model):
    """
    User can have access level of 'r' -> reading (1) or 'w' for writing (2)
    """
    READ = 'read'
    WRITE = 'write'
    MODES = (
        (READ, 'read'),
        (WRITE, 'write')
    )
    name = models.CharField(max_length=5)
    mode = models.CharField(choices=MODES, default=MODES[0], max_length=5)
    description = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.name


class Contributor(TimeStampedModel):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    queue_position = models.PositiveSmallIntegerField(default=1)
    note = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} {}".format(self.employee.user.employee_code, self.queue_position)

    class Meta:
        unique_together = ('employee', 'project')


class ActiveProjectAccessDetails(TimeStampedModel):
    uuid = models.UUIDField(null=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uuid)


class Signature(TimeStampedModel):
    APPROVED = 1
    REJECTED = 2
    UNSIGNED = 3
    TOKENS = (
        (APPROVED, 'approved'),
        (REJECTED, 'rejected'),
        (UNSIGNED, 'unsigned')
    )
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    token = models.IntegerField(choices=TOKENS)

    def __str__(self):
        return "{} - {} - {}".format(self.contributor, self.project, self.token)
