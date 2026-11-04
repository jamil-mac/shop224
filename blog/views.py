from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from blog.models import PostModel, CommentModel, CommentLikeModel


class PostListView(ListView):
    template_name = 'about.html'
    queryset = PostModel.objects.order_by('-pk')
    context_object_name = 'posts'


def post_detail(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    comments = post.comments.order_by('-pk')

    if request.method == 'POST':
        comment_text = request.POST.get('comment')

        if comment_text:
            if request.user.is_authenticated:
                CommentModel.objects.create(
                    user=request.user,
                    comment=comment_text,
                    post=post,
                )
                return redirect("blog:detail", pk=post.pk)
            else:
                return redirect("accounts:login")

    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'blog-detail.html', context)


@login_required
def comment_like(request, pk):
    comment = get_object_or_404(CommentModel, pk=pk)
    user = request.user

    like = CommentLikeModel.objects.filter(user=user, comment=comment)

    if like.exists():
        like.delete()
    else:
        CommentLikeModel.objects.create(user=user, comment=comment)

    return redirect(request.GET.get('next', '/'))
