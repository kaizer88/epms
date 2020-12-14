from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.timezone import now

<<<<<<< HEAD
# from enterprise_management_suite.organisation.models import Organisation, Branch, Component, Programme
=======
from organisation.models import Organisation, Branch, Component, Programme
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


class EPMUserManager(BaseUserManager):
    def create_user(self, email, employee_code, password=None):
        """
        Creates and saves a User with the given email, employee_code and password.
        """
        if not employee_code:
            raise ValueError('Users must have an Employee Number')
        user = self.model(
            email=self.normalize_email(email),
            employee_code=employee_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, employee_code, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email,
            password=password,
            employee_code=employee_code,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Token(models.Model):

    token = models.UUIDField(null=True, blank=True)
    token_is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=now())
    expiry_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.token)


class EPMUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    employee_code = models.CharField(
        verbose_name='employee code',
        max_length=50,
        unique=True,
    )
    token = models.ForeignKey(Token, null=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField('last login', blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
        'Designates whether this user should be treated as active. ' 
        'Unselect this instead of deleting accounts.'
    )
    objects = EPMUserManager()
    USERNAME_FIELD = 'employee_code'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their employee code
        return self.employee_code

    def get_short_name(self):
        # The user is identified by their employee code
        return self.employee_code

    def __str__(self):  # __unicode__ on Python 2
        return self.employee_code

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""

        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app 'app_label?"""

        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""

        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = 'EPM Users Auth'


class SalaryNotch(TimeStampedModel):

        DURATION = (
            (1, '6/8th'),
            (2, '5/8th'),
            (3, '3/8th'),
        )

        NOTCH = (
            (1, 'Full-time notch'),
            (2, 'Part-time notch'),
        )

        full_time = models.FloatField(null=True, blank=True)
        part_time = models.FloatField(null=True, blank=True)
        duration = models.IntegerField(choices=DURATION, null=True, blank=True)
        notch = models.IntegerField(choices=NOTCH, null=True, blank=True)

        def __str__(self):
            return str(self.duration)


class Employee(TimeStampedModel):

    EMPLOYMENT_STATUS = (

        (1, 'Acting'),
        (2, 'Contract'),
        (3, 'Fixed - Term'),
        (4, 'Permanent'),
        (5, 'Internship'),
        (6, 'Secondmen'),
        (7, 'Probationary'),
    )

    TITLES = (
        (1, 'Ms'),
        (2, 'Miss'),
        (3, 'Mrs'),
        (4, 'Mr'),
        (5, 'Prof'),
        (6, 'Dr'),
        (7, 'Rev'),
    )

    GENDER = (
        (1, 'Female'),
        (2, 'Male'),
    )

    DISABILITY = (
        (1, 'Disabled'),
        (2, 'Not Disabled'),
    )

    RACE = (
        (1, 'Asian'),
        (2, 'Black'),
        (3, 'Coloured'),
        (4, 'White')
    )

    user = models.OneToOneField(EPMUser, on_delete=models.CASCADE)
<<<<<<< HEAD
    organisation = models.ForeignKey('organisation.Organisation', on_delete=models.CASCADE, null=True)
    programme = models.ForeignKey('organisation.Programme', on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey('organisation.Branch', on_delete=models.CASCADE, null=True)
    component = models.ForeignKey('organisation.Component', on_delete=models.CASCADE, null=True)
=======
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
>>>>>>> master
    salary_notch = models.ForeignKey(SalaryNotch, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=100,  null=True, blank=True)
    is_first_login = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.IntegerField(choices=TITLES, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    disability_status = models.IntegerField(choices=DISABILITY, default=2)
    race = models.IntegerField(choices=RACE, default=2)
    emp_status = models.IntegerField(choices=EMPLOYMENT_STATUS, default=4)
    salary_level = models.IntegerField(null=True, blank=True)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.user.employee.first_name, self.user.employee.last_name)

    class Meta:
        verbose_name_plural = 'Employee Profile'


class Disability(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.employee)

    class Meta:
        verbose_name_plural = 'Disabilities'


class Supervisor(models.Model):

    name = models.ForeignKey(Employee, related_name='staff_supervisor', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    employees = models.ManyToManyField(Employee, related_name='supervisor_staff')

    def __str__(self):
        return str(self.name)


class Role(models.Model):

    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.role

