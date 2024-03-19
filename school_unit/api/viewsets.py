from rest_framework import generics
from controle_estoque_api.api.permissions import ReadOnlyUnlessStaff
from school_unit.api.serializers import SchoolUnitSerializer
from ..models import SchoolUnit

class SchoolUnitListAPIView(generics.ListAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class SchoolUnitRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class SchoolUnitCreateApiView(generics.CreateAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class SchoolUnitUpdateApiView(generics.UpdateAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class SchoolUnitDestroyApiView(generics.DestroyAPIView):
    serializer_class = SchoolUnitSerializer
    queryset = SchoolUnit.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]
