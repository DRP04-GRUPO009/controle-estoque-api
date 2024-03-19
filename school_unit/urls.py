from django.urls import path

from school_unit.api.viewsets import SchoolUnitListAPIView, SchoolUnitCreateApiView, SchoolUnitRetrieveApiView, SchoolUnitUpdateApiView, SchoolUnitDestroyApiView

urlpatterns = [
    path('', SchoolUnitListAPIView.as_view(), name='school-unit-list'),
    path('nova/', SchoolUnitCreateApiView.as_view(), name='school-unit-create'),
    path('<int:pk>/', SchoolUnitRetrieveApiView.as_view(), name='school-unit-retrieve'),
    path('<int:pk>/alterar/', SchoolUnitUpdateApiView.as_view(), name='school-unit-update'),
    path('<int:pk>/excluir/', SchoolUnitDestroyApiView.as_view(), name='school-unit-delete'),
]
