from django import forms
from comments.models import chat

class chatForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)

	class Meta:
		model = chat
		fields = ('body',)
