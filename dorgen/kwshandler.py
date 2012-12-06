#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *

class KWHandler:

    def __init__(self, theFile, keyword = "%keyword%", grouping = False ):
        self.file = theFile
        self.keyword = keyword
        with open(self.file) as f:
            lines = [l.strip().decode("utf8") for l in f.readlines()]
        if grouping:
            self.kws = self.__make_list_by_groups(lines)
        else:
            self.kws = self.__make_simple_list(lines)
        print self.kws
        if len(self.kws) == 0:
            raise GotZeroKeyWords()

    def __make_list_by_groups(self, lines):
        result = []
        current_group = []
        for line in lines:
            if not line.strip():
                result.append(current_group)
                current_group = []
            else:
                current_group.append(line)
        result.append(current_group)
        return filter(None, result) 

    def __make_simple_list(self, lines):
        return filter(None, lines)


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







