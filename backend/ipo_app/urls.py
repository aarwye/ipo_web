from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IPOViewSet, all_ipos

router = DefaultRouter()
router.register('ipos', IPOViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all-ipos/', all_ipos, name='all-ipos'),
]
