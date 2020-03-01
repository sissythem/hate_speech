from django.contrib import admin

from hate_speech_detection.models import Tweet, Dataset, Feature

# Register your models here.
admin.register(Dataset)
admin.register(Tweet)
admin.register(Feature)
