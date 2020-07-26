from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,  authenticate
from .forms import UserCreationForm, UserLoginForm, UserProfileEdithForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blog.models import Post

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from account.models import User
user = User.objects.all()

def Signup_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST, request.FILES)
            if form.is_valid():

                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate Your UniverseExplorerBlog Account.'
                message = render_to_string('account/acc_active_email.html',{
                    'user':user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),})
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to = [to_email])
                email.send()
                return render(request, 'account/email_confirmation.html')

            
        else:
            form = UserCreationForm()
        return render(request, 'account/register.html', {'form':form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError , User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return redirect('dashboard_index') 
        
        return render(request, 'account/email_confirmed.html')
        
       
        
    else:
        return render(request,'account/email_activation_error.html')

def logout_view(request):
    logout(request)
    return redirect('post_list')


def login_view(request):

    
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
   


        if request.POST:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                

                if user:
                    login(request, user)
                    messages.success(request, "Welcome {} ".format(request.user.username))
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('post_list')
                    
        
                    
        else:
            form = UserLoginForm()
        return render(request, 'account/login.html',{'form':form})


def Account_Update(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    user = request.user
    favourite_posts_count = user.favourite.all().count()
    all_user_posts_count = Post.objects.filter(author=request.user).count()

    if request.POST:
        user = request.user
        form = UserProfileEdithForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account {} has been  successfully updated!".format(request.user.username))
    else:
        form = UserProfileEdithForm(initial = {"email":request.user.email,
                                                "username": request.user.username,
                                                "first_name": request.user.first_name,
                                                "last_name": request.user.last_name,
                                                
                                                })
    
    context = {
        'form': form,
        'favourite_posts_count': favourite_posts_count, 
        'all_user_posts_count': all_user_posts_count,
    }
    return render(request, 'account/account_update.html', context)


