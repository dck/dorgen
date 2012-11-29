#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from exceptions import ErrorInKeywords

class DgData:

    def __init__(self, data):
        self.data = data
        for e in self.data:
            e["file"] = self.make_filename(e["keyword"])

    def make_filename(self, name):
        TRANSTABLE = (
            (u" ", u"_"),
            (u"‘", u""),
            (u"’", u""),
            (u"«", u''),
            (u"»", u''),
            (u"“", u''),
            (u"”", u''),
            (u"–", u"-"),
            (u"—", u"-"), 
            (u"‒", u"-"), 
            (u"−", u"-"),
            (u"…", u""),
            (u"№", u""),
            (u"щ", u"sch"),
            (u"ё", u"yo"),
            (u"ж", u"zh"),
            (u"ц", u"ts"),
            (u"ч", u"ch"),
            (u"ш", u"sh"),
            (u"ы", u"yi"),
            (u"ю", u"yu"),
            (u"я", u"ya"),
            (u"а", u"a"),
            (u"б", u"b"),
            (u"в", u"v"),
            (u"г", u"g"),
            (u"д", u"d"),
            (u"е", u"e"),
            (u"з", u"z"),
            (u"и", u"i"),
            (u"й", u"j"),
            (u"к", u"k"),
            (u"л", u"l"),
            (u"м", u"m"),
            (u"н", u"n"),
            (u"о", u"o"),
            (u"п", u"p"),
            (u"р", u"r"),
            (u"с", u"s"),
            (u"т", u"t"),
            (u"у", u"u"),
            (u"ф", u"f"),
            (u"х", u"h"),
            (u"э", u"e"),
            (u"ъ", u""),
            (u"ь", u"")
        )
        translit = name.lower()
        for s_in, s_out in TRANSTABLE:
            translit = translit.replace(s_in, s_out)
        try:
            translit = str(translit)
        except UnicodeEncodeError:
            raise ErrorInKeywords()
        return translit + ".html"


    def get_random(self, number = 1):
        return random.sample(self.data, number)

    def get_kws(self):
        return [e["keyword"] for e in self.data if "keyword" in e]

    def get_filenames(self):
        return [e["file"] for e in self.data if "file" in e]

    def get_all(self):
        return self.data

    def __get_smth_by_e(self, element, smth):
        l = [e for e in self.data if e == element]
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0][smth]
        else:
            return [e[text] for e in l]

    def make_links(self, number = 5):
        filenames = self.get_filenames()
        if number > len(self.data) - 1:
            print "[WARN] You want pages to have %d links but specify only %d keywords" % (number, len(self.data))
            number = len(self.data) - 1
        for e in self.data:
            e["links"] = []
            i = 0
            while i<number:
                candidate = random.choice(filenames)
                i+=1
                while candidate == e["file"] or candidate in e["links"]:
                    candidate = random.choice(filenames)
                e["links"].append(candidate)

    def get_text_by_element(self, element):
        return self.__get_smth_by_e(element, "text")

    def get_links_by_element(self, element):
        return self.__get_smth_by_e(element, "links")

    def get_keyword_by_filename(self, filename):
        l = [e for e in self.data if e["file"] == filename]
        if len(l) == 0:
            return None
        else:
            return l[0]["keyword"]

    def iterable(self):
        for i in self.data:
            yield i

    def set_content(self, key, value):
        for l in self.data:
            if key == l:
                l["content"] = value

    def get_content_by_kw(self, kw):
            return self.__get_smth_by_kw(kw, "content")
