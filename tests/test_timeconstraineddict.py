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
