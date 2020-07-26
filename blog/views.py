from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from blog.models import Post, Comment, NewsletterSignup
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from datetime import datetime
from .forms import PostCreationForm, PostEdithForm, CommentForm, UserContactForm, UserNewsletterSignup, SendEmailForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.db.models import Count
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings



def post_list(request, tag_slug=None):
    
    post_list = Post.published.all().order_by('-id')

    post_title_list = Post.published.all().order_by('-id')


    if request.user.is_authenticated:
        user = request.user
        favourite_posts_count = user.favourite.all().count()
        all_user_posts_count = Post.objects.filter(author=request.user).count()
    

    
    
    
    
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)
    query = request.GET.get('q')
    if query:
        post_list = Post.published.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)
        )
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    
    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(post, index=4)
    page_range = list(paginator.page_range)[start_index:end_index]

    
    
    form = UserNewsletterSignup()
    if request.method == 'POST':
        form = UserNewsletterSignup(request.POST or None)
        if form.is_valid():
            email_signup_qs = NewsletterSignup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed to our newsletter updates")
            else:
                form.save()
                messages.success(request, "You have successfully subscribe to our newsletter updates")

            return redirect('post_list')
    else:
        form = UserNewsletterSignup()

     



    
    context = {
        'post': post,
        'page_range': page_range,
        'tag' : tag,
        'post_title_list': post_title_list,
        'form': form,
        
        
        
        
        
        
        
    }

    if request.user.is_authenticated:
        context = {
        'post': post,
        'page_range': page_range,
        'tag' : tag,
        'post_title_list': post_title_list,
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count, 
        'form': form,   
    }

    return render (request, 'blog/post_list.html', context)




def proper_pagination(post, index):
    start_index = 0
    end_index = 7
    if post.number > index:
        start_index = post.number - index
        end_index = start_index + end_index
    return (start_index, end_index)










def post_detail(request, id, slug, tag_slug=None):
    post = get_object_or_404(Post, id=id, slug=slug)
    post_title_list = Post.published.all().order_by('-id')
    post_list = Post.published.all().order_by('-id')
    recent_post = Post.published.all().order_by('-id')[:6]
    
    views_count = Post.published.get(id=id)
    views_count.blog_views = views_count.blog_views+1
    views_count.save()
    
    if request.user.is_authenticated:
        user = request.user
        favourite_posts_count = user.favourite.all().count()
        all_user_posts_count = Post.objects.filter(author=request.user).count()

    

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-id')[:6]
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    
    is_liked = False
    is_favourite = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    is_heart = False
    if post.heart.filter(id=request.user.id).exists():
        is_heart = True

    

    if request.method =='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            
    else:
        comment_form = CommentForm()
    context = {
        'comments': comments,
        'post': post,
        'is_favourite': is_favourite,
        'is_liked': is_liked,
        'is_heart': is_heart,
        'total_likes': post.total_likes(),
        'total_heart': post.total_heart(),
        'comment_form': comment_form,
        'tag':tag,
        'similar_posts': similar_posts,
        'recent_post' : recent_post,
        'post_title_list': post_title_list,
       
        
        
    }

    if request.user.is_authenticated:
        context = {
        'comments': comments,
        'post': post,
        'is_favourite': is_favourite,
        'is_liked': is_liked,
        'is_heart': is_heart,
        'total_likes': post.total_likes(),
        'total_heart': post.total_heart(),
        'comment_form': comment_form,
        'tag':tag,
        'similar_posts': similar_posts,
        'recent_post' : recent_post,
        'post_title_list': post_title_list,
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count,
        
        
    }

    if request.is_ajax():
        html = render_to_string('blog/comments_section.html', context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='login')
def post_favourite_list(request, tag_slug=None):
    post_list = Post.published.all().order_by('-id')
    post_title_list = Post.published.all().order_by('-id')
    user = request.user
    favourite_posts = user.favourite.all().order_by('-id')

    
    favourite_posts_count = user.favourite.all().count()
    all_user_posts_count = Post.objects.filter(author=request.user).count()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)

    form = UserNewsletterSignup()
    if request.method == 'POST':
        form = UserNewsletterSignup(request.POST or None)
        if form.is_valid():
            email_signup_qs = NewsletterSignup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed to our newsletter updates")
            else:
                form.save()
                messages.success(request, "You have successfully subscribe to our newsletter updates")

            return redirect('post_list')
    else:
        form = UserNewsletterSignup()

    context = {
        'favourite_posts': favourite_posts,
        'tag': tag,
        'post_title_list': post_title_list, 
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count,
        'form': form,
    }
    return render(request, 'blog/post_favourite_list.html', context)



