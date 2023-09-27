from typing import TYPE_CHECKING

from store_kit.common.managers import BaseQuerySet

if TYPE_CHECKING:
    from .models import Unit  # noqa


class UnitQuerySet(BaseQuerySet["Unit"]):
    ...
