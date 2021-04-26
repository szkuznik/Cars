from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    make = models.CharField(_("Make"), max_length=200)
    model = models.CharField(_("Make"), max_length=200)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def __str__(self):
        return f'{self.make} {self.model}'

    @property
    def avg_rating(self):
        return self.carrating_set.aggregate(Avg('rating'))['rating__avg']


class CarRating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(_('Rating'), choices=list(zip(range(1, 6), range(1, 6))))

    class Meta:
        verbose_name = _("Car rating")
        verbose_name_plural = _("Car ratings")

    def __str__(self):
        return f'{self.car} rating: {self.rating}'
