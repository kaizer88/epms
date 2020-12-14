from django.db import models
from django.core.files.storage import FileSystemStorage

<<<<<<< HEAD
# from accounts.models import Employee, Supervisor
=======
from accounts.models import Employee, Supervisor
>>>>>>> master


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PositiveIntegerRangeField(models.PositiveIntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, default=None, **kwargs):
        self.min_value, self.max_value, self.default = min_value, max_value, default
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(PositiveIntegerRangeField, self).formfield(**defaults)

fs = FileSystemStorage(location='media/ep/performance/evidence/')


class Bathopele(TimeStampedModel):
    """
    Batho Pele principles for KRAs
    """
    description = models.CharField('Batho Phele Principles', max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Batho Phele Principles'


class MeasurableOutput(TimeStampedModel):
    """
    Measurable Output
    """
    DAILY = 'd'
    WEEKLY = 'w'
    MONTHLY = 'm'
    ANNUALLY = 'a'

    TIME_FRAMES = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALLY, 'Annually')
    )

<<<<<<< HEAD
    supervisor = models.ManyToManyField('accounts.Employee', related_name='kra_supervisor')
=======
    supervisor = models.ManyToManyField(Employee, related_name='kra_supervisor')
>>>>>>> master
    mo_kra_id = models.UUIDField(max_length=50)
    output_id = models.UUIDField(max_length=50)
    output = models.TextField('Measurable Output')
    slug = models.SlugField()
    self_weight = models.FloatField('Self Output Weight', default=0, null=True, blank=True)
    super_weight = models.FloatField('Senior Management Service Weight', default=0, null=True, blank=True)
    self_rating = PositiveIntegerRangeField('Self Rating', min_value=1, max_value=5, null=True, blank=True)
    agreed_rating = PositiveIntegerRangeField('Supervisor Rating', min_value=1, max_value=5, null=True, blank=True)
    super_rating = PositiveIntegerRangeField('Supervisor Rating', min_value=1, max_value=5, null=True, blank=True)
    time_frame = models.CharField('Time Frame', choices=TIME_FRAMES, max_length=1, null=True, blank=True)
    cal_date = models.DateField('Calendar Date', null=True, blank=True)
    resources = models.TextField('Resources', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    target = models.CharField('Target', null=True, blank=True, max_length=255)

    def __str__(self):
        return str(self.self_weight)

    class Meta:
        verbose_name_plural = 'Measurable Outputs'


class TrainingNeed(TimeStampedModel):
    """
    Personal Development Plan, PDP
    """

    DAILY = 'd'
    WEEKLY = 'w'
    MONTHLY = 'm'
    ANNUALLY = 'a'

    TIME_FRAMES = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALLY, 'Annually')
    )

    pdp_kra_id = models.UUIDField(max_length=50)
    pdp_id = models.UUIDField(max_length=50, unique=True)
    t_type = models.CharField('Training Need Type', max_length=255, null=True, blank=True)
    outcome = models.TextField('Expected Outcome', null=True, blank=True)
    time_frame = models.CharField('Time Frame', choices=TIME_FRAMES, max_length=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.t_type


class MOReview(TimeStampedModel):

    reviewed_kra_id = models.UUIDField()
    self_rating = models.DecimalField('Staff Rating', default=0.0, decimal_places=1, max_digits=4)
    super_rating = models.DecimalField('Supervisor Rating', default=0.0, decimal_places=1, max_digits=4)
    agreed_rating = models.DecimalField('Agreed Rating', default=0.0, decimal_places=1, max_digits=4)
    final_score = models.DecimalField('Score', default=0.0, decimal_places=1, max_digits=4)
    self_comment = models.TextField('Employee Comment')
    super_comment = models.TextField('Supervisor Comment')
    self_note = models.TextField('Staff Notes')
    super_note = models.TextField('Supervisor Notes')
    pa_weight = models.DecimalField('PA Weight', default=0.0, decimal_places=1, max_digits=4)
    rev_weight = models.DecimalField('Staff Review Weight', default=0.0, decimal_places=1, max_digits=4)
    employee_has_signed = models.BooleanField(default=False)
    supervisor_has_signed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Review Measurable Outputs'

    def __float__(self):
        return self.pa_weight


class ReviewPeriod(TimeStampedModel):
    """
    Date range for the review period and period cycle
    """
    period_start = models.DateField('Period Start', auto_now_add=False)
    period_end = models.DateField('Period End', auto_now_add=False)
    cycle = models.DateField()

    class Meta:
        verbose_name_plural = 'Review Periods'

    def __str__(self):
        return '{} -- {}'.format(self.period_end, self.period_end)


class KRAReview(TimeStampedModel):

    kra_id = models.UUIDField()
<<<<<<< HEAD
    employee = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE)
    supervisor = models.ManyToManyField('accounts.Employee', related_name='review_supervisor')
