from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator
from django.db import models
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from .validators import size_validator


class Drone(models.Model):
    # Validators
    BATTERY_CAPACITY_VALIDATORS = (
        MinValueValidator(0, _("The minimum percentage allowed is 0.")),
        MaxValueValidator(100, _("The maximum percentage allowed is 100."))
    )

    MODEL_CHOICES = [
        ('lightweight', 'Lightweight'),
        ('middleweight', 'Middleweight'),
        ('cruiserweight', 'Cruiserweight'),
        ('heavyweight', 'Heavyweight')
    ]
    STATE_IDLE = 'idle'
    STATE_LOADING = 'loading'
    STATE_LOADED = 'loaded'
    STATE_DELIVERING = 'delivering'
    STATE_DELIVERED = 'delivered'
    STATE_RETURNING = 'returning'
    STATE_CHOICES = [
        (STATE_IDLE, 'IDLE'), (STATE_LOADING, 'LOADING'), (STATE_LOADED, 'LOADED'),
        (STATE_DELIVERING, 'DELIVERING'), (STATE_DELIVERED, 'DELIVERED'), (STATE_RETURNING, 'RETURNING')
    ]

    # Fields
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=15, choices=MODEL_CHOICES)
    weight_limit = models.PositiveSmallIntegerField(validators=[MaxValueValidator(500, _("The maximum weight limit of a drone is 500gr."))])
    battery_capacity = models.PositiveSmallIntegerField(validators=BATTERY_CAPACITY_VALIDATORS)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    class Meta:
        ordering = ['-battery_capacity']


class Medication(models.Model):
    # Validators
    NAME_VALIDATOR = RegexValidator(_lazy_re_compile(r'^[a-zA-Z0-9-_]+$'),
                                    message=_('It is only allowed letters, numbers, "-" and "_".'),
                                    code='not_allowed_characters')
    CODE_VALIDATOR = RegexValidator(_lazy_re_compile(r'^[A-Z0-9_]+$'),
                                    message=_('It is only allowed upper-case letters, numbers and "_".'),
                                    code='not_allowed_characters')
    WEIGHT_VALIDATOR = MinValueValidator(1, _("The minimum weight allowed is 1g."))

    # Fields
    name = models.CharField(max_length=100, validators=[NAME_VALIDATOR])
    weight = models.FloatField(validators=[WEIGHT_VALIDATOR])
    code = models.CharField(max_length=100, validators=[CODE_VALIDATOR])
    image = models.ImageField(upload_to='medication_pictures/%Y/%m/%d/', max_length=100, validators=[size_validator])
    drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']
