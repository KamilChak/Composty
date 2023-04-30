from django.db import models

# Create your models here.

class Compost(models.Model):
    
    COMPOST_TYPES = (
        ('AnimalManure', 'Animal manure'),
        ('PlantFertilizers', 'Plant-based fertilizers'),
        ('BiodegradableFertilizers', 'Biodegradable fertilizers'),
    )
    
    CompostName = models.CharField(max_length=255)
    CompostImage = models.FileField(upload_to='composts/', null=True, blank=True)
    CompostType = models.CharField(max_length=30, choices=COMPOST_TYPES)

    def __str__(self):
        return self.CompostName



