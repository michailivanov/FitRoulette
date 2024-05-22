from rest_framework import serializers
from . import models


class ExerciseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.Exercise
        fields = ['name', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    def get_names(self, obj):
        return obj.name
    def get_images(self, obj):
        return obj.image.url


class CardSetSerializer(serializers.ModelSerializer):
    exercises = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.CardSet
        fields = ['id', 'name', 'exercises']


class GameSessionSerializer(serializers.ModelSerializer):
    game = serializers.SerializerMethodField()
    class Meta:
        model = models.GameSession
        fields = ['game']

    def get_game(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/game_session/{obj.session_id}/')