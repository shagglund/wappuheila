from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class ChangeUserDetailsForm(ModelForm):
    
    class Meta:
        model = User;
        fields = ('username','first_name','last_name')
    
class UserCreationFormUniqueEmail(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']