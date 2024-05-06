from django.db import models
import uuid


class Exercise(models.Model):
    """
    Класс "Упражнения
    """
    name = models.CharField("Название упражнения", max_length=250)
    image = models.ImageField("Изображение", upload_to='img/')

    def __str__(self):
        return self.name


class CardSet(models.Model):
    """
    Класс "Набор карточек"

    """
    name = models.CharField("Название набора", max_length=250)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name


class GameSession(models.Model):
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def get_session_url(self):
        return f"http://127.0.0.1:8000/game_session/{self.session_id}"

    def __str__(self):
        return str(self.session_id)
