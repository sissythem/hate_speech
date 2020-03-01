import json

from django.db import models
from django.forms.models import model_to_dict


# Create your models here.
class Dataset(models.Model):

    class Meta:
        db_table = "datasets"

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    num_labels = models.IntegerField()
    language = models.CharField(max_length=255)
    label1 = models.CharField(max_length=255)
    label2 = models.CharField(max_length=255)

    def __str__(self):
        """
        Overrides the __str__ object method to show all the object fields & values as strings.

        Returns
            str: string containing all the class fields and their values
        """
        obj = model_to_dict(self)
        return json.dumps(obj)

    def get_tweets(self):
        return Tweet.objects.filter(dataset=self)


class Tweet(models.Model):
    class Meta:
        db_table = "tweets"

    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=4000)
    preprocessed_text = models.CharField(max_length=4000)
    label = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset, related_name="tweets", on_delete=models.CASCADE)

    def get_features(self):
        return Feature.objects.filter(tweet=self)

    def __str__(self):
        """
        Overrides the __str__ object method to show all the object fields & values as strings.

        Returns
            str: string containing all the class fields and their values
        """
        obj = model_to_dict(self)
        return json.dumps(obj)


class Feature(models.Model):

    class Meta:
        db_table = "features"

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    tweet = models.ForeignKey(Tweet, related_name="features", on_delete=models.CASCADE)
    folder_path = models.CharField(max_length=4000)
    filename = models.CharField(max_length=1000)
