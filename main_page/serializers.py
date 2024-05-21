from rest_framework import serializers
from . import models


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exercise
        fields = ['name', 'image']



    def get_names(self, obj):
        return obj.name
    def get_images(self, obj):
        return obj.image.url


class CardSetSerializer(serializers.ModelSerializer):
    exercises = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.CardSet
        fields = ['id', 'name', 'exercises']
