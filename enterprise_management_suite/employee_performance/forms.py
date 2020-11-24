from django import forms

from .models import PerformanceAgreement


class PAForm(forms.ModelForm):
    period_start = forms.DateField()
    period_end = forms.DateField()

    class Meta:
        model = PerformanceAgreement
        exclude = ('supervisor', 'staff', 'kras', 'is_signed_staff', 'is_signed_super',)
        fields = ['period_start', 'period_end', 'pa_id']