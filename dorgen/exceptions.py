# -*- coding: utf-8 -*-

#If you want to add new exception inherit from Error class
#and redefine msg attribute

class Error(Exception):
    pass

class FileError(Error):
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return "[FAIL] Can't read file: {0}".format(self.filename)

class FolderAccessError(Error):
    def __init__(self, folder):
        self.folder = folder
    def __str__(self):
        return "[FAIL] Permission denied\n[FAIL] The script can't write into: {0}".format(self.folder)

class GeneratedZeroTexts(Error):
    def __init__(self):
        pass
    def __str__(self):
        return "[FAIL] Continuation with 0 texts doesn't make senses"

class GotZeroKeyWords(Error):
    def __init__(self):
        pass
    def __str__(self):
        return "[FAIL] No keyword found. Please write some keywords to file"

class ParsingError(Error):
    def __init__(self, parse_exception):
        self.e = parse_exception
    def __str__(self):
        s  = "[FAIL] Error while parsing text file"
        s += "\n[FAIL] " + self.e.line
        s += "\n[FAIL] " + " " * (self.e.column-1) + "^"
        s += "\n[FAIL] " + str(self.e)
        s += "\n"
        return s

class BadTemplateGiven(Error):
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "[FAIL] Incorrect template\n[FAIL] {0}".format(self.reason.capitalize())

class ErrorInKeywords(Error):
    def __init__(self):
        pass
    def __str__(self):
        return "[FAIL] Look at keywords file. Bad characters found"