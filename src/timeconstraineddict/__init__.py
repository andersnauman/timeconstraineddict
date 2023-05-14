#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Time contrained dictionary """

from threading import Lock
from collections.abc import Mapping
from time import time

class TimeConstrainedDict(dict, Mapping):
    """
    Usage:
    
    from timeconstraineddict import TimeConstrainedDict as tdict

    # Set value to expire in 2 seconds
    d = tdict()
    d["key"] = "value", 2

    # Set the tuple ("value", 20) to expire in 2 seconds
    d = tdict()
    d["key"] = "value", 20, 2

    # Set the default expire time to 5 minutes
    d = tdict(300)
    d["key"] = "value"    
    """
    def __init__(self, max_age=60):
        self.max_age = float(max_age)

        self.lock = Lock()

        dict.__init__(self)

    def __contains__(self, key):
        with self.lock:
            try:
                _, value_time = dict.__getitem__(self, key)
            except KeyError:
                return False

            if time() >= value_time:
                dict.__delitem__(self, key)
                return False
        return True

    def __setitem__(self, key, value, age = 0):
        """
        Assume the last entry in the tuple is the age limit.
        (value, age)
        (value, value, age)
        Use 0 as the last value if tuple is used but the max_age should be honored
        (value, value, 0) = max/default age
        """
        if isinstance(value, tuple):
            # Large drawback by assuming the last int/float is a age limit.
            # TODO: Be creative and less assuming
            if isinstance(value[-1:][0], (int, float)):
                age, = value[-1:]
                value = value[:-1] if len(value[:-1]) > 1 else value[:-1][0]
            else:
                value = value[0] if isinstance(value, list) else value
            if age == 0 or age > self.max_age:
                age = self.max_age
        else:
            age = self.max_age
        age = time() + float(age)

        with self.lock:
            dict.__setitem__(self, key, (value, age))

    def __getitem__(self, key):
        with self.lock:
            # Do not catch exception.
            # Dict suppose to return KeyError if key is not found
            values = dict.__getitem__(self, key)
            value = values[:-1] if len(values[:-1]) > 1 else values[:-1][0]
            value_time, = values[-1:]
            if time() >= value_time:
                dict.__delitem__(self, key)
                raise KeyError(key)
        return value

    def __len__(self):
        return dict.__len__(self)

    def __iter__(self):
        for item in dict.__iter__(self):
            yield item

    def items(self):
        result = []
        with self.lock:
            now = time()
            for key, (value, value_time) in dict(self).items():
                if now >= value_time:
                    dict.__delitem__(self, key)
                    continue
                result.append((key, value))
        return result

    def values(self):
        result = []
        with self.lock:
            now = time()
            for key, (value, value_time) in dict(self).items():
                if now >= value_time:
                    dict.__delitem__(self, key)
                    continue
                result.append(value)
        return result

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "{}".format({k: v[:-1] if isinstance(v, list) and len(v[:-1]) > 1 else v for k, v in dict(self).items()})
