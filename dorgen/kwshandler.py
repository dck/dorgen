#!/usr/bin/env python
# -*- coding: utf-8 -*-


class KWHandler:

    def __init__(self, theList, theFile):
        self.variant = theList
        self.file = theFile

    def handle(self):
        return self.__getContext()

    def __getContext()
        file = open(self.theFile)
        while True:
          line = file.readline()
          if not line:
            file.close()
            break
          yield line