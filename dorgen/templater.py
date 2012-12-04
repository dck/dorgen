#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from exceptions import BadTemplateGiven, FileError
from shutil import copy2, copytree

re_kw   = re.compile(r"%key%", re.I|re.S|re.X)
re_text = re.compile(r"%text%", re.I|re.S|re.X)
re_map  = re.compile(r"%map%", re.I|re.S|re.X)
re_links  = re.compile(r"%links_(\d+)%", re.I|re.S|re.X)
re_categories  = re.compile(r"%kategorii_(\d+)%", re.I|re.S|re.X)

templates = {
    "page": "",
    "catalog": ""
}

class cd:
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class Templater:
    def __init__(self, template_folder, tgdata, deploy_folder = "."):
        self.template_folder = os.path.abspath(template_folder)
        self.data = tgdata
        self.deploy_folder = os.path.abspath(deploy_folder)

    def __create_enviroment(self):
        with cd(self.template_folder):
            templates_files = [f for f in os.listdir(".") if not f.endswith(".thtml")]
            for f in templates_files:
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
            for i, v in  templates.iteritems():
                name = i + ".thtml"
                if os.path.exists(name) and os.path.isfile(name) and os.access(name, os.R_OK):
                    with open(name) as f:
                        templates[i] = f.read().decode("utf-8")
                        print "[OK] Teamplate {} has been read".format(name)
                else:
                    raise FileError(name)       

    def __check_template(self):
        for i, v in  templates.iteritems():
            if v.strip() == "":
                raise BadTemplateGiven("Template file is empty")

    def __output(self):
        with cd(self.deploy_folder):
            for e in self.data.iterable():
                self.__write_to_file(e["file"], e["content"])
            self.__make_site_map()


    def __write_to_file(self, file, content):
        with open(file, "w") as f:
            f.write(content.encode("utf-8"))
            print "[OK] File {0} is created".format(f.name)


    def __make_site_map(self):
        links_str = u""
        for e in self.data.iterable():
            links_str += u"<a href = '{0}'> {1} </a><br />\n".format(e["file"], e["keyword"].capitalize()) 
        
        pagetext = re.sub(re_map, links_str, templates["catalog"])

        self.__write_to_file("catalog.html", pagetext)
   

    def __make_categories(self, number):
        result = []
        s = u""
        i = 1
        n = 1
        fulllist = [(e["keyword"], e["file"]) for e in self.data.iterable()]
        fulllist = fulllist[::-1]
        while fulllist:
            e = fulllist.pop()
            s += u"<a href = '{0}'> {1} <a/><br/>\n".format(e[1], e[0].capitalize())
            if i >= number:
                pagetext = re.sub(re_map, s, templates["catalog"])
                name = "category{0}.html".format(n)
                self.__write_to_file(name, pagetext)
                result.append(dict(filename = name, name = u"Категория {}".format(n)))
                s = u""
                n += 1
                i = 0
            i += 1
        if s:
            pagetext = re.sub(re_map, s, templates["catalog"])
            self.__write_to_file("category{}.html".format(n), pagetext)
            result.append(dict(filename = "category{}.html".format(n), name = u"Категория {}".format(n)))
        return result

    def serialize(self):
        self.__create_enviroment()
        self.__check_template()
        categories = []
        m = re_categories.search(templates["page"])
        if m:
            with cd(self.deploy_folder):
                    categories = self.__make_categories(int(m.group(1)))
        for e in self.data.iterable():
            pagetext = re.sub(re_kw, e["keyword"].capitalize(), templates["page"])
            pagetext = re.sub(re_text, e["text"], pagetext)
            pagetext = re.sub(re_map, u"<a href = 'catalog.html'>Карта сайта</a>", pagetext)
            m = re_links.search(pagetext)
            if m:
                self.data.make_links(int(m.group(1)))
                links = [(u"<a href = '{0}'>{1}</a><br />".format(el, self.data.get_keyword_by_filename(el).capitalize())) for el in self.data.get_links_by_element(e)]
                links = '\n'.join(links)
                pagetext = re.sub(re_links, links, pagetext)    

            links = [u"<a href='{filename}'>{name}</a><br />".format(**i) for i in categories]
            links = '\n'.join(links)
            pagetext = re.sub(re_categories, links, pagetext)
            
            self.data.set_content(e, pagetext)

        self.__output()