#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from exceptions import BadTemplateGiven, FileError
from shutil import copy2, copytree

re_kw   = re.compile(r"%key%", re.I|re.S|re.X)
re_text = re.compile(r"%text%", re.I|re.S|re.X)
re_map  = re.compile(r"%map%", re.I|re.S|re.X)

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
        for e in self.data.iterable():
            txt = self.text
            with open(e["keyword"] + ".html", "w") as f:
                txt = re.sub(re_kw, e["keyword"], txt)
                txt = re.sub(re_text, e["text"], txt)
                f.write(txt)

    def serialize(self):
        self.__create_enviroment()
        self.__check_template()