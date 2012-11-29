#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *

KEYWORD = "%kw%"

class KWHandler:

    def __init__(self, theFile):
        self.file = theFile
        with open(self.file) as f:
            lines = f.readlines()
        self.kws = filter(None, [e.strip() for e in lines])
        if len(self.kws) == 0:
            raise GotZeroKeyWords()

    def count(self):
        return len(self.kws)

    def get_dg_data(self, texts):
        if len(texts) == 0:
            raise GeneratedZeroTexts()
        global KEYWORD
        data = []
        newTexts = texts[:]
        for kw in self.kws:
            value = newTexts[0].replace(KEYWORD, kw)
            data.append(dict(keyword = kw, text = value))
            del newTexts[0]
            if len(newTexts) == 0:
                newTexts = texts[:]
        return data







