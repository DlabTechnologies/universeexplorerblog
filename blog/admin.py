from django.contrib import admin

from .models import Post, Comment, ContactForm, NewsletterSignup

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','status')
    list_filter = ('status','created','updated')
    search_fields = ('author__email', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')



class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')
    
admin.site.register(ContactForm)
admin.site.register(NewsletterSignup, NewsletterSignupAdmin)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)

