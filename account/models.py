from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            
        )

        
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,password):
        user = self.create_user(
            email = self.normalize_email(email),
            
            password=password,
            
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename, **kwargs):
    file_path = 'profile_image/{filename}'.format(filename=filename
    )
    return file_path

class User(AbstractBaseUser):
    email           =  models.EmailField(max_length=225, unique = True, verbose_name="email")
    username        =  models.CharField(max_length=50, blank=False)
    first_name      =  models.CharField(max_length=50, blank=False)
    last_name       =  models.CharField(max_length=50, blank=False)
    photo           =  models.ImageField(upload_to=upload_location , default='account/img/default.jpg')
    date_joined     =  models.DateTimeField(auto_now_add = True)
    last_login      =  models.DateTimeField(auto_now=True)
    is_active       =  models.BooleanField(default=True)
    is_staff        =  models.BooleanField(default=False)
    is_admin        =  models.BooleanField(default=False)
    is_superuser    =  models.BooleanField(default=False)
    
    
             
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


