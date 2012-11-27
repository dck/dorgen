#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class DgData:

    def __init__(self, variants):
        self.vars = variants

    def get_random(self):
        return random.choice(self.vars)

    def get_kws(self):
        return [e[0] for e in self.vars]

