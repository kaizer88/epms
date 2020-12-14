from django.forms import ModelForm

from .models import Framework, Overview


class StrategyForm(ModelForm):

    class Meta:
        model = Framework
        fields = ['obj_id']


class OverviewForm(ModelForm):

    class Meta:
        model = Overview
        fields = ['vision', 'mission', 'values', 'revisions', 'priority_programme', 'goals', 'analysis',
                  'risks', 'mtef_budget']

