from django.db.models import TextChoices


class UnitType(TextChoices):
    PIECES = "pieces", "Pieces"
    WEIGHT = "weight", "Weight"
    VOLUME = "volume", "Volume"
    LENGTH = "length", "Length"
    USAGE = "usage", "Usage"
