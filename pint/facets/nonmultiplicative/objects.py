"""
pint.facets.nonmultiplicative.objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2022 by Pint Authors, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

from typing import Generic

from ..plain import MagnitudeT, PlainQuantity, PlainUnit


class NonMultiplicativeQuantity(Generic[MagnitudeT], PlainQuantity[MagnitudeT]):
    @property
    def _is_multiplicative(self) -> bool:
        """Check if the PlainQuantity object has only multiplicative units."""
        return not self._get_non_multiplicative_units()

    def _get_non_multiplicative_units(self) -> list[str]:
        """Return a list of the of non-multiplicative units of the PlainQuantity object."""
        return [
            unit
            for unit in self._units
            if not self._get_unit_definition(unit).is_multiplicative
        ]

    @property
    def _is_logarithmic(self) -> bool:
        """Check if the PlainQuantity object has logarithmic units."""
        pass

    def _get_delta_units(self) -> list[str]:
        """Return list of delta units ot the PlainQuantity object."""
        pass

    def _has_compatible_delta(self, unit: str) -> bool:
        """ "Check if PlainQuantity object has a delta_unit that is compatible with unit"""
        pass

    def _ok_for_muldiv(self, no_offset_units: int | None = None) -> bool:
        """Checks if PlainQuantity object can be multiplied or divided"""
        pass


class NonMultiplicativeUnit(PlainUnit):
    pass
