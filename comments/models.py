from django.db import models
from rec.models import Review
from django.contrib.auth.models import User


class chat(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
    
    


