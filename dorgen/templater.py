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
                            print "[OK] Copied folder %s to %s" % (f, name)
                        except OSError:
                            pass
                    else:
                        copy2(f, self.deploy_folder)
                        print "[OK] Copied %s to %s" % (f, self.deploy_folder)
                except IOError as e:
                    print "[WARN] Can't copy %s" % f
            for i, v in  templates.iteritems():
                name = i + ".thtml"
                if os.path.exists(name) and os.path.isfile(name) and os.access(name, os.R_OK):
                    with open(name) as f:
                        templates[i] = f.read()
                        print "[OK] Teamplate %s has been read" % name
                else:
                    raise FileError(name)       

    def __check_template(self):
        for i, v in  templates.iteritems():
            if v.strip() == "":
                raise BadTemplateGiven("Template file is empty")

    def __output(self):
        with cd(self.deploy_folder):
            for e in self.data.iterable():
                with open(e["file"], "w") as f:
                    f.write(e["content"])
                    print "[OK] File %s is created" % f.name
                    #e["Created"] = True
            self.__make_site_map()


    def __make_site_map(self):
        links_str = ""
        for e in self.data.iterable():
            links_str += "<a href = '%s'> %s </a><br />" % (e["file"], e["keyword"].capitalize()) 
        
        pagetext = re.sub(re_map, links_str.encode("utf8"), templates["catalog"])

        with open("catalog.html", "w") as f:
            f.write(pagetext)
            print "[OK] Sitemap is created"

    def serialize(self):
        self.__create_enviroment()
        self.__check_template()
        for e in self.data.iterable():
            pagetext = re.sub(re_kw, e["keyword"].capitalize().encode("utf8"), templates["page"])
            pagetext = re.sub(re_text, e["text"].encode("utf8"), pagetext)
            pagetext = re.sub(re_map, "<a href = 'catalog.html'>Карта сайта</a>", pagetext)
            m = re_links.search(pagetext)
            if m:
                self.data.make_links(int(m.group(1)))
                links = [("<a href = '%s'> %s </a><br />" % (el, self.data.get_keyword_by_filename(el).capitalize())) for el in self.data.get_links_by_element(e)]
                links = '\n'.join(links)
                pagetext = re.sub(re_links, links.encode("utf8"), pagetext)
            self.data.set_content(e, pagetext)

        self.__output()