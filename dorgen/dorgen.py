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

    def __init__(self, text_file, keys_file, template_folder, capitalize = 1, shuffle = 1,  **kwargs):
        try:
            with open(text_file, "r") as f:
                self.text = f.read().decode("utf-8")
        except Exception as e:
            raise FileError(text_file)
        print "[OK] Read {0} file".format(text_file)

        if not os.access(keys_file, os.R_OK):
            raise FileError(keys_file)
        self.keys_file = keys_file
        print "[OK] Read {0} file".format(keys_file)

        t = os.path.abspath(template_folder)
        if not os.path.exists(t):
            raise FolderNotFound(t)           
        if not os.access(t, os.R_OK):
            raise FolderAccessError(f)
        self.template_folder = t
        print "[OK] Template folder is {0}".format(t)
        
        self.capitalize = capitalize
        self.shuffle = shuffle


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
        self.__prepare_deploy(deploy)
        tg = TextGenerator()
        variants = tg.generate(self.text, self.capitalize, self.shuffle)
        print "[OK] Generated {0} variants of the text".format(len(variants))
        kwh = KWHandler(self.keys_file)
        print "[OK] Read {0} keywords".format(kwh.count())
        data = kwh.get_dg_data(variants)
        dgdata = DgData(data)
        t = Templater(template_folder = self.template_folder, tgdata = dgdata, deploy_folder = self.deploy_folder)
        t.serialize()