#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from timeconstraineddict import TimeConstrainedDict as tdict

from time import sleep

def test_normal_dict():
    assert tdict(3) == dict()

def test_normal_dict_append():
    d = tdict()
    d["test-key"] = "test-value"
    assert d["test-key"] == "test-value"

def test_timed_value_exist():
    d = tdict()
    d["test-key"] = "test-value", 0.2
    sleep(0.1)
    assert "test-key" in d

def test_timed_value_tuple_exist():
    d = tdict()
    d["test-key"] = "test-value", 40, 0.2
    sleep(0.1)
    assert "test-key" in d and d["test-key"] == ("test-value", 40)    

def test_timed_value_expire():
    d = tdict()
    d["test-key"] = "test-value", 0.2
    sleep(0.3)
    assert "test-key" not in d

def test_timed_value_max_age_exist():
    d = tdict(0.1)
    d["test-key"] = "test-value", 0.3
    assert "test-key" in d

def test_timed_value_max_age_expire():
    d = tdict(0.1)
    d["test-key"] = "test-value", 0.3
    sleep(0.2)
    assert "test-key" not in d
