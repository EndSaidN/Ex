from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from message.models import Profile
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
        return render(request, 'registration/profile.html', {'profile': profile, 'total_follows': profile.follows.count()})
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

    def get_object(self):
        return self.request.user


class AllUsers(ListView):
    model = Profile
    template_name = 'registration/all_profiles.html'
    ordering = ['user_id']