=======
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    supervisor = models.ManyToManyField(Employee, related_name='review_supervisor')
>>>>>>> master
    outputs = models.ManyToManyField(MOReview)
    dispute = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    final_score = models.DecimalField('Final Score', default=0.0, max_digits=4, decimal_places=1)
    self_rating = PositiveIntegerRangeField('Self Rating', min_value=1, max_value=5, null=True, blank=True, default=0)
    super_rating = PositiveIntegerRangeField('Supervisor Rating', min_value=1, max_value=5, null=True, blank=True,
                                             default=0)
    agreed_rating = PositiveIntegerRangeField('Supervisor Rating', min_value=1, max_value=5, null=True, blank=True,
                                              default=0)
    rev_weight = models.DecimalField('Staff Review Weight', default=0.0, decimal_places=1, max_digits=4)

    class Meta:
        verbose_name_plural = 'Key Result Area Reviews'

    def __str__(self):
        return '{} - Rated - {} - By {}'.format(self.kra_id, self.self_rating, self.employee)


class ProcessedKRAReview(TimeStampedModel):

    processed_rev_id = models.UUIDField()
    review = models.ManyToManyField(KRAReview)
    review_type = models.CharField('Review Type', max_length=8, null=True, blank=True)
    is_signed = models.BooleanField('Is Review Signed', default=False)
    email_is_sent = models.BooleanField('Is Notification Email Sent', default=False)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    employee_has_signed = models.BooleanField(default=False)
    supervisor_has_signed = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} to {}".format(self.processed_rev_id, self.period_start, self.period_end)


class Target(TimeStampedModel):

    target_id = models.UUIDField(unique=True, max_length=50)
    kpi_id = models.UUIDField(max_length=50)
    target = models.TextField()
    evidence = models.TextField()
    baseline = models.TextField()


class KeyPerformanceIndicator(TimeStampedModel):

    target = models.ManyToManyField(Target)
    kpi_id = models.UUIDField(max_length=50, unique=True)
    description = models.TextField()
    staff_weight = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Key Performance Indicators'


class KeyResultArea(TimeStampedModel):
    """
    Key Result Area
    """
    review = models.ForeignKey(KRAReview, on_delete=models.CASCADE, null=True, blank=True)
    kra_pa_id = models.UUIDField(max_length=50)
    kra_id = models.UUIDField(max_length=50, unique=True)
<<<<<<< HEAD
    supervisor = models.ManyToManyField('accounts.Supervisor')
    employee = models.ManyToManyField('accounts.Employee')
=======
    supervisor = models.ManyToManyField(Supervisor)
    employee = models.ManyToManyField(Employee)
>>>>>>> master
    bathophele = models.ManyToManyField(Bathopele)
    outputs = models.ManyToManyField(MeasurableOutput)
    training_needs = models.ManyToManyField(TrainingNeed)
    indicators = models.ManyToManyField(KeyPerformanceIndicator)
    kra = models.TextField('KRA Entry', null=True, blank=True)
    slug = models.SlugField()
    self_weight = models.FloatField('Employee Weight', default=0, null=True, blank=True)
    evidence = models.FileField(upload_to=fs, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.kra_id)

    class Meta:
        verbose_name_plural = 'Key Result Areas'


class GenericSTD(TimeStampedModel):
    description = models.TextField()
    weight = models.FloatField(default=0)

    def __str__(self):
        return '{} -- {}'.format(self.weight, self.description)

    class Meta:
        verbose_name_plural = 'Generic Standards'


class CoreManagementCriteria(TimeStampedModel):
    """
    Capture Core Management Criteria by users from 13 up.
    Link it to Bophele principles and generic standards
    """

    bophele = models.ManyToManyField(Bathopele)
    g_std = models.ManyToManyField(GenericSTD)
    description = models.TextField()
    weight = models.FloatField(default=0)
    dept_specific = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} -- {}'.format(self.weight, self.description)

    class Meta:
        verbose_name_plural = 'Core Management Criteria'
        ordering = ['description', 'weight']


class PerformanceAgreement(TimeStampedModel):

    pa_id = models.UUIDField(max_length=50, unique=True)
<<<<<<< HEAD
    supervisor = models.ManyToManyField('accounts.Supervisor')
    employee = models.ManyToManyField('accounts.Employee')
=======
    supervisor = models.ManyToManyField(Supervisor)
    employee = models.ManyToManyField(Employee)
>>>>>>> master
    kras = models.ManyToManyField(KeyResultArea)
    employee_has_signed = models.BooleanField(default=False)
    supervisor_has_signed = models.BooleanField(default=False)
    period_start = models.CharField(max_length=12, null=True, blank=True)
    period_end = models.CharField(max_length=12, null=True, blank=True)
    fin_year_start = models.CharField(max_length=12, null=True, blank=True)
    fin_year_end = models.CharField(max_length=12, null=True, blank=True)
    fyear = models.CharField(max_length=12, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pa_id)

    class Meta:
        verbose_name_plural = 'Performance Agreements (PAs)'
