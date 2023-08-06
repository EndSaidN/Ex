from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import serializers, status

from message.models import Post, Comment
from message.forms import PostForm, EditPostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from message.serializers import PostSerializer


def Like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('detail-post', args=[str(pk)]))


class Home(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']


class PostDetail(DetailView):
    model = Post
    template_name = 'post_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')


class AddPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'


class UpdatePost(UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'post_update.html'


class DeletePost(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


'''-------------------- APIS --------------------'''


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_posts': '/api-home/',
        'Search by Title': '/?title=title_name',
        'All Posts': '/all',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
def add_posts(request):
    post = PostSerializer(data=request.data)
    if Post.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if post.is_valid():
        post.save()
        return Response(post.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_posts(request):
    if request.query_params:
        post = Post.objects.filter(**request.query_params.dict())
    else:
        post = Post.objects.all()
    if post:
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_posts(request, pk):
    post = Post.objects.get(pk=pk)
    data = PostSerializer(instance=post, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_posts(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
