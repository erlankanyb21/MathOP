from django.db import models

# Create your models here.
class MathOperation(models.Model):
    operation = models.CharField(max_length=255)
    expression = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    numerical_result = models.CharField(max_length=255, null=True, blank=True)
    upper_limit = models.CharField(max_length=255, null=True, blank=True)
    lower_limit = models.CharField(max_length=255, null=True, blank=True)
    x_value = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    prompt = models.CharField(max_length=255)
    bitmap = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    is_from_user = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)