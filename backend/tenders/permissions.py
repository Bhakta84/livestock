from rest_framework.permissions import BasePermission
class StaffTenderPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.groups.filter(name__in=["Admin","Procurement Officer"]).exists())
