from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from blog.models import Post
from blog.forms import EmailPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# def post_list(request):
#     post_list = Post.published.all()
#     # Постраничная разбивка с 3-мя постами на страницу
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Если page_number не целое число, то
#         # выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если page_number находится вне диапазона, то
#         # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   template_name='blog/post/list.html',
#                   context={'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    return render(request,
                  template_name='blog/post/detail.html',
                  context={'post': post})


def share_post(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['name']
            email_from = cd['email']
            email_to = cd['to']
            message = cd['comments']
            send_mail(subject, message, email_from, [email_to, ])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
