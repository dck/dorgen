#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pyparsing import *
from collections import deque
s = u"{He|She|It}{is|are}привет{going|suck}{to}{him}"

deque = deque()
depth = 0
def mesh_lists(listOne, listTwo):
    result = []
    for l1 in listOne:
        for l2 in listTwo:
            firstWord = str(l1).strip()
            secondWord = str(l2).strip()
            result.append(" " + firstWord + " " + l2 + " ")
    return result

def action(string, pos, token):
    global deque
    deque.append(list(token[0]))

def processDeque():
    global deque
    print deque
    while len(deque) > 1:
        l1 = deque.popleft()
        l2 = deque.popleft()
        res = mesh_lists(l1,l2)
        deque.appendleft(res)
    return [x.strip() for x in deque[0]]


def openTag(string, pos, token):
    global depth
    depth += 1
def closeTag(string, pos, token):
    global depth
    depth -= 1

def cbWord(string, pos, word):
    global depth
    if depth == 0:
        with open("other.txt", "w") as f:
            f.write(word[0].encode("utf8"))

_lcurl = Suppress('{').setParseAction(openTag)
_rcurl = Suppress('}').setParseAction(closeTag)
_pipe = Suppress('|')
word = Regex("[^{|}]+").setParseAction(cbWord)

varBlock = Forward()
entry = word | varBlock
varList = Group(entry + ZeroOrMore(_pipe + entry))
varBlock << (_lcurl + Optional(varList) + _rcurl)#.setParseAction(action)
template = ZeroOrMore(entry)


with open("template.txt", "r") as f:
    sfile = f.read().decode("utf8")

res = template.parseString(sfile)

#print processDeque()

from dorgen import templater

try:
    t = templater.Templater()
except Exception as e:
    print e