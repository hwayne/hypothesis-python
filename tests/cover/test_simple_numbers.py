# coding=utf-8

# Copyright (C) 2013-2015 David R. MacIver (david@drmaciver.com)

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# END HEADER

from __future__ import division, print_function, absolute_import, \
    unicode_literals

import sys
import math

import pytest
from hypothesis import find, assume
from hypothesis.specifiers import integers_from, integers_in_range


def test_minimize_negative_int():
    assert find(int, lambda x: x < 0) == -1
    assert find(int, lambda x: x < -1) == -2


def test_positive_negative_int():
    assert find(int, lambda x: x > 0) == 1
    assert find(int, lambda x: x > 1) == 2


boundaries = pytest.mark.parametrize('boundary', [0, 1, 11, 23, 64, 10000])


@boundaries
def test_minimizes_int_down_to_boundary(boundary):
    assert find(int, lambda x: x >= boundary) == boundary


@boundaries
def test_minimizes_int_up_to_boundary(boundary):
    assert find(int, lambda x: x <= -boundary) == -boundary


@boundaries
def test_minimizes_ints_from_down_to_boundary(boundary):
    assert find(
        integers_from(boundary - 10), lambda x: x >= boundary) == boundary


def test_negative_floats_simplify_to_zero():
    assert find(float, lambda x: x <= -1.0) == -1.0


def test_find_infinite_float_is_positive():
    assert find(float, math.isinf) == float('inf')


def test_minimize_nan():
    assert math.isnan(find(float, math.isnan))


def test_minimize_very_large_float():
    t = sys.float_info.max / 2
    assert t <= find(float, lambda x: x >= t) < float('inf')


def test_list_of_fractional_float():
    assert set(find(
        [float], lambda x: len([t for t in x if t >= 1.5]) >= 10
    )) in (
        {1.5},
        {1.5, 2.0}
    )


def test_minimal_fractional_float():
    assert find(float, lambda x: x >= 1.5) in (1.5, 2.0)