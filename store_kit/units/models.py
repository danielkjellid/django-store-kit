from django.db import models

from store_kit.common.models import BaseModel

from .enums import UnitType
from .managers import UnitQuerySet

_UnitManager = models.Manager.from_queryset(UnitQuerySet)


class Unit(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    name_pluralized = models.CharField(max_length=30, null=True)
    abbreviation = models.CharField(max_length=30, unique=True)
    unit_type = models.CharField(max_length=30, choices=UnitType.choices)
    base_factor = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    is_base_unit = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    objects = _UnitManager()

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.abbreviation})"

    class Meta:
        verbose_name = "unit"
        verbose_name_plural = "units"

    def __str__(self) -> str:
        return self.name
