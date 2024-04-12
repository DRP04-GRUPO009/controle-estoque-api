from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from school_unit.models import SchoolUnit
from stock.models import StockItem


class ReadOnlyUnlessStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not isinstance(user, User):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return user.is_staff


class ApiProductPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not isinstance(user, User):
            return False

        if user.is_authenticated:
            # System Admin and Secretary User
            if user.is_staff or user.groups.count() == 0:
                return True
        return False


class ApiStockItemPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not isinstance(user, User):
            return False

        if user.is_authenticated:
            # System Admin and Secretary User
            if user.is_staff or user.groups.count() == 0:
                return True

            stock_item_id = view.kwargs.get('pk', None)
            if stock_item_id:
                stock_item_id = int(stock_item_id)
                stock_item = get_object_or_404(StockItem, id=stock_item_id)

                # School user
                if not stock_item:
                    return False
                else:
                    return user.groups.filter(id=stock_item.stock.school_unit_id).exists()


class ApiSchoolUnitPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not isinstance(user, User):
            return False

        if user.is_authenticated:
            # System Admin and Secretary User
            if user.is_staff or user.groups.count() == 0:
                return True

            school_unit_id = request.query_params.get('pk', None)
            if school_unit_id:
                school_unit_id = int(school_unit_id)
                school_unit = get_object_or_404(SchoolUnit, id=school_unit_id)

                # School user
                if not school_unit:
                    return False
                else:
                    return user.groups.filter(id=school_unit.id).exists()
            elif request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False
