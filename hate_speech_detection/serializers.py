from rest_framework import serializers

from hate_speech_detection.models import Dataset, Tweet, Feature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "tweet", "folder_path", "filename"]
        depth = 1


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ["id", "text", "preprocessed_text", "label", "dataset"]
        depth = 1


class DatasetSerializer(serializers.ModelSerializer):
    tweets = TweetSerializer(source='get_tweets', many=True, read_only=True)
    features = FeatureSerializer(source="get_features", many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ["id", "name", "num_labels", "language", "label1", "label2", "tweets", "features"]
        depth = 1
