from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label="E-Posta Adresiniz:")
    subject = forms.CharField(required=True, label="Konu:")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Mesjaınız:")
