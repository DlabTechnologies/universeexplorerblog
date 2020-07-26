
from django.contrib import admin
from django.urls import include, path, re_path
from blog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account.views import Signup_view, logout_view, login_view, Account_Update
from blog.views import user_post_list, contact_us, SendEmail
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from account.views import activate


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'',  views.post_list, name="post_list"),
    path(r'tag/<slug:tag_slug>/',  views.post_list, name="post_list_by_tag"),
    path(r'blog/',  include('blog.urls', namespace="blog")),
    
    
    
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path(r'sendemail', SendEmail, name="send_email"),
    path(r'contact', contact_us, name="contact"),
    path(r'register', Signup_view, name="register"),
    path(r'logout', logout_view, name="logout"),
    path(r'login', login_view, name="login"),
    path(r'account_update', Account_Update, name="account_update"),
    path(r'like/', views.like_post, name="like_post"),
    path(r'heart/', views.heart_post, name="heart_post"),
    path(r'user_post/',  views.user_post_list, name="user_post_list"),
    path(r'sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(r'activate/<uidb64>/<token>/', activate, name='activate'),
    


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
     name='password_reset_complete'),

   
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)