from django.db import models

class Produkty(models.Model):
    # class Przeliczniki(models.TextChoices):
    #     kilogram = 'kg'
    #     dekagram = 'dag'
    #     gram = 'g'
    #     sztuki = 'szt'
    #     litr = 'l'
    #     mililitr = 'ml'
    KILO = 'kilogram'
    PRZELICZNIKI = [
        ('kilogram' , 'kg'),
        ('gram' , 'g')
    ]

    # class Kategorie(models.TextChoices):
    #     Pozostale = 'pozostałe'
    #     Owoce = 'owoce'
    #     Warzywa = 'warzywa'
    #     Zboza = 'zboża'
    #     Nabial = 'nabiał'

    OWOCE = 'owoce'
    KATEGORIE = [
        ('owoce', 'owoce'),
        ('warzywa', 'warzywa')
    ]

    nazwa = models.CharField(max_length=50, null=False)
    przelicznik = models.CharField(choices=PRZELICZNIKI, default=KILO, max_length=20)
    grafika = models.FileField(blank=True, null=True)
    kategoria = models.CharField(choices=KATEGORIE, default=OWOCE, max_length=20)

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
