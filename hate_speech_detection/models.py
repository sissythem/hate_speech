import json

from django.db import models
from django.forms.models import model_to_dict


# Create your models here.
class Dataset(models.Model):

    class Meta:
        db_table = "datasets"

    id = models.AutoField(primary_key=True, unique=True)
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
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=1000)
    preprocessed_text = models.CharField(max_length=1000)
    label = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset, related_name="tweets", on_delete=models.CASCADE)

    def __str__(self):
        """
        Overrides the __str__ object method to show all the object fields & values as strings.

        Returns
            str: string containing all the class fields and their values
        """
        obj = model_to_dict(self)
        return json.dumps(obj)
