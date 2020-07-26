from django import forms
from django.contrib.auth.forms import UserCreationForm as RegForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from account.models import User
from safe_filefield.forms import SafeFileField

class UserCreationForm(RegForm):
    email = forms.EmailField(max_length=60, help_text='Required. Enter a valid email address')
    photo = SafeFileField(widget=forms.FileInput(), allowed_extensions=('png','jpg','jpeg','bmp'), check_content_type=True)
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','password1','password2','photo')
    

    def clean_image(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            photo.save()
        else:
            raise forms.ValidationError('Please Upload a profile photo.')

        return photo


    def clean_first_name(self):
        # Get the email
        first_name = self.cleaned_data.get('first_name')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(first_name=first_name)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return first_name

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This first name  is already in use.')

    def clean_last_name(self):
        # Get the email
        last_name = self.cleaned_data.get('last_name')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(last_name=last_name)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return last_name

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This last name is already in use.')

    def clean_username(self):
        # Get the email
        username = self.cleaned_data.get('username')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(username=username)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This username is already in use.')

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is not available.')

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label="password")
    

    class Meta:
        model = User
        fields = ('email','password')

    def clean(self): 

        email = self.cleaned_data.get('email', None)
        if email:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid email or password")
        else:
            raise forms.ValidationError("Invalid email or password")

        return None
        
        

        

class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','photo','password')
    
    def clean_password(self):
        #Regardlesss of what the user provides, return the nitial value.
        #this is done here, rather that on the field, because the
        #field does not have access to the initial values
        return self.initial["password"]

    
class UserProfileEdithForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileEdithForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        
        
    photo = SafeFileField(widget=forms.FileInput(), allowed_extensions=('png','jpg','jpeg','bmp'), check_content_type=True)
    email = forms.CharField(widget=forms.TextInput(attrs={}))
    
    
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','photo')

    

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(email=email)
            except User.DoesNotExist:
                return email

            raise forms.ValidationError('Email "%s" is not available or taken.' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            except User.DoesNotExist:
                return username

            raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean_first_name(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(first_name=first_name)
            except User.DoesNotExist:
                return first_name

            raise forms.ValidationError('First Name "%s" is already in use.' % first_name)
    
    def clean_last_name(self):
        if self.is_valid():
            last_name = self.cleaned_data['last_name']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(last_name=last_name)
            except User.DoesNotExist:
                return last_name

            raise forms.ValidationError('Last Name "%s" is already in use.' % last_name)



    
        

    

        
        
        

    


    




