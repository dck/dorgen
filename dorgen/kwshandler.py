#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *

class KWHandler:

    def __init__(self, theFile, keyword = "%keyword%", grouping = False ):
        self.file = theFile
        self.keyword = keyword
        self.grouping = grouping
        with open(self.file) as f:
            lines = [l.strip().decode("utf8") for l in f.readlines()]
        if grouping:
            self.kws = self.__make_list_by_groups(lines)
        else:
            self.kws = self.remove_dups(self.__make_simple_list(lines))
        if len(self.kws) == 0:
            raise GotZeroKeyWords()

    def __make_list_by_groups(self, lines):
        result = []
        current_group = []
        for line in lines:
            if not line.strip():
                result.append(self.remove_dups(current_group))
                current_group = []
            else:
                current_group.append(line)
        result.append(self.remove_dups(current_group))
        return filter(None, result) 

    def __make_simple_list(self, lines):
        return filter(None, lines)

    def remove_dups(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if x not in seen and not seen_add(x)]

    def count(self):
        return len(self.kws)

    def __proccess_simple_kw_list(self, theList, variants):
        data = []
        newTexts = variants[:]
        for kw in theList:
            value = newTexts[0].replace(self.keyword, kw)
            data.append(dict(keyword = kw, text = value))
            del newTexts[0]
            if len(newTexts) == 0:
                newTexts = variants[:]
        return data



    def get_dg_data(self, variants):
        if len(variants) == 0:
            raise GeneratedZeroTexts()
        if self.grouping:
            return [self.__proccess_simple_kw_list(kw, variants) for kw in self.kws]
        else:
            return self.__proccess_simple_kw_list(self.kws, variants)







