#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from exceptions import ErrorInKeywords, UndefinedData

class DgData:
    def __init__(self, data, categories, footer_links = 5, pages_in_category = 10):
        self.categories = categories
        self.footer_links = footer_links
        self.pages_in_category = pages_in_category
        if data:
            if isinstance(data[0], dict):
                self.data = self.__split_by_categories(data)
            elif isinstance(data[0], list):
                self.data = data
            else:
                raise UndefinedData()
        self.__make_filenames()
        self.__make_links(footer_links)
        self.__make_categories()
    def __split_by_categories(self, data):
        result = []
        temp = []
        for i in xrange(len(data)):
            temp.append(data[i])
            if len(temp) == self.pages_in_category or i == len(data)-1:
                result.append(temp)
                temp = []
        return result

    def __make_categories(self):
        self.cat_tuples = [] #[(name, self.make_filename(name)) for name in self.categories]
        min_data = min(len(self.data), len(self.categories))
        for i in range(min_data):
            self.cat_tuples.append((self.categories[i], self.make_filename(self.categories[i])))
        for e in self.iterable():
            e["categories"] = self.cat_tuples

    def __make_filenames(self):
        for e in self.iterable():
            e["file"] = self.make_filename(e["keyword"])

    def __make_links(self, number):
        filenames = [page for page in self.iterable()]
        if number > self.count() - 1:
            print "[WARN] You want pages to have {0} links but specify only {1} keywords".format(number, self.count())
            number = self.count() - 1
        for e in self.iterable():
            e["links"] = []
            i = 0
            while i < number:
                candidate = random.choice(filenames)
                i+=1
                while candidate == e or candidate["keyword"] in (l[0] for l in e["links"]):
                    candidate = random.choice(filenames)
                e["links"].append((candidate["keyword"], candidate["file"]))

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


    def get_filenames(self):
        return [e["file"] for e in self.iterable() if "file" in e]

    def get_key_by_filename(self, filename):
        for page in self.iterable():
            if page["filename"] == filename:
                return page["keyword"]
        return None

    def count(self):
        return sum(len(category) for category in self.data)

    def iterable(self):
        for l in self.data:
            for e in l:
                yield e
    def icategories(self):
        for cat_tuple in self.cat_tuples:
            yield cat_tuple

    def get_categories(self):
        return [c for c in self.icategories()]

    def get_all_by_category(self, category_tuple = None):
        if category_tuple:
            category_index = self.cat_tuples.index(category_tuple)
            return self.data[category_index]
        else:
            return [e for e in self.iterable()]


