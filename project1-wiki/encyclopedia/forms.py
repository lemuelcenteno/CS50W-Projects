from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea)


class EditEntryForm(forms.Form):
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea)
