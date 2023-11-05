from typing import TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseQuerySet(models.QuerySet[T]):
    ...
