from django.contrib import admin

from .models import MathOperation, Chat, AudioFile
# Register your models here.
admin.site.register(MathOperation)
admin.site.register(Chat)
admin.site.register(AudioFile)
