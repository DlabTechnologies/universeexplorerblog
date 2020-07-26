from django import forms
from .models import Post, Comment, ContactForm, NewsletterSignup
from safe_filefield.forms import SafeFileField


class PostCreationForm(forms.ModelForm):
    image = SafeFileField(widget=forms.FileInput(), allowed_extensions=('png','jpg','jpeg','bmp'), check_content_type=True)
   
    
    class Meta:
        model = Post

        fields = (
            'title',
            'body',
            'status',
            'image',
            'restrict_comment',
            'tags',
        )
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            return image
        else:
            raise forms.ValidationError('Please Upload a photo for this post.')

        


class PostEdithForm(forms.ModelForm):
    

    image = SafeFileField(widget=forms.FileInput(), allowed_extensions=('png','jpg','jpeg','bmp'), check_content_type=True, required=False)
    def __init__(self, *args, **kwargs):
        super(PostEdithForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False  
        
    
    class Meta:
        model = Post

        fields = (
            'title',
            'body',
            'status',
            'image',
            'restrict_comment',
            'tags',
        )

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comments here', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields =('content',)




class UserContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ('name','email','message',)


class UserNewsletterSignup(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ('email', )


class SendEmailForm(forms.Form):
    

    to = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())


