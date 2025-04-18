from rest_framework.permissions import BasePermission


class ActionPermission(BasePermission):
    _map = {
        'list': 'view',
        'retrieve': 'view',
        'create': 'create',
        'update': 'update',
        'partial_update': 'update',
        'destroy': 'delete',
    }

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        model_name = view.queryset.model.__name__.lower()
        action = self.action_map(view.action)
        if not action:
            return False

        perm_code = f"{model_name}:{action}"
        return request.user.has_perm(perm_code=perm_code)

    def action_map(self, action_name):
        return self._map.get(action_name, '')
