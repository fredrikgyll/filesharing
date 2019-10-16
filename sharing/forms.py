from django import forms

from sharing.models import SharedFile


class FileForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = (
            'file',
            'password',
            'message',
            'short_identifier',
            'burn_after_open',
            'burn_after',
        )
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': 'Optional password'}),
            'short_identifier': forms.TextInput(
                attrs={'placeholder': 'Optional short url slug'}
            ),
            'message': forms.Textarea(
                attrs={'placeholder': 'Message to be shown to recipient'}
            ),
            'burn_after_open': forms.CheckboxInput(attrs={'label': ''}),
        }

    def save(self, commit=True):
        m = super(FileForm, self).save(commit=False)
        pwd = self.cleaned_data.get('password', '')
        if pwd:
            m.set_password(pwd, commit=False)
        if commit:
            m.save()
        return m


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
