import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    # first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='exact')
    # last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='exact')
    roles = django_filters.BaseInFilter(method='filter_roles')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['username', 'roles', 'is_active']

    def filter_roles(self, queryset, name, value):
        # roles查詢: 支援逗號分隔的id列表，例如: roles=1,2,3
        if value:
            queryset = queryset.filter(roles__id__in=value).distinct()
        return queryset
