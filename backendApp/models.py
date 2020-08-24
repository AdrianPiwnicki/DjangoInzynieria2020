from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Produkty(models.Model):
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
    grafika = models.FileField(blank=True, null=True)
    kategoria = models.CharField(choices=Kategorie.choices, default=Kategorie.Inne, max_length=20)
    popularnosc = models.IntegerField(default=0)

    def __str__(self):
        return self.nazwa + " (" + str(self.kategoria) + ")"


class Skladniki(models.Model):
    class Przelicznik(models.TextChoices):
        Sztuki = 'szt'
        Kilogram = 'kg'
        Dekagram = 'dag'
        Gram = 'g'
        Litr = 'l'
        Mililitr = 'ml'
        Szczypta = 'szczypta'

    produkt = models.ForeignKey(Produkty, on_delete=models.CASCADE)
    ilosc = models.FloatField(null=True)
    przelicznik = models.CharField(choices=Przelicznik.choices, default=Przelicznik.Sztuki, max_length=20)

    def __str__(self):
        return self.produkt.nazwa + " (" + str(self.ilosc) + " " + self.przelicznik + ")"


class Przepisy(models.Model):
    nazwa = models.CharField(max_length=100, null=False)
    przygotowanie = models.TextField()
    czas = models.IntegerField()
    photo = models.FileField(blank=True, null=True)
    skladniki = models.ManyToManyField(Skladniki)

    def __str__(self):
        return self.nazwa + " - " + str(self.czas) + " minut"


@receiver(post_save, sender=Przepisy)
def przepisy_produkty(sender, instance, **kwargs):
    for i in instance.skladniki.all():
        i.produkt.popularnosc += 1
        i.produkt.save()
