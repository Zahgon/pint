from __future__ import annotations

import contextlib
import doctest
import math
import os
import pathlib
import unittest
import warnings

from pint import UnitRegistry
from pint.testsuite.helpers import PintOutputChecker


class QuantityTestCase:
    kwargs = {}

    @classmethod
    def setup_class(cls):
        cls.ureg = UnitRegistry(**cls.kwargs)
        cls.Q_ = cls.ureg.Quantity
        cls.U_ = cls.ureg.Unit

    @classmethod
    def teardown_class(cls):
        cls.ureg = None
        cls.Q_ = None
        cls.U_ = None


@contextlib.contextmanager
def assert_no_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("error")

        yield


def testsuite():
    """A testsuite that has all the pint tests."""
    pass


def main():
    """Runs the testsuite as command line application."""
    try:
        unittest.main()
    except Exception as e:
        print("Error: %s" % e)


def run():
    """Run all tests.

    :return: a :class:`unittest.TestResult` object

    Parameters
    ----------

    Returns
    -------

    """
    pass


_GLOBS = {
    "wrapping.rst": {
        "pendulum_period": lambda length: 2 * math.pi * math.sqrt(length / 9.806650),
        "pendulum_period2": lambda length, swing_amplitude: 1.0,
        "pendulum_period_maxspeed": lambda length, swing_amplitude: (1.0, 2.0),
        "pendulum_period_error": lambda length: (1.0, False),
    }
}


def add_docs(suite):
    """Add docs to suite

    Parameters
    ----------
    suite :


    Returns
    -------

    """
    pass


def test_docs():
    suite = unittest.TestSuite()
    add_docs(suite)
    runner = unittest.TextTestRunner()
    return runner.run(suite)
