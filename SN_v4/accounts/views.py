from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView
from django.urls import reverse_lazy
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from accounts.serializers import ProfileSerializer
from message.models import Profile, Post
from accounts.forms import SignUpForm, EditProfileForm


def profiles(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'registration/profile.html',
                      {'profile': profile, 'total_follows': profile.follows.count()})
    else:
        messages.success(request, 'You must login')
        return redirect('home')


class UserRegister(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class UserEdit(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, **kwargs):
        return self.request.user


class AllUsers(ListView):
    model = Profile
    template_name = 'registration/all_profiles.html'
    ordering = ['user_id']


'''-------------------- APIS --------------------'''


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_profiles': '/accounts/api-home/',
        'Search by Username': '/accounts/?username=username_name',
        'All Profiles': '/accounts/all',
        'Add': '/accounts/create',
        'Update': '/accounts/update/pk',
        'Delete': '/accounts/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
def add_profiles(request):
    profile = ProfileSerializer(data=request.data)

    if Profile.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if profile.is_valid():
        profile.save()
        return Response(profile.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_profiles(request):

    if request.query_params:
        profile = Profile.objects.filter(**request.query_params.dict())
    else:
        profile = Profile.objects.all()

    if profile:
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_profiles(request, pk):
    profile = Profile.objects.get(pk=pk)
    data = ProfileSerializer(instance=profile, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_profiles(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
