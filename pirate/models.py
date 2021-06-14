from django.db import models

# Create your models here.
class Pirate(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    bounty = models.IntegerField(default=0)

    def __str__(self):
        return self.name
