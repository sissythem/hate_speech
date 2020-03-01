from rest_framework import serializers

from hate_speech_detection.models import Dataset, Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ["id", "text", "preprocessed_text", "label", "dataset"]
        depth = 1


class DatasetSerializer(serializers.ModelSerializer):
    """
    Class used to serialize an ExperimentGroup object. All the declared fields in the models.py are included in this
    serializer.
    """
    tweets = TweetSerializer(source='get_tweets', many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ["id", "name", "num_labels", "language", "label1", "label2", "tweets"]
        depth = 1
