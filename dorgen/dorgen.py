#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from exceptions import *
from textgenerator import TextGenerator
from kwshandler import KWHandler
from templater import Templater
from dgdata import DgData

class Dorgen:

    def __init__(self, config):
        try:
            with open(config.text_file, "r") as f:
                self.text = f.read().decode("utf-8")
        except Exception as e:
            raise FileError(config.text_file)
        print "[OK] Read {0} file".format(config.text_file)

        try:
            with open(config.categories_file, "r") as f:
                self.categories = filter(None, [l.strip().decode("utf8") for l in f.readlines()])
        except Exception as e:
            raise FileError(config.categories_file)
        print "[OK] Read {0} categories".format(len(self.categories))

        if not os.access(config.keys_file, os.R_OK):
            raise FileError(config.keys_file)
        print "[OK] Proccessed {0} file".format(config.keys_file)

        t = os.path.abspath(config.template_folder)
        if not os.path.exists(t):
            raise FolderNotFound(t)           
        if not os.access(t, os.R_OK):
            raise FolderAccessError(f)
        print "[OK] Template folder is {0}".format(t)
        
        self.config = config

    def __prepare_deploy(self, deploy):
        f = os.path.abspath(deploy)
        if not os.path.exists(f):
            try:
                os.makedirs(f)
                print "     {0} not found. Creating...".format(f)
            except OSError as e:
                raise FolderAccessError(f)              
        if not os.access(f, os.W_OK):
            raise FolderAccessError(f)
        self.deploy_folder = f
        print "[OK] Deploy folder is {0}".format(f)


    def run(self, deploy):
        c = self.config
        self.__prepare_deploy(deploy)
        tg = TextGenerator(c.gen_capitalize, c.gen_shuffle)
        variants = tg.generate(self.text)
        print "[OK] Generated {0} variants of the text".format(len(variants))
        kwh = KWHandler(c.keys_file, c.gen_keyword, c.gen_grouping)
        print "[OK] Read {0} keywords".format(kwh.count())
        data = kwh.get_dg_data(variants)
        dgdata = DgData(data, self.categories, footer_links = c.footer_links, pages_in_category = c.pages_in_category)
        t = Templater(template_folder = c.template_folder,
                      templates = c.templates,
                      tgdata = dgdata,
                      deploy_folder = self.deploy_folder,
                      sitename = c.sitename.decode("utf8"),
                      words_in_preview = c.words_in_preview
                      )
        t.serialize()



