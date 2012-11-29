#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class DgData:

    def __init__(self, data):
        self.data = data

    def get_random(self):
        return random.choice(self.data)

    def get_kws(self):
        return [e["keyword"] for e in self.data if "keyword" in e]

    def get_all(self):
        return self.data

    def __get_smth_by_kw(self, kw, smth):
        l = filter(lambda e: e["keyword"] == kw, self.data)
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0][smth]
        else:
            return [e[text] for e in l]

    def get_text_by_kw(self, kw):
        return self.__get_smth_by_kw(kw, "text")

    def iterable(self):
        for i in self.data:
            yield i
