from django.urls import path
from accounts.views import *

urlpatterns = [
    path('register/', UserRegister.as_view(), name='registration'),
    path('edit_profile/', UserEdit.as_view(), name='edit-profile'),
    path('profile/<int:pk>', profiles, name='profile'),
    path('all_profiles/', AllUsers.as_view(), name='all-profile'),
    # '''-------------------- APIS --------------------'''
    path('api-home/', ApiOverview, name='api-home'),
    path('create/', add_profiles, name='api-add-profiles'),
    path('all/', view_profiles, name='view-profiles'),
    path('update/<int:pk>/', update_profiles, name='update-profiles'),
    path('profiles/<int:pk>/delete/', delete_profiles, name='delete-profiles'),
]
