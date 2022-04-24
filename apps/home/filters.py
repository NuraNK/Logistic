import django_filters

from .models import *


class TeachersFilter(django_filters.FilterSet):
    class Meta:
        model = Sklad
        # fields = (
        #     "__all__"
        # )
        exclude=(
            'date',
            'obiem',
            'accept'
        )
