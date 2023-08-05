from .api import ProfileViewSet
from rest_framework import routers

profile_router = routers.DefaultRouter()
profile_router.register('sn/api/profile', ProfileViewSet, 'api-profile')

urlpatterns = profile_router.urls
