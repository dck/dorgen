#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *

class KWHandler:

    def __init__(self, theFile, keyword = "%keyword%"):
        self.file = theFile
        self.keyword = keyword
        with open(self.file) as f:
            lines = f.readlines()
        self.kws = filter(None, [e.strip().decode("utf8") for e in lines])
        if len(self.kws) == 0:
            raise GotZeroKeyWords()

    def count(self):
        return len(self.kws)

    def get_dg_data(self, texts):
        if len(texts) == 0:
            raise GeneratedZeroTexts()
        data = []
        newTexts = texts[:]
        for kw in self.kws:
            value = newTexts[0].replace(self.keyword, kw)
            data.append(dict(keyword = kw, text = value))
            del newTexts[0]
            if len(newTexts) == 0:
                newTexts = texts[:]
        return data