@login_required(login_url='login')
def user_post_list(request, tag_slug=None):
    post_list = Post.published.all().order_by('-id')
    post_title_list = Post.published.all().order_by('-id')
    user = request.user
    all_user_posts = Post.objects.filter(author=request.user).order_by('-id')

    favourite_posts_count = user.favourite.all().count()
    all_user_posts_count = Post.objects.filter(author=request.user).count()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)
    paginator = Paginator(all_user_posts, 10)
    page = request.GET.get('page')
    try:
        user_posts = paginator.page(page)
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)
    
    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(user_posts, index=4)
    page_range = list(paginator.page_range)[start_index:end_index]
    

    form = UserNewsletterSignup()
    if request.method == 'POST':
        form = UserNewsletterSignup(request.POST or None)
        if form.is_valid():
            email_signup_qs = NewsletterSignup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed to our newsletter updates")
            else:
                form.save()
                messages.success(request, "You have successfully subscribe to our newsletter updates")

            return redirect('post_list')
    else:
        form = UserNewsletterSignup()

    context = {
        'user_posts': user_posts,
        'user': user,
        'page_range':page_range,
        'tag': tag,
        'post_title_list': post_title_list, 
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count,
        'form': form,
    }
    return render(request, 'blog/user_post_list.html', context)


@login_required(login_url='login')
def favourite_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


@login_required(login_url='login')
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        
        'post': post,
        'is_liked' : is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form':html})
    
        

@login_required(login_url='login')
def heart_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_heart = False
    
    if post.heart.filter(id=request.user.id).exists():
        post.heart.remove(request.user)
        is_heart = False
    
    else:
        post.heart.add(request.user)
        is_heart = True
    context = {
        
        'post': post,
        'is_heart' : is_heart,
        'total_heart': post.total_heart(),
    }
    if request.is_ajax():
        html = render_to_string('blog/heart_section.html', context, request=request)
        return JsonResponse({'form':html})



@login_required(login_url='login')
def post_create(request):
    user = request.user
    favourite_posts_count = user.favourite.all().count()
    all_user_posts_count = Post.objects.filter(author=request.user).count()

    if request.method =='POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post has been successfully created.")
            return redirect('post_list')
    else:
        form = PostCreationForm()
    context = {
        'form': form,
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count,  
    }

    return render(request, 'blog/post_create.html', context)


@login_required(login_url='login')
def post_edit(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)

    user = request.user
    favourite_posts_count = user.favourite.all().count()
    all_user_posts_count = Post.objects.filter(author=request.user).count()

    if post.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = PostEdithForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "{} has been successfully updated!".format(post.title))
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEdithForm(instance=post)
    context = {
        'form': form,
        'post': post,
        'favourite_posts_count': favourite_posts_count,
        'all_user_posts_count': all_user_posts_count,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required(login_url='login')
def post_delete(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.user != post.author:
        raise Http404()
    post.delete()
    messages.warning(request, 'Post has been successfully deleted!')
    return redirect('post_list')


def contact_us(request):
    form = UserContactForm()
    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            email_from = settings.EMAIL_HOST_USER

            message = "{0} has sent you a new message:\n\n{1}".format(name, form.cleaned_data.get('message'))
            send_mail('New Enquiry', message, email,[email_from])


            messages.success(request, 'Message sent successfully')
            return redirect('post_list')
    else:
        form = UserContactForm()

    return render(request, 'blog/contact_page.html', {'form':form})    


def SendEmail(request):
    form = SendEmailForm()
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            
            to = form.cleaned_data.get('to')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to,]    
            send_mail( subject, message, email_from, recipient_list )    
            messages.success(request, 'Message successfully sent to {}'.format(to))
            return redirect('send_email')
            
    else:
        form = SendEmailForm()
    email_u = NewsletterSignup.objects.all()
    
    
    context = {
        'form': form,
        'email_u': email_u,
    }

    return render(request, 'blog/send_email.html', context)  


  



    