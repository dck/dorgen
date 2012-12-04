#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from exceptions import FileError, BadConfigFileError

class Config:
    def load(self, filename):
        try:
            with open(filename) as fh:
                content = fh.read().decode("utf-8")
        except Exception:
            raise FileError(filename)

        try:
            config = json.loads(content)
        except ValueError:
            raise BadConfigFileError()

        return config