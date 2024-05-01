from django.db import models


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
    cards = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name
