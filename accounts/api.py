from rest_framework import viewsets, permissions
from .serializers import ProfileSerializer
from message.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProfileSerializer
