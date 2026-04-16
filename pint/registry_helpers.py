"""
pint.registry_helpers
~~~~~~~~~~~~~~~~~~~~~

Miscellaneous methods of the registry written as separate functions.

:copyright: 2016 by Pint Authors, see AUTHORS for more details..
:license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterable
from inspect import Parameter, signature
from itertools import zip_longest
from typing import TYPE_CHECKING, Any, TypeVar

from ._typing import F
from .errors import DimensionalityError
from .util import UnitsContainer, to_units_container

if TYPE_CHECKING:
    from ._typing import Quantity, Unit
    from .registry import UnitRegistry

T = TypeVar("T")


def _replace_units(original_units, values_by_name):
    """Convert a unit compatible type to a UnitsContainer.

    Parameters
    ----------
    original_units :
        a UnitsContainer instance.
    values_by_name :
        a map between original names and the new values.

    Returns
    -------

    """
    pass


def _to_units_container(a, registry=None):
    """Convert a unit compatible type to a UnitsContainer,
    checking if it is string field prefixed with an equal
    (which is considered a reference)

    Parameters
    ----------
    a :

    registry :
         (Default value = None)

    Returns
    -------
    UnitsContainer, bool


    """
    pass


def _parse_wrap_args(args, registry=None):
    # Arguments which contain definitions
    # (i.e. names that appear alone and for the first time)
    defs_args = set()
    defs_args_ndx = set()

    # Arguments which depend on others
    dependent_args_ndx = set()

    # Arguments which have units.
    unit_args_ndx = set()

    # _to_units_container
    args_as_uc = [_to_units_container(arg, registry) for arg in args]

    # Check for references in args, remove None values
    for ndx, (arg, is_ref) in enumerate(args_as_uc):
        if arg is None:
            continue
        elif is_ref:
            if len(arg) == 1:
                [(key, value)] = arg.items()
                if value == 1 and key not in defs_args:
                    # This is the first time that
                    # a variable is used => it is a definition.
                    defs_args.add(key)
                    defs_args_ndx.add(ndx)
                    args_as_uc[ndx] = (key, True)
                else:
                    # The variable was already found elsewhere,
                    # we consider it a dependent variable.
                    dependent_args_ndx.add(ndx)
            else:
                dependent_args_ndx.add(ndx)
        else:
            unit_args_ndx.add(ndx)

    # Check that all valid dependent variables
    for ndx in dependent_args_ndx:
        arg, is_ref = args_as_uc[ndx]
        if not isinstance(arg, dict):
            continue
        if not set(arg.keys()) <= defs_args:
            raise ValueError(
                "Found a missing token while wrapping a function: "
                "Not all variable referenced in %s are defined using !" % args[ndx]
            )

    def _converter(ureg, sig, values, kw, strict):
        len_initial_values = len(values)

        # pack kwargs
        for i, param_name in enumerate(sig.parameters):
            if i >= len_initial_values:
                values.append(kw[param_name])

        values_by_name = {}

        # first pass: Grab named values
        for ndx in defs_args_ndx:
            value = values[ndx]
            values_by_name[args_as_uc[ndx][0]] = value
            values[ndx] = getattr(value, "_magnitude", value)

        # second pass: calculate derived values based on named values
        for ndx in dependent_args_ndx:
            value = values[ndx]
            assert _replace_units(args_as_uc[ndx][0], values_by_name) is not None
            values[ndx] = ureg._convert(
                getattr(value, "_magnitude", value),
                getattr(value, "_units", UnitsContainer({})),
                _replace_units(args_as_uc[ndx][0], values_by_name),
            )

        # third pass: convert other arguments
        for ndx in unit_args_ndx:
            if isinstance(values[ndx], ureg.Quantity):
                values[ndx] = ureg._convert(
                    values[ndx]._magnitude, values[ndx]._units, args_as_uc[ndx][0]
                )
            else:
                if strict:
                    if isinstance(values[ndx], str):
                        # if the value is a string, we try to parse it
                        tmp_value = ureg.parse_expression(values[ndx])
                        values[ndx] = ureg._convert(
                            tmp_value._magnitude, tmp_value._units, args_as_uc[ndx][0]
                        )
                    else:
                        raise ValueError(
                            "A wrapped function using strict=True requires "
                            "quantity or a string for all arguments with not None units. "
                            "(error found for {}, {})".format(
                                args_as_uc[ndx][0], values[ndx]
                            )
                        )

        # unpack kwargs
        for i, param_name in enumerate(sig.parameters):
            if i >= len_initial_values:
                kw[param_name] = values[i]

        return values[:len_initial_values], kw, values_by_name

    return _converter


def _apply_defaults(sig, args, kwargs):
    """Apply default keyword arguments.

    Named keywords may have been left blank. This function applies the default
    values so that every argument is defined.
    """
    pass


def wraps(
    ureg: UnitRegistry,
    ret: str | Unit | Iterable[str | Unit | None] | None,
    args: str | Unit | Iterable[str | Unit | None] | None,
    strict: bool = True,
) -> Callable[[Callable[..., Any]], Callable[..., Quantity]]:
    """Wraps a function to become pint-aware.

    Use it when a function requires a numerical value but in some specific
    units. The wrapper function will take a pint quantity, convert to the units
    specified in `args` and then call the wrapped function with the resulting
    magnitude.

    The value returned by the wrapped function will be converted to the units
    specified in `ret`.

    Parameters
    ----------
    ureg : pint.UnitRegistry
        a UnitRegistry instance.
    ret : str, pint.Unit, or iterable of str or pint.Unit
        Units of each of the return values. Use `None` to skip argument conversion.
    args : str, pint.Unit, or iterable of str or pint.Unit
        Units of each of the input arguments. Use `None` to skip argument conversion.
    strict : bool
        Indicates that only quantities are accepted. (Default value = True)

    Returns
    -------
    callable
        the wrapper function.

    Raises
    ------
    TypeError
        if the number of given arguments does not match the number of function parameters.
        if any of the provided arguments is not a unit a string or Quantity

    """
    pass


def check(
    ureg: UnitRegistry, *args: str | UnitsContainer | Unit | None
) -> Callable[[F], F]:
    """Decorator to for quantity type checking for function inputs.

    Use it to ensure that the decorated function input parameters match
    the expected dimension of pint quantity.

    The wrapper function raises:
      - `pint.DimensionalityError` if an argument doesn't match the required dimensions.

    ureg : UnitRegistry
        a UnitRegistry instance.
    args : str or UnitContainer or None
        Dimensions of each of the input arguments.
        Use `None` to skip argument conversion.

    Returns
    -------
    callable
        the wrapped function.

    Raises
    ------
    TypeError
        If the number of given dimensions does not match the number of function
        parameters.
    ValueError
        If the any of the provided dimensions cannot be parsed as a dimension.
    """
    pass
