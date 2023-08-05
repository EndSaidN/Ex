from django.urls import path
from accounts.views import UserRegister, UserEdit, AllUsers, profiles

urlpatterns = [
    path('register/', UserRegister.as_view(), name='registration'),
    path('edit_profile/', UserEdit.as_view(), name='edit-profile'),
    path('profile/<int:pk>', profiles, name='profile'),
    path('all_profiles/', AllUsers.as_view(), name='all-profile'),
]
