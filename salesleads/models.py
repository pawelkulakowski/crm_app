from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

MARKETS = (
    (1, 'ME-DE'),
    (2, 'ME-IT'),
    (3, 'ME-NL'),
    (4, 'ME-PE'),
    (5, 'ME-RU')
)

SOURCES = (
    (1, 'targi'),
    (2, 'internet'),
    (3, 'linkedin'),
    (4, 'inne')
)

STATUS = (
    (1, 'Pierwsze zamówienie'),
    (2, 'Złożone warunki/oferta'),
    (3, 'Najbardziej obiecujące'),
    (4, 'Pozostałe Aktywności'),
    (5, 'Odrzucone')
)

SCORE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

TYPES = (
    (1, 'Nowy klient'),
    (2, 'Rozszerzenie oferty'),
    (3, 'Historyczny klient'),
)

ACTIVITIES = (
    (1, 'Kontakt telefoniczny'),
    (2, 'E-mail'),
    (3, 'Spotkanie')
)

POTENTIAL = (
    (1, 'do 5.000 Eur'),
    (2, '5.000 - 10.000 Eur'),
    (3, '10.000 - 25.000 Eur'),
    (4, '25.000 - 50.000 Eur'),
    (5, '50.000 - 75.000 Eur'),
    (6, '75.000 - 100.000 Eur'),
    (7, '100.000 - 125.000 Eur'),
    (8, '125.000 - 150.000 Eur'),
    (9, '150.000 - 200.000 Eur'),
    (10, '200.000 - 250.000 Eur'),
    (11, 'Powyżej 250.000 Eur')
)


class ExportUser(AbstractUser):
    market = models.IntegerField(choices=MARKETS, verbose_name='rynek', null=True, blank=True)

    def __str__(self):
        return self.username


class Country(models.Model):
    country = models.CharField(max_length=128)

    def __str__(self):
        return self.country

    class Meta:
        ordering = ['country']
        verbose_name = 'Kraj'
        verbose_name_plural = 'Kraje'


class SalesLead(models.Model):
    user = models.ForeignKey(ExportUser, null=True, blank=True, on_delete=models.PROTECT)
    type = models.IntegerField(choices=TYPES, null=True, verbose_name='Typ')
    status = models.IntegerField(choices=STATUS, null=True)
    company_name = models.CharField(max_length=65, null=True, verbose_name='Nazwa firmy')
    location = models.PointField(null=True, blank=True)
    latitude = models.CharField(null=True, blank=True, max_length=128, verbose_name='Wysokość')
    longtitude = models.CharField(null=True, blank=True, max_length=128, verbose_name='Szerokość')
    street = models.CharField(max_length=256, null=True, blank=True, verbose_name='Ulica')
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name='Miejscowość')
    postcode = models.IntegerField(null=True, blank=True, verbose_name='Kod pocztowy')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name='Kraj')
    company_website = models.URLField(null=True, blank=True, verbose_name='Strona www')
    source = models.IntegerField(choices=SOURCES, null=True, blank=True, verbose_name='Źródło')
    brands = models.CharField(max_length=256, null=True, blank=True, verbose_name='Referencje')
    potential = models.IntegerField(choices=POTENTIAL, null=True, blank=True, verbose_name='Potencjał')
    score = models.IntegerField(choices=SCORE, null=True, verbose_name='Ocena', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.company_name

    @property
    def lat_lng(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    class Meta:
        ordering = ['company_name']


class Comment(models.Model):
    saleslead = models.ForeignKey(SalesLead, on_delete=models.PROTECT, related_name='comment', null=True)
    comment = models.TextField(verbose_name='Komentarz', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created']


class ContactPerson(models.Model):
    saleslead = models.ForeignKey(SalesLead, on_delete=models.PROTECT, related_name='contacts')
    first_name = models.CharField(max_length=64, null=True, verbose_name='Imię', blank=True)
    last_name = models.CharField(max_length=128, null=True, verbose_name='Nazwisko', blank=True)
    position = models.CharField(max_length=128, null=True, verbose_name='Stanowisko', blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.IntegerField(null=True, verbose_name='Telefon', blank=True)
    whatsapp = models.IntegerField(null=True, verbose_name='WhatsApp', blank=True)
    linkedin_added = models.BooleanField(verbose_name='Kontakt Linkedin', null=True, blank=True)
    default = models.BooleanField(verbose_name='Kontakt domyślny', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PlannedActivities(models.Model):
    user = models.ForeignKey(ExportUser, null=True, blank=True, on_delete=models.PROTECT)
    saleslead = models.ForeignKey(SalesLead, on_delete=models.CASCADE, related_name='plannedactivities')
    date = models.DateField(null=True, blank=True, verbose_name='Data')
    activity_type = models.IntegerField(choices=ACTIVITIES, verbose_name='Forma działania')
    activity_comment = models.TextField(verbose_name='Dodatkowe informacje', null=True, blank=True)
    activity_done = models.BooleanField(null=True, verbose_name='Wykonane', default=False)
    history = HistoricalRecords()
    # def __str__(self):
    #     return str(self.activity_type[1])
