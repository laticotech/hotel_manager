import django_filters
from .models import Food



class FoodFilter(django_filters.FilterSet):

    class Meta:
        model = Food
        fields = [
            'food_name',

        ]
