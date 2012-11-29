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

    def __init__(self, text, kw, template = "templates", deploy = "."):
        try:
            with open(text, "r") as f:
                self.text = f.read()
        except Exception as e:
            raise FileError(text)
        print "[OK] Read %s file" % text

        if not os.access(kw, os.R_OK):
            raise FileError(kw)
        self.kw = kw
        print "[OK] Read %s file" % kw

        t = os.path.abspath(template)
        if not os.path.exists(t):
            raise FolderNotFound(t)           
        if not os.access(t, os.R_OK):
            raise FolderAccessError(f)
        self.template_folder = t
        print "[OK] Template folder is %s" % t

        f = os.path.abspath(deploy)
        if not os.path.exists(f):
            try:
                os.makedirs(f)
                print "     %s not found. Creating..."
            except OSError as e:
                raise FolderAccessError(f)              
        if not os.access(f, os.W_OK):
            raise FolderAccessError(f)
        self.deploy_folder = f
        print "[OK] Deploy folder is %s" % f


    def run(self):
        tg = TextGenerator()
        variants = tg.generate(self.text)
        print "[OK] Generated %d variants of the text" % len(variants) 
        kwh = KWHandler(self.kw)
        print "[OK] Read %d keywords" % kwh.count()
        data = kwh.get_dg_data(variants)
        dgdata = DgData(data)
        t = Templater(template_folder = self.template_folder, tgdata = dgdata, deploy_folder = self.deploy_folder)
        t.serialize()