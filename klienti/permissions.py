from rest_framework import permissions

class IsPoradceOrAdmin(permissions.BasePermission):
    """
    Povolit pouze poradcům a administrátorům (role 'poradce' nebo staff/superuser).
    """
    def has_permission(self, request, view):
        user = request.user
        print(f"[DEBUG has_permission] user={user}, is_staff={user.is_staff}, is_superuser={user.is_superuser}, role={getattr(getattr(user, 'userprofile', None), 'role', None)}")
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        try:
            return user.userprofile.role == 'poradce'
        except Exception as e:
            print(f"[DEBUG has_permission] Exception: {e}")
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        print(f"[DEBUG has_object_permission] user={user}, is_staff={user.is_staff}, is_superuser={user.is_superuser}, role={getattr(getattr(user, 'userprofile', None), 'role', None)}")
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        try:
            return user.userprofile.role == 'poradce'
        except Exception as e:
            print(f"[DEBUG has_object_permission] Exception: {e}")
            return False

class IsKlientOrReadOnly(permissions.BasePermission):
    """
    Klient může číst a upravovat pouze své záznamy, ostatní mají read-only přístup.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        try:
            if user.userprofile.role == 'klient':
                return obj.user == user
        except Exception:
            pass
        return request.method in permissions.SAFE_METHODS
