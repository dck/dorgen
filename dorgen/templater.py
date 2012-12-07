#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from exceptions import BadTemplateGiven, FileError
from shutil import copy2, copytree
from mako.template import Template


class ITemplate:
    pass


class Page(ITemplate):
    def __init__(self, template_text):
        self.template = Template(template_text)

    def render(self, page_dict, global_dict):
        return self.template.render_unicode(
                key = page_dict["keyword"],
                text = page_dict["text"],
                links = page_dict["links"],
                **global_dict
            )



class Index(ITemplate):
    def __init__(self, template_text):
        self.template = Template(template_text)

    def __make_prev(self, text, number):
            l = text.split(" ")[:number]
            return ' '.join(l)

    def render(self, page_iterator, words_in_preview, global_dict):
        all_pages = [(el["keyword"], el["file"], self.__make_prev(el["text"], words_in_preview)) for el in page_iterator]
        return self.template.render_unicode(
                links = all_pages,
                **global_dict
            )

class Map(ITemplate):
    def __init__(self, template_text):
        self.template = Template(template_text)

    def render(self, name, page_list, global_dict):
        links = [(p["keyword"], p["file"]) for p in page_list]
        return self.template.render_unicode(
                group_name = name,
                links = links,
                **global_dict
            )

class Templater:
    class cd:
        def __init__(self, newPath):
            self.newPath = newPath

        def __enter__(self):
            self.savedPath = os.getcwd()
            os.chdir(self.newPath)

        def __exit__(self, etype, value, traceback):
            os.chdir(self.savedPath)

    def __init__(self, sitename, template_folder, templates, tgdata, deploy_folder = ".", grouping = False, words_in_preview = 10):
        self.template_folder = os.path.abspath(template_folder)
        self.data = tgdata
        self.deploy_folder = os.path.abspath(deploy_folder)
        self.templates = templates
        self.grouping = grouping
        self.sitename = sitename
        self.words_in_preview = words_in_preview

    def __create_enviroment(self):
        with Templater.cd(self.template_folder):
            additional_files = [f for f in os.listdir(".") if not f.endswith(".html")]
            for f in additional_files:
                try:
                    if os.path.isdir(f):
                        name = self.deploy_folder + "/" + os.path.basename(f)
                        try:
                            copytree(f, name)
                            print "[OK] Copied folder {0} to {1}".format(f, name)
                        except OSError:
                            pass
                    else:
                        copy2(f, self.deploy_folder)
                        print "[OK] Copied {0} to {1}".format(f, self.deploy_folder)
                except IOError as e:
                    print "[WARN] Can't copy {}".format(f)
            self.templates_content = {} 
            for t, filename in self.templates.iteritems():
                try:
                    with open(filename) as fh:
                        content = fh.read().decode("utf8")
                except:
                    raise FileError(filename)

                if t == "page":
                    self.templates_content[t] = Page(content)
                elif t == "map":
                    self.templates_content[t] = Map(content)
                elif t == "index":
                    self.templates_content[t] = Index(content)


    def serialize(self):
        self.__create_enviroment()
        global_dict = dict(index_name = self.templates["index"],
                           map_name = self.templates["map"],
                           categories = self.data.get_categories(),
                           sitename = self.sitename)
        with Templater.cd(self.deploy_folder):
            result = self.templates_content["index"].render(self.data.iterable(), self.words_in_preview, global_dict)
            with open(global_dict["index_name"], "w") as f:
                f.write(result.encode("utf8"))
            print "[OK] Created {0} page".format(global_dict["index_name"])

            result = self.templates_content["map"].render(u"Карта сайта", self.data.get_all_by_category(), global_dict)
            with open(global_dict["map_name"], "w") as f:
                f.write(result.encode("utf8"))
            print "[OK] Created {0} page".format(global_dict["map_name"])

            for page in self.data.iterable():
                result = self.templates_content["page"].render(page, global_dict)
                with open(page["file"], "w") as f:
                     f.write(result.encode("utf8"))
                print "[OK] Created {0} page".format(page["file"])
            for category in self.data.icategories():
                theList = self.data.get_all_by_category(category)
                if theList:
                    result = self.templates_content["map"].render(category[0], theList, global_dict)
                    with open(category[1], "w") as f:
                        f.write(result.encode("utf8"))
                    print "[OK] Created {0} page".format(category[1])


