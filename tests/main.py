#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(sys.path[0]))


if __name__ == "__main__":

    path = sys.argv[1:]
    if len(path) == 0:
        path = os.getcwd()

    tests = unittest.defaultTestLoader.discover(path)
    unittest.TextTestRunner(verbosity=2).run(tests)