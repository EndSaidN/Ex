from .api import PostViewSet
from rest_framework import routers

post_router = routers.DefaultRouter()
post_router.register('sn/api/posts', PostViewSet, 'api-post')

urlpatterns = post_router.urls
