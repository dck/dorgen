#!/usr/bin/env python
# -*- coding: utf-8 -*-

# s = u"{He|She|It}{is|are}привет{going|suck}{to}{him}"

# deque = deque()
# depth = 0
# positions = []
# def mesh_lists(listOne, listTwo):
#     result = []
#     for l1 in listOne:
#         for l2 in listTwo:
#             firstWord = str(l1).strip()
#             secondWord = str(l2).strip()
#             result.append(" " + firstWord + " " + l2 + " ")
#     return result

# def action(string, pos, token):
#     global deque
#     deque.append(list(token[0]))

# def processDeque():
#     global deque
#     print deque
#     while len(deque) > 1:
#         l1 = deque.popleft()
#         l2 = deque.popleft()
#         res = mesh_lists(l1,l2)
#         deque.appendleft(res)
#     return [x.strip() for x in deque[0]]


# def openTag(string, pos, token):
#     global depth
#     depth += 1
# def closeTag(string, pos, token):
#     global depth
#     depth -= 1

# def cbWord(string, pos, word):
#     global depth
#     positions.append(depth)
#     # global depth
#     # if depth == 0:
#     #     with open("other.txt", "w") as f:
#     #         f.write(word[0].encode("utf8"))
# def cbBlock(string, pos, block):
#     global deque
#     print block[0]
#     deque.append(block[0])

# def removeDupsInARow(theList):
#     if len(theList) == 0:
#         return []
#     newList = theList[:1]
#     for item in theList[1:]:
#         if item != newList[-1]:
#             newList.append(item)
#     return newList

# _lcurl = Suppress('{').setParseAction(openTag)
# _rcurl = Suppress('}').setParseAction(closeTag)
# _pipe = Suppress('|')
# word = Regex("[^{|}]+").setParseAction(cbWord)

# varBlock = Forward()
# entry = word | varBlock
# varList = Group(entry + ZeroOrMore(_pipe + entry))
# varBlock << (_lcurl + Optional(varList) + _rcurl).setParseAction(cbBlock)
# template = ZeroOrMore(entry)


# with open("template.txt", "r") as f:
#     sfile = f.read().decode("utf8")

# res = template.parseString(sfile)
# #print positions
# #print list(deque)
# #print processDeque()

# print removeDupsInARow(positions)

import sys
from dorgen import dorgen
from dorgen.exceptions import Error

def usage():
    s = """
    Usage: %s <textfile> <kwfile> <template> [folder]

    This script provides generation of texts by keywords
        <textfile> - file with template text
        <kwfile> - file with keywords
        <template> - HTML template
        [folder] - deploy folder
    """ % sys.argv[0]
    print s


argv = sys.argv[1:]

if len(argv) < 3:
    usage()
    exit(2)

try:
    dorgen = dorgen.Dorgen(*argv[:4])
    dorgen.run()
except Error as e:
    print "[FAIL] Error while excecuting the script"
    print e