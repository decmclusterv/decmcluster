from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperAdmin(BasePermission):
    """
    Custom permission to only allow superusers (superadmins) to access the endpoint.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_staff
                or getattr(request.user, "role", None) == "superadmin"
            )
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class RoleBasedPermission(BasePermission):
    """
    Custom permission for role-based access control:
    - Superadmin (is_staff/is_superuser or role == 'superadmin'):
        Can perform any operation (full CRUD: view, create/upload, edit/verify/update, delete).
    - Area Administrator (role == 'area_administrator'):
        Can view and edit / verify / update data (GET, HEAD, OPTIONS, PUT, PATCH).
        Cannot upload new data (POST) or delete data (DELETE).
    - Field Coordinator (role == 'field_coordinator'):
        Can view, upload, and edit data (GET, HEAD, OPTIONS, POST, PUT, PATCH).
        Cannot delete data (DELETE).
    - EC Focal Point (role == 'ec_focal_point'):
        Can view, upload, and edit data (GET, HEAD, OPTIONS, POST, PUT, PATCH).
        Cannot delete data (DELETE).
    - Data Enumerator (role == 'data_enumerator'):
        Can only view and upload data (GET, HEAD, OPTIONS, POST).
        Cannot edit (PUT, PATCH) or delete data (DELETE).
    - Viewer (role == 'viewer'):
        Can only view data (GET, HEAD, OPTIONS).
        Cannot upload, edit, or delete data.
    """

    EDIT_METHODS = ("PUT", "PATCH")

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False

        # Superadmin can do anything
        if user.is_superuser or user.is_staff or getattr(user, "role", None) == "superadmin":
            return True

        role = getattr(user, "role", None)

        # Viewer can only view
        if role == "viewer":
            return request.method in SAFE_METHODS

        # Area Administrator can only edit, verify, or update the data with view also
        if role == "area_administrator":
            return request.method in SAFE_METHODS or request.method in self.EDIT_METHODS

        # Field Coordinator and EC Focal Point can upload, edit, and view data
        if role in ("field_coordinator", "ec_focal_point"):
            return (
                request.method in SAFE_METHODS
                or request.method == "POST"
                or request.method in self.EDIT_METHODS
            )

        # Data Enumerator can only upload and view data
        if role == "data_enumerator":
            return request.method in SAFE_METHODS or request.method == "POST"

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

