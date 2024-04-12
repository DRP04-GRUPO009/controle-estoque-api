from rest_framework import generics
from controle_estoque_api.api.permissions import ApiSchoolUnitPermissions
from school_unit.api.serializers import SchoolUnitSerializer, SchoolUnitWriteSerializer
from ..models import SchoolUnit


class SchoolUnitListAPIView(generics.ListAPIView):
    serializer_class = SchoolUnitSerializer
    permission_classes = [ApiSchoolUnitPermissions]

    def get_queryset(self):
        user = self.request.user
        user_groups_ids = user.groups.values_list('id', flat=True)

        if not user_groups_ids:
            return SchoolUnit.objects.all()

        queryset = SchoolUnit.objects.filter(id__in=user_groups_ids)
        return queryset


class SchoolUnitRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ApiSchoolUnitPermissions]


class SchoolUnitCreateApiView(generics.CreateAPIView):
    serializer_class = SchoolUnitWriteSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ApiSchoolUnitPermissions]


class SchoolUnitUpdateApiView(generics.UpdateAPIView):
    serializer_class = SchoolUnitWriteSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ApiSchoolUnitPermissions]


class SchoolUnitDestroyApiView(generics.DestroyAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ApiSchoolUnitPermissions]
