from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User


class UserAdmin(BaseUserAdmin):

    
    
    list_display = ('email','username','first_name','last_name','photo','date_joined','is_active','last_login','is_staff','is_superuser','is_admin')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    ordering = ('email',)
    filter_horizontal =()
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields':('email','is_active','last_login','is_staff','is_superuser','is_admin','password')}),
        ('Personal info',{'fields':('username','first_name','last_name','photo')}),
        
       
    )
     
    add_fieldsets = (
        (None, {'fields':('email','is_active','last_login','is_staff','is_superuser','is_admin','password1','password2')}),
        ('Personal info',{'fields':('username','first_name','last_name','photo')}),
        
       
    )


admin.site.register(User, UserAdmin)

