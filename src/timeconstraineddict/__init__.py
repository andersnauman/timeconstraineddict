#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock

from time import time

class TimeConstrainedDict(dict):
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
            else:
                if time() >= value_time:
                    dict.__delitem__(self, key)
                    return False
                return True
    
    def __setitem__(self, key, value):
        # Assume the last entry in the tuple is the age limit.
        # (value, age)
        # (value, value, age)
        # Use 0 as the last value if tuple is used but the max_age should be honored
        if isinstance(value, tuple):
            age, = value[-1:]
            if age == 0 or age > self.max_age:
                age = self.max_age
            value = value[:-1] # Erase the last value from 'value'
        else:
            age = self.max_age
        age = time() + float(age)

        with self.lock:
            dict.__setitem__(self, key, (value, age))

    def __getitem__(self, key):
        with self.lock:
            # Do not catch exception.
            # Dict suppose to return KeyError if key is not found
            value, value_time = dict.__getitem__(self, key)
            if time() >= value_time:
                dict.__delitem__(self, key)
                raise KeyError(key)

            return value
    
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