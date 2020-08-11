from django.db import models

class Produkty(models.Model):
    class Przeliczniki(models.TextChoices):
        kilogram = 'kg'
        dekagram = 'dag'
        gram = 'g'
        sztuki = 'szt'
        litr = 'l'
        mililitr = 'ml'
        szczypta = 'szczypta'

    class Kategorie(models.TextChoices):
        Inne = 'inne'
        Owoce = 'owoce'
        Warzywa = 'warzywa'
        Zboza = 'zboża'
        Nabial = 'nabiał'
        Mieso = 'mięso'
        Ryby = 'ryby'
        Przyprawy = 'przyprawy'

    nazwa = models.CharField(max_length=50, null=False)
    przelicznik = models.CharField(choices=Przeliczniki.choices, default=Przeliczniki.kilogram, max_length=20)
    grafika = models.FileField(blank=True, null=True)
    kategoria = models.CharField(choices=Kategorie.choices, default=Kategorie.Inne, max_length=20)

    def __str__(self):
        return self.nazwa + " (" + str(self.kategoria) + ")"


class Przepisy(models.Model):
    nazwa = models.CharField(max_length=100, null=False)
    przygotowanie = models.TextField()
    czas = models.IntegerField()
    photo = models.FileField(blank=True, null=True)
    skladniki = models.ManyToManyField(Produkty)

    def __str__(self):
        return self.nazwa + " - " + str(self.czas) + " minut"
