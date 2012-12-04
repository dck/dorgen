#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *
from collections import deque
from exceptions import ParsingError
import random

class TextGenerator:

    def __init__(self):
        _lcurl = Suppress('{')
        _rcurl = Suppress('}')
        _pipe = Suppress('|')
        entry = Regex("[^{|}]+").setParseAction(self.stripWords)
        varConstruction = Forward()
        varList = Group(entry + ZeroOrMore(_pipe + entry))
        varConstruction << (_lcurl + Optional(varList) + _rcurl).setParseAction(self.blockAction)
        template = ZeroOrMore(entry|varConstruction)

        self.blockQueue = []
        self.result = []
        self.grammar = template

    def generate(self, template, capitalize = True, shuffle = False):
        try:
            res = self.grammar.parseString(template, parseAll=True)
            self.result.append(res.asList())
        except ParseException as e:
            raise ParsingError(e)
        l = self.__processQueues()
        return self.__makeSentences(l, capitalize, shuffle)

    def blockAction(self, string, pos, token):
        self.blockQueue.append(token[0].asList())

    def stripWords(self, string, pos, token):
        return token[0].strip()

    def __processQueues(self):
        for block in self.blockQueue:
            for i in self.result[:]:
                lst = i
                index = lst.index(block)
                del lst[index]
                for word in block:
                    tmp = lst[:]
                    tmp.insert(index, word)
                    self.result.append(tmp)
                del self.result[0]
        return filter(None, self.result)

    def __makeSentences(self, seq, capitalize, shuffle):
        res = [' '.join(s) for s in seq]
        if shuffle:    random.shuffle(res)
        if capitalize: res = map(lambda word: word.capitalize(), res) # add smrty capitalizing
        return res