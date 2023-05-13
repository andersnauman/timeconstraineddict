#!/usr/bin/env python3tcdd
# -*- coding: utf-8 -*-

""" Test module """

from time import sleep

from timeconstraineddict import TimeConstrainedDict as tdict

def test_normal_dict():
    """ Test a normal dictionary """
    assert isinstance(tdict(), tdict) and isinstance(tdict(), dict) and not tdict()

def test_normal_dict_append():
    """ Test a normal dictionary append """
    tcd = tdict()
    tcd["test-key"] = "test-value"
    assert tcd["test-key"] == "test-value"

def test_timed_value_exist():
    """ Test if timed value still exist """
    tcd = tdict()
    tcd["test-key"] = "test-value", 0.2
    sleep(0.1)
    assert "test-key" in tcd

def test_timed_value_tuple_exist():
    """ Test if a tuple still exist """
    tcd = tdict()
    tcd["test-key"] = "test-value", 40, 0.2
    sleep(0.1)
    assert "test-key" in tcd and tcd["test-key"] == ("test-value", 40)

def test_timed_value_expire():
    """ Test if a value have been expired """
    tcd = tdict()
    tcd["test-key"] = "test-value", 0.2
    sleep(0.3)
    assert "test-key" not in tcd

def test_timed_value_max_age_exist():
    """ Test if the max age can overwrite higher input values """
    tcd = tdict(0.1)
    tcd["test-key"] = "test-value", 0.3
    assert "test-key" in tcd

def test_timed_value_max_age_expire():
    """ Test if the max age overwrites higher input values """
    tcd = tdict(0.1)
    tcd["test-key"] = "test-value", 0.3
    sleep(0.2)
    assert "test-key" not in tcd

def test_enumerate():
    """ Test if enumerate works """
    tcd = tdict()
    tcd["test-key"] = "test-value"
    for i, key in enumerate(tcd):
        assert key
        assert isinstance(i, int)
        continue

def test_zip():
    """ Test if you can combine a time constrained dict and a normal one """
    tcd = tdict()
    tcd["test-key"] = "test-value"
    for dict1, dict2 in zip(tcd, {"test-key2": "test-value2"}):
        assert dict1
        assert dict2
        continue

def test_unpack():
    """ Test if dictionary unpack is done properly. Obviously the timer will not be passed on since it gets converted to a pure dictionary. """
    dict1 = tdict()
    dict1["test-key"] = "test-value"
    dict2 = {"test-key2": "test-value2"}

    # Next line should yield {'test-key': 'test-value'}, not {'test-key': ('test-value', 1684006565.8971586)}
    assert not {**dict1}

    dict3 = {**dict1, **dict2}
    assert "test-key" in dict3 and dict3["test-key"] == "test-value"

