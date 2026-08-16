import django_filters

from .models import Newsletter


class NewsletterFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr="icontains")
    is_subscribed = django_filters.BooleanFilter()
    start_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Newsletter
        fields = ["email", "is_subscribed", "start_date", "end_date"]
