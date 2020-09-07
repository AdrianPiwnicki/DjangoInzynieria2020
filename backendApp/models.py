from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Products(models.Model):
    class Category(models.TextChoices):
        Inne = 'inne'
        Owoce = 'owoce'
        Warzywa = 'warzywa'
        Zboza = 'zboża'
        Nabial = 'nabiał'
        Mieso = 'mięso'
        Ryby = 'ryby'
        Przyprawy = 'przyprawy'

    name = models.CharField(max_length=50, null=False)
    graphics = models.FileField(blank=True, null=True)
    category = models.CharField(choices=Category.choices, default=Category.Inne, max_length=20)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + str(self.category) + ")"


class Ingredients(models.Model):
    class Converter(models.TextChoices):
        Sztuki = 'szt'
        Kilogram = 'kg'
        Dekagram = 'dag'
        Gram = 'g'
        Litr = 'l'
        Mililitr = 'ml'
        Szczypta = 'szczypta'

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    converter = models.CharField(choices=Converter.choices, default=Converter.Sztuki, max_length=20)

    def __str__(self):
        return self.product.name + " (" + str(self.quantity) + " " + self.converter + ")"


class Recipes(models.Model):
    name = models.CharField(max_length=100, null=False)
    preparation = models.TextField()
    time = models.IntegerField()
    photo = models.FileField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.name + " - " + str(self.time) + " minut"


@receiver(post_save, sender=Recipes)
def przepisy_produkty(sender, instance, **kwargs):
    for i in instance.ingredients.all():
        i.product.popularity += 1
        i.product.save()
