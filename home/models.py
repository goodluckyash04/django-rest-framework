from django.db import models


class Color(models.Model):
    color_name = models.CharField(primary_key=True, max_length=15)
    color_hash = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.color_name.upper()


# Create your models here.
class Person(models.Model):
    person_name = models.CharField(max_length=100)
    age = models.IntegerField()
    fav_color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="fav_color",
    )

    def __str__(self) -> str:
        return self.person_name
